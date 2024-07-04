#!/bin/bash

# 设置要查找的进程名称
process_name=$1

# 使用ps命令和grep来查找进程，然后使用awk打印出PID
pid=$(ps -ef | grep "$process_name" | grep -v grep | awk '{print $2}')

# 检查是否找到了PID
if [ -z "$pid" ]; then
  echo "Process $process_name not found."
else
  # 使用kill命令终止进程
  kill $pid
  echo "Process $process_name has been terminated."
fi