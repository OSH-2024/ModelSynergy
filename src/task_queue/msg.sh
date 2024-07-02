#!/bin/bash

# 定义服务单元文件的路径和名称
SERVICE_FILE=/etc/systemd/system/task_queue.service

# 编译消息队列服务
gcc -o task_queue main.c -lrt -Wall -g
# 编译动态链接库
gcc -fPIC -shared -o libreceive.so receive.c -lrt -Wall -g
gcc -fPIC -shared -o libsend.so send.c -lrt -Wall -g

# 将可执行文件 task_queue 移动至 /usr/local/bin 目录下
sudo mv task_queue /usr/local/bin
# 将动态链接库 libreceive.so 与 libsend.so 移动至 /usr/local/lib 目录下
sudo mv libreceive.so /usr/local/lib
sudo mv libsend.so /usr/local/lib

# 可执行文件的绝对路径
EXECUTABLE_PATH=/usr/local/bin/task_queue

# 创建服务单元文件并写入配置
cat <<EOF | sudo tee $SERVICE_FILE > /dev/null
[Unit]
Description=Task Queue Service

[Service]
Type=simple
ExecStart=$EXECUTABLE_PATH
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd，使新的服务单元文件生效
sudo systemctl daemon-reload

# 启用服务，使其在系统启动时自动启动
sudo systemctl enable task_queue.service

# 立即启动服务
sudo systemctl start task_queue.service

# 显示服务状态
sudo systemctl status task_queue.service