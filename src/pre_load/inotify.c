#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/inotify.h>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define BUF_LEN     (1024 * (EVENT_SIZE + 16))

int main(int argc, char **argv) {
    int length, i = 0;
    int fd;
    int wd;
    char buffer[BUF_LEN];  // inotify事件缓冲区

    fd = inotify_init(); // 初始化inotify
    if (fd < 0) {
        perror("inotify_init");
    }

    wd = inotify_add_watch(fd, "/home/qsqsdac/test", IN_MODIFY);
    if (wd < 0) {
        perror("inotify_add_watch");
    }

    while (1) {
        i = 0;
        length = read(fd, buffer, BUF_LEN);  
        if (length < 0) {
            perror("read");
        } 

        while (i < length) { // 遍历inotify事件
            struct inotify_event *event = (struct inotify_event *) &buffer[i];
            if (event->len) { // 文件名不为空
                if (event->mask & IN_MODIFY) { // 文件被修改
                    if (!(event->mask & IN_ISDIR)) { // 不是目录
                        printf("The file %s was modified.\n", event->name);
                    }
                }
            }
            i += EVENT_SIZE + event->len;
        } 
    }
    
    inotify_rm_watch(fd, wd);
    close(fd);

    return 0;
}
