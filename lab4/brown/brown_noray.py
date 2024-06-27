import numpy as np
import matplotlib.pyplot as plt
import os
import time

# 使用ray.remote装饰器定义布朗运动的增量函数
def brownian_increment(dt):
    return np.random.normal(0, np.sqrt(dt))

# 定义随机微分方程的求解函数
def solve_sde(sigma, A0, dt, T, N):
    A = np.zeros(N + 1)
    A[0] = A0
    for i in range(1, N + 1):
        A[i] = A[i-1] + sigma * A[i-1] * brownian_increment(dt)
    return A

def main():
    # 开始时间
    start_time = time.time()

    # 参数设置
    sigma = 0.2
    A0 = 1.0
    T = 1.0
    N = 1000000
    dt = T / N

    # 解随机微分方程
    A = [solve_sde(sigma, A0, dt, T, N) for _ in range(10)]

    # 绘制每个SDE解的图像
    for i, result in enumerate(A):
        plt.plot(result, label=f"Simulation {i+1}")

    # 结束时间
    end_time = time.time()
    
    plt.xlabel("Time Steps")
    plt.ylabel("Value")
    plt.title("SDE Simulations")
    plt.legend()
    # 保存图像到文件
    plt.savefig("sde.png", dpi=300)  # 指定文件名和分辨率

    print(f"Time taken: {end_time - start_time} seconds")

# 主程序
if __name__ == "__main__":
    main()