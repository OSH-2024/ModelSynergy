import numpy as np
import ray
import matplotlib.pyplot as plt  # 导入matplotlib
import os
import time

# 生成布朗运动增量的函数
@ray.remote
def brownian_increments_batch(num_steps, dt, batch_size):
    # 分批生成增量
    total_batches = (num_steps - 1) // batch_size + 1
    increments_batches = [np.random.normal(0, np.sqrt(dt), size=min(batch_size, num_steps - 1 - i * batch_size)) for i in range(total_batches)]
    return increments_batches

# 段计算函数
@ray.remote
def compute_segment_batch(start_value, sigma, dt, increments_batches):
    A_segment = [start_value]
    for increments in increments_batches:
        for increment in increments:
            A_segment.append(A_segment[-1] + sigma * A_segment[-1] * increment)
    return np.array(A_segment[1:])  # 返回除了初始值之外的所有计算结果

# 定义随机微分方程的求解函数
# num_segments: 段数
# batch_size: 批处理大小
@ray.remote
def solve_sde_batch(sigma, A0, dt, T, num_steps, num_segments, batch_size):
    segment_length = num_steps // num_segments
    # 并行生成所有段的布朗运动增量
    increments_futures = [brownian_increments_batch.remote(segment_length - 1, dt, batch_size) for _ in range(num_segments)]
    # 一次性获取所有增量，确保所有增量计算都已完成
    increments_batches = ray.get(increments_futures)

    segment_futures = []
    start_value = A0
    for increments_batch in increments_batches:
        # 使用预先计算的增量进行段计算
        segment_future = compute_segment_batch.remote(start_value, sigma, dt, increments_batch)
        # 异步获取结果以更新start_value，但不阻塞循环
        segment_futures.append(segment_future)

    # 等待所有段计算完成
    for i, future in enumerate(segment_futures):
        if i == 0:
            segments = [ray.get(future)]
        else:
            # 更新start_value为前一个段的最后一个值
            start_value = segments[-1][-1]
            # 使用更新后的start_value重新计算当前段
            segments.append(ray.get(compute_segment_batch.remote(start_value, sigma, dt, increments_batches[i])))

    return np.concatenate([[A0], *segments])

def main():
    ray.init(address="auto")

    # 开始时间
    start_time = time.time()

    sigma = 0.2
    A0 = 1.0
    T = 1.0
    num_steps = 1000000
    dt = T / num_steps

    num_segments = 10 # 段数
    batch_size = num_steps // 10 # 批处理大小
    futures = [solve_sde_batch.remote(sigma, A0, dt, T, num_steps, num_segments, batch_size) for _ in range(10)]

    results = ray.get(futures)

    # 结束时间
    end_time = time.time()

    ray.shutdown()

    # 绘制每个SDE解的图像
    for i, result in enumerate(results):
        plt.plot(result, label=f"Simulation {i+1}")

    plt.xlabel("Time Steps")
    plt.ylabel("Value")
    plt.title("SDE Simulations")
    plt.legend()
    # 保存图像到文件
    plt.savefig("sde_ray.png", dpi=300)  # 指定文件名和分辨率

    print(f"Time taken: {end_time - start_time} seconds")

# 主程序
if __name__ == "__main__":
    main()