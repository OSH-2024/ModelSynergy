import numpy as np
import ray
import matplotlib.pyplot as plt  # 导入matplotlib
import os
import time

@ray.remote
def brownian_increment(dt):
    # 生成布朗运动增量
    return np.random.normal(0, np.sqrt(dt))

@ray.remote
def solve_sde(sigma, A0, dt, T, num_steps):
    A = np.zeros(num_steps + 1)
    A[0] = A0
    for i in range(1, num_steps + 1):
        A[i] = A[i-1] + sigma * A[i-1] * ray.get(brownian_increment.remote(dt))
    return A

def main():
    ray.init(address="auto")

    # 开始时间
    start_time = time.time()

    sigma = 0.2
    A0 = 1.0
    T = 1.0
    num_steps = 10000
    dt = T / num_steps

    futures = [solve_sde.remote(sigma, A0, dt, T, num_steps) for _ in range(10)]

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
    plt.savefig("sde_worse.png", dpi=300)  # 指定文件名和分辨率

    print(f"Time taken: {end_time - start_time} seconds")

# 主程序
if __name__ == "__main__":
    main()