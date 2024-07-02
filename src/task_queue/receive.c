// Time: 2024/7/2 
// Auth: YangJiahe
// Desc: 接受消息
// version: 1.0

#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 从消息队列中接收消息
void re_msg(char *msg) {
    const char *queue_name = "/task_queue";
    const int max_msg_size = 4096;
    mqd_t mq;
    unsigned int msg_prio = 0;
    ssize_t msg_len;

    // 打开消息队列
    mq = mq_open(queue_name, O_RDONLY);
    if (mq == (mqd_t) -1) {
        perror("mq_open");
        exit(1);
    }

    // 接收消息
    msg_len = mq_receive(mq, msg, max_msg_size, &msg_prio);
    if (msg_len == -1) {
        perror("mq_receive");
    } else {
        // msg[msg_len] = '\0';
        // printf("Received message: %s\n", msg);
    }

    // 关闭消息队列
    mq_close(mq);
}