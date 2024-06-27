import numpy as np
import ray
import matplotlib.pyplot as plt  # 导入matplotlib
import os
import time

@ray.remote
def brownian_increment(num_steps, dt, batch_size):
    # 一次性生成多个时间步骤的增量
    num_batches = num_steps // batch_size
    increments = [np.random.normal(0, np.sqrt(dt), size=batch_size) for _ in range(num_batches)]
    return np.concatenate(increments)

@ray.remote
def solve_sde(sigma, A0, dt, T, num_steps, batch_size):
    A = np.zeros(num_steps)
    A[0] = A0
    num_batches = num_steps // batch_size
    increments = ray.get([brownian_increment.remote(batch_size, dt, batch_size) for _ in range(num_batches)])
    increments = np.concatenate(increments)[:num_steps-1]  # 确保增量数组与时间步骤对齐
    for i in range(1, num_steps):
        A[i] = A[i-1] + sigma * A[i-1] * increments[i-1]
    return A

def main():
    ray.init(address="auto")

    # 开始时间
    start_time = time.time()

    sigma = 0.2
    A0 = 1.0
    T = 1.0
    num_steps = 1000000
    batch_size = 10000 # 批处理大小
    dt = T / num_steps

    futures = [solve_sde.remote(sigma, A0, dt, T, num_steps, batch_size) for _ in range(10)]

    results = ray.get(futures)

    # 结束时间
    end_time = time.time()

    # 绘制每个SDE解的图像
    for i, result in enumerate(results):
        plt.plot(result, label=f"Simulation {i+1}")
    
    plt.xlabel("Time Steps")
    plt.ylabel("Value")
    plt.title("SDE Simulations")
    plt.legend()
    # 保存图像到文件
    plt.savefig("sde_simulations.png", dpi=300)  # 指定文件名和分辨率

    print(f"Time taken: {end_time - start_time} seconds")

    ray.shutdown()

# 主程序
if __name__ == "__main__":
    main()