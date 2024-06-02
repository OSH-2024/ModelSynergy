// 请使用Makefile编译
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h> // 目录操作
#include <glib.h> // 哈希表
#include <sys/types.h>
#include <sys/inotify.h>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define BUF_LEN     (1024 * (EVENT_SIZE + 16))
#define MAX_PATH_LENGTH 1024
#define ROOT_PATH   "/home/qsqsdac/test"   // 监控的根目录
// 进程运行时新创建的目录下文件无法监控，重新运行程序即可监控

GHashTable *wd_to_path; // 监视描述符到目录的映射

void add_watch_recursively(int fd, const char *dir_name) {  // 递归遍历目录树，添加监控
    DIR *dir = opendir(dir_name); // 打开根目录
    if (dir == NULL) {
        perror("opendir");
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) { 
        if (entry->d_type == DT_DIR) { 
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue; 
            }
            char path[MAX_PATH_LENGTH];
            snprintf(path, sizeof(path), "%s/%s", dir_name, entry->d_name); // 拼接目录路径
            add_watch_recursively(fd, path);
        }
    }

    int wd = inotify_add_watch(fd, dir_name, IN_MODIFY); // 添加监视描述符
    if (wd < 0) 
        perror("inotify_add_watch");
    else 
        g_hash_table_insert(wd_to_path, GINT_TO_POINTER(wd), g_strdup(dir_name));

    closedir(dir);
}

void handle_exit(int sig) {
    g_hash_table_destroy(wd_to_path);
    exit(0);
}

int main(int argc, char **argv) {
    signal(SIGINT, handle_exit);

    int length, i = 0;
    int fd;
    char buffer[BUF_LEN];  // inotify事件缓冲区
    char root_path[MAX_PATH_LENGTH] = ROOT_PATH;
    char *path;

    fd = inotify_init(); // 初始化inotify
    if (fd < 0) {
        perror("inotify_init");
        exit(1);
    }

    wd_to_path = g_hash_table_new(g_direct_hash, g_direct_equal); // 创建哈希表
    add_watch_recursively(fd, root_path);

    while (1) {
        i = 0;
        length = read(fd, buffer, BUF_LEN);  
        if (length < 0) {
            perror("read");
            continue;
        } 

        while (i < length) { // 遍历inotify事件
            struct inotify_event *event = (struct inotify_event *) &buffer[i];
            if (event->len) { // 文件名不为空
                if (i + EVENT_SIZE > length)
                    break;
                else if (event->mask & IN_MODIFY) { // 文件被修改
                    if (!(event->mask & IN_ISDIR)) { // 不是目录
                        path = g_hash_table_lookup(wd_to_path, GINT_TO_POINTER(event->wd));
                        printf("The file %s/%s was modified.\n", path, event->name);
                    }
                }
            }
            i += EVENT_SIZE + event->len;
        } 
    }
    
    close(fd);
    return 0;
}