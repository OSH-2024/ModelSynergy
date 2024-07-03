#include <stdlib.h>
#include <stdio.h>

extern void mq_create();
extern void se_msg(char *msg, unsigned msg_prio);
extern void re_msg(char *msg);

int main() {
    mq_create();
    char *msg = "hello";
    char *remsg = (char*)malloc(sizeof(char)*4096);
    se_msg(msg, 0);
    re_msg(remsg);
    printf("Received message: %s\n", remsg);
    free(remsg);
    return 0;
}