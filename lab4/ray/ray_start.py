import ray

# 连接到Ray集群
ray.init(address='auto')

@ray.remote
def hello_world():
    return "Hello, world!"

# 调用远程函数
future = hello_world.remote()
result = ray.get(future)
print(result)
print(ray.nodes())
