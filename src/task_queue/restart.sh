# 删除原有的消息队列
sudo rm /dev/mqueue/task_queue

# 编译消息队列服务
gcc -o task_queue main.c -lrt -Wall -g
# 运行消息队列服务
./task_queue &

# 进程名
PROCESS_NAME="task_queue"

# 使用pgrep获取进程ID
PID=$(pgrep -f $PROCESS_NAME | awk 'NR==2')

# 检查PID是否为空
if [ ! -z "$PID" ]; then
    echo "Killing process $PROCESS_NAME with PID $PID"
    kill $PID
else
    echo "Process $PROCESS_NAME not found"
fi

rm ./task_queue

echo new: 
ls /dev/mqueue/