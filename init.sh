# 将src/auto_modify/watch 与 src/auto_modify/trans 移动到/usr/local/bin/下
sudo cp src/auto_modify/watch /usr/local/bin/
sudo cp src/auto_modify/trans /usr/local/bin/

# 增加脚本运行权限
chmod +x src/auto_modify/kill_watch.sh
chmod +x src/task_queue/msg.sh

# 执行msg.sh
cd src/task_queue
sudo ./msg.sh
cd ../..

# 将 src/auto_modify/kill_watch.sh 移动至 /usr/local/bin/
sudo cp src/auto_modify/kill_watch.sh /usr/local/bin/