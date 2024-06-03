// Time: 2024/6/3 20：39
// Auth: YangJiahe
// Desc: 添加消息
// version: 1.0 未完成(未处理报错)

// 向消息队列中添加消息
void send_message(int msgid, struct message *msg, char *text) {
    msg->message_type = 1;
    strncpy(msg->text, text, MAX_TEXT);

    if (msgsnd(msgid, (void *)msg, MAX_TEXT, 0) == -1) {
        fprintf(stderr, "msgsnd failed\n");
        exit(EXIT_FAILURE);
    }
}