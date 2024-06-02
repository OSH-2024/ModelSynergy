// Time: 2024/6/2 21:40
// Auth: YangJiahe
// Desc: 任务队列，向消息队列中添加消息(待处理的文件路径)，然后从消息队列中接收消息
// version: 1.0 未完成

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>

// 最大文本长度
#define MAX_TEXT 1024

// 消息结构体
struct message {
    long message_type;
    char text[MAX_TEXT];
};

int main() {
    int running = 1;
    struct message some_message;
    int msgid;
    char buffer[BUFSIZ];

    // 创建消息队列
    msgid = msgget((key_t)1234, 0666 | IPC_CREAT);

    if (msgid == -1) {
        fprintf(stderr, "msgget failed\n");
        exit(EXIT_FAILURE);
    }

    // 向消息队列中添加消息
    while (running) {
        printf("Enter file path: ");
        fgets(buffer, BUFSIZ, stdin);
        some_message.message_type = 1;
        strcpy(some_message.text, buffer);

        if (msgsnd(msgid, (void *)&some_message, MAX_TEXT, 0) == -1) {
            fprintf(stderr, "msgsnd failed\n");
            exit(EXIT_FAILURE);
        }

        if (strncmp(buffer, "end", 3) == 0) {
            running = 0;
        }
    }

    // 从消息队列中接收消息
    if (msgrcv(msgid, (void *)&some_message, BUFSIZ, 0, 0) == -1) {
        fprintf(stderr, "msgrcv failed\n");
        exit(EXIT_FAILURE);
    }

    printf("You wrote: %s", some_message.text);

    // 删除消息队列
    if (msgctl(msgid, IPC_RMID, 0) == -1) {
        fprintf(stderr, "msgctl(IPC_RMID) failed\n");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}