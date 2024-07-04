# modelsynergy命令

通过执行`modelsynergy - `命令可以调用该目录下的函数

## 根据目标文件生成kvcache

`modelsynergy -s [/path/to/source] [/path/to/kvcache]`
- 将使用模型处理 `/path/to/source` 处的文件，生成kvcache并将kvcache的地址设置为源文件的扩展属性
- 详见`control.py`中的`store_command()`

## 读取目标文件kvcache

获取目标文件的扩展属性中其kvcache的路径，并将其加载至模型

`modelsynergy -l [/path/to/source]`
- 将使用模型加载`/path/to/source`处文件的kvcache，并直接进入对话

## 监视目录下文件更改情况

监视指定目录下文件的更改情况，当文件更改后，向消息队列中发送更改文件的**绝对路径**，并在后台自动调用模型处理更改后的文件生成kvcache
`modelsynergy -w [/path/to/dir]`

## 停止监视

`modelsynergy -f`