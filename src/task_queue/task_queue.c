// Time: 2024/7/2
// Auth: YangJiahe
// Desc: 任务队列，向消息队列中添加消息(待处理的文件路径)，然后从消息队列中接收消息
// version: 2.0 未完成
// 使用方法：

// message_queue.c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <string.h>
#include <unistd.h>

#define QUEUE_NAME "/task_queue"
#define MAX_MSG_SIZE 4096
#define MAX_MSG_NUM 10
#define MSG_STOP "exit"

// 创建消息队列
void mq_create() {
    mqd_t mq; // 消息队列描述符
    // 创建消息队列结构体
    struct mq_attr attr;

    // 初始化消息队列属性
    // 在阻塞模式下创建消息队列
    // 当一个进程尝试向已满的消息队列发送消息或者从空的消息队列读，该线程将会被阻塞
    attr.mq_flags = 0;
    attr.mq_maxmsg = MAX_MSG_NUM;
    attr.mq_msgsize = MAX_MSG_SIZE;
    attr.mq_curmsgs = 0; // 当前消息队列中的消息数，有系统维护，当前设置为0

    // 创建消息队列并以只读模式打开
    mq = mq_open(QUEUE_NAME, O_CREAT | O_RDONLY, 0644, &attr);
    if (mq == (mqd_t) -1) {
        perror("mq_create");
        exit(1);
    }
}