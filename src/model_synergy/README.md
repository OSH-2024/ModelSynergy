# modelsynergy命令

通过执行`modelsynergy - `命令可以调用该目录下的函数

## 根据目标文件生成kvcache

`modelsynergy -s [/path/to/source] [/path/to/kvcache]`
- 将使用模型处理 `/path/to/source` 处的文件，生成kvcache并将kvcache的地址设置为源文件的扩展属性
- 详见`control.py`中的`store_command()`

## 读取目标文件kvcache

获取目标文件的扩展属性中其kvcache的路径，并将其加载至模型
