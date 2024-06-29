# 用RAY计算求解随机微分方程

## 随机微分方程与伊藤积分

- 随机微分方程是描述随机过程的微分方程，其形式通常为：

\[ dX_t = \mu(X_t, t) dt + \sigma(X_t, t) dW_t \]

这里，
- \( X_t \) 是随时间 \( t \) 变化的随机过程，
- \( \mu(X_t, t) \) 是漂移系数，描述了确定性部分，
- \( \sigma(X_t, t) \) 是扩散系数，描述了随机波动部分，
- \( W_t \) 是维纳过程（或布朗运动），表示随机扰动。

SDE的解通常是一个随机过程，它可以用来描述系统在随机环境下的演化。

- 伊藤积分是为了处理随机微分方程中的随机扰动项 \( dW_t \) 而引入的。与传统的黎曼积分不同，伊藤积分处理的是非确定性的积分。

对于给定的适应过程 \( f(t, \omega) \)，其关于维纳过程 \( W_t \) 的伊藤积分定义为：

\[ \int_0^t f(s, \omega) dW_s \]


## 具体任务

随机微分方程 (SDE) :

$$
dA(t) = \sigma \, A(t) \, dW_t
$$
通常被称为**几何布朗运动** (Geometric Brownian Motion, GBM)。其中`Wt`是标准布朗运动

其可用于：
- **工程与控制系统**
- **时间序列分析**
- **强化学习**

对于方程 \( dA(t) = \sigma A(t) dW_t \)，解的形式为：
\[ A(t) = A(0) \exp\left( \sigma W_t - \frac{1}{2} \sigma^2 t \right) \]
其中 \( A(0) \) 是初始值，\( W_t \) 是标准布朗运动。

这种解法揭示了几何布朗运动中指数增长或衰减的性质.

## 利用RAY模拟求数值解

求解该随机微分方程，可以采用循环累加的方式，将
$$
\int_0^T \sigma \, X(t) \, dW_t
$$
的`T`拆分为`dt`，本次实验中`dt = 1 000 000`

- 用`numpy.random.normal(0, numpy.sprt(dt))`模拟布朗运动的正态增量，由其增量独立性，可并行的进行
- 

## 部署RAY

首先部署一个虚拟环境`venv`

```bash
python3 -m venv venv
```

会生成一个名为`venv`的文件夹，在该文件夹下可进入虚拟环境

- 在`venv`虚拟环境下部署，`venv`可以提供一个轻量化的虚拟环境，与系统的`python`环境隔离(以免系统python环境不支持ray)
  1. **使用`source bin/activate`激活`venv`环境**
  2. `source deactivate`退出`venv`环境 
- `ray`的部署：
  1. 使用`ray`支持的`python`版本：3.6-3.9 以python3.9为例
  2. `python3.9 -m pip install --upgrade pip`
  3. `pip install --upgrade pip` 升级pip，确保支持ray
  4. `pip install ray[default]` 获取ray包

### 单机部署

1. 使用`ray start --head`启动一个**ray头节点**
> --port可以指定端口，例如：`ray start --head --port=6379
1. 在本地机器上使用`ray start --address=<head_node_address> --num-cpus=<cpu_num>`向已启动的头节点**添加工作节点**，并且指定该工作节点可使用的CPU数量
> 分配CPU数量的意思是指为一个工作节点分配2个CPU的计算资源，即可并行执行两个任务，ray可能会使用操作系统的线程调度功能来在CPU上并行执行多个任务

`ray status` 查看ray集群当前状态
`ray stop` 结束当前机器ray节点运行

#### 部署运行

```python
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
```

将每个增量分布式生成，并且集中叠加

经过测试，这种方法因为任务划分太细，导致分布式处理时网络通信压力较大，并且由于通信带来的内存压力极大的限制了分布式处理的性能，并不能体现出`ray`分布式计算的优化

#### 单机部署优化

1. **内部拆分**

- 分批：由于布朗运行具有独立增量性，在生成`dt`时间内增量时，每个增量服从独立的正态分布，可以分布式处理，当划分粒度为`1000000`时，若一次性生成会造成极大的内存开销，并且不利于将任务并行化，故采用分批的方式，多次生成，批处理大小经测试，在批处理大小为`200000`时与`10000`时性能较好，但批处理大小过大可能会造成单个节点内存开销过大
- 分步：将每次解`SDE`的过程分为：增量的生成，增量的累加。分成两步，并行进行

```python
@ray.remote
def brownian_increment(num_steps, dt, batch_size):
    # 一次性生成多个时间步骤的增量
    num_batches = num_steps // batch_size
    increments = [np.random.normal(0, np.sqrt(dt), size=batch_size) for _ in range(num_batches)]
    return np.concatenate(increments)
```

```python
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
```

2. **外部拆分**

- 由于求解该随机微分方程，其解具有随机性，故模拟10次并画出其图像来对比，每一次都可并行，划分为10个任务

```python
sigma = 0.2
A0 = 1.0
T = 1.0
num_steps = 1000000
batch_size = num_steps // 5 # 批处理大小
dt = T / num_steps

futures = [solve_sde.remote(sigma, A0, dt, T, num_steps, batch_size) for _ in range(10)]
```

### 多机部署

确保每台主机都安装了相同版本的操作系统和Python环境。建议使用虚拟环境来隔离项目依赖。

#### 1. 配置Ray头节点

选择一台主机作为Ray的头节点（head node）。在该主机上启动Ray头节点，并指定需要的资源（如CPU、内存等）：
```bash
ray start --head --port=6379
```
你可以指定任意的端口号。启动命令成功执行后，会返回一个命令，这个命令用于在其他工作节点上加入集群。

#### 2. 配置Ray工作节点

在其他主机（工作节点）上执行从头节点返回的命令，加入Ray集群。例如，如果头节点返回的命令如下：
```bash
ray start --address='192.168.1.100:6379' --redis-password='5241590000000000'
```
在每个工作节点上运行这个命令以加入集群。

#### 3. 验证集群

创建一个简单的Ray脚本来验证集群是否正常工作。例如，创建一个名为`ray_test.py`的文件，内容如下：
```python
import ray

ray.init(address='auto')

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
print(ray.get(futures))
```
运行该脚本：
```bash
python ray_test.py
```
如果集群配置正确，应该会看到输出`[0, 1, 4, 9]`。