// Time: 2024/7/2 20：39
// Auth: YangJiahe
// Desc: 添加消息
// version: 2.0

#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// 向消息队列中添加消息
void se_msg(char *msg, unsigned msg_prio) {
    const char *queue_name = "/task_queue";
    mqd_t mq;

    // 打开消息队列
    mq = mq_open(queue_name, O_WRONLY);
    if (mq == (mqd_t) -1) {
        perror("mq_open_se");
        exit(1);
    }

    // 发送消息到消息队列
    if (mq_send(mq, msg, strlen(msg), msg_prio) == -1) {
        perror("mq_send");
    }

    // 关闭消息队列
    mq_close(mq);
}