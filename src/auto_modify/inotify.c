// 请使用Makefile编译
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h> // 目录操作
#include <glib.h> // 哈希表
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/inotify.h>
#include <stdbool.h>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define BUF_LEN     (4096 * (EVENT_SIZE + 16))
#define MAX_PATH_LENGTH 4096
#define DEBOUNCE_INTERVAL 0.28 // 事件去抖时间

// 进程运行时新创建的目录下文件无法监控，重新运行程序即可监控

GHashTable *wd_to_path; // 哈希表，监视描述符到目录路径的映射
GHashTable *file_event_times; // 哈希表，文件名到事件时间的映射

// 递归遍历目录树，添加监控
void add_watch_recursively(int fd, const char *dir_name) {  
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

// 检查事件是否应该被忽略
// 返回1表示忽略，0表示不忽略
bool debounce_event(const char *filename) {
    time_t current_time = time(NULL);
    time_t *last_time_ptr = (time_t *)g_hash_table_lookup(file_event_times, filename);

    if (last_time_ptr != NULL) {
        // 如果时间差小于阈值，则忽略此事件
        if (difftime(current_time, *last_time_ptr) < DEBOUNCE_INTERVAL) {
            return true; // 忽略
        }
    }

    // 更新记录的时间
    if (last_time_ptr == NULL) {
        last_time_ptr = malloc(sizeof(time_t));
        g_hash_table_insert(file_event_times, strdup(filename), last_time_ptr);
    }
    *last_time_ptr = current_time;

    return false; // 不忽略
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <dir>\n", argv[0]);
        exit(1);
    }

    signal(SIGINT, handle_exit);

    struct stat path_stat;
    stat(argv[1], &path_stat);
    if (!S_ISDIR(path_stat.st_mode)) {
        fprintf(stderr, "%s is not a directory\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    int length, i = 0;
    int fd;
    char buffer[BUF_LEN];  // inotify事件缓冲区
    char *path;

    fd = inotify_init(); // 初始化inotify
    if (fd < 0) {
        perror("inotify_init");
        exit(1);
    }

    wd_to_path = g_hash_table_new(g_direct_hash, g_direct_equal); // 创建哈希表
    file_event_times = g_hash_table_new(g_str_hash, g_str_equal);
    // 递归添加监控
    add_watch_recursively(fd, argv[1]);

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
                else if (event->mask & IN_MODIFY) {
                    // 文件被修改
                    if (!debounce_event(event->name)) {
                        // 时间阈值外，不是同一个事件，可以处理
                        if (!(event->mask & IN_ISDIR)) {
                            // 不是目录
                            path = g_hash_table_lookup(wd_to_path, GINT_TO_POINTER(event->wd));
                            printf("The file %s/%s was modified.\n", path, event->name);
                        }
                    }
                }
                i += EVENT_SIZE + event->len;
            } 
        }
    }
    close(fd);
    return 0;
}