// Time: 2024/06/05/21:06
// Auth: YangJiahe
// Desc: Get the value of an extended attribute of a file
// version: 1.0

#include <sys/xattr.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

// file_path: 文件路径
// attr_name: 属性名
// value: 字符串，表示对应kvcache路径
// size: 属性值大小
int get_xattr(const char *file_path, const char *attr_name, char *value, ssize_t size) {
    ssize_t ret = getxattr(file_path, attr_name, value, size);
    if (ret == -1) {
        switch (errno) {
            // 文件系统不支持扩展属性
            case ENOTSUP:
                printf("Error getting attribute: Operation not supported on the filesystem\n");
                return ENOTSUP;
            // 文件不存在
            case ENOENT:
                printf("Error getting attribute: No such file or directory\n");
                return ENOENT;
            // 权限不足
            case EACCES:
                // 获取当前权限
                struct stat file_stat;
                stat(file_path, &file_stat);
                // 修改权限
                int ch_re = chmod(file_path, 0777);
                if (ch_re == -1) {
                    printf("Error getting attribute: Permission denied\n");
                    return EACCES;
                } else {
                    // 重新获取属性
                    ret = getxattr(file_path, attr_name, value, size);
                    if (ret == -1) {
                        printf("Error getting attribute: %s\n", strerror(errno));
                        return errno;
                    }
                    // 恢复权限
                    ch_re = chmod(file_path, file_stat.st_mode);
                    if (ch_re == -1) {
                        printf("Error getting attribute: %s\n", strerror(errno));
                        return errno;
                    }
                }
            // 属性不存在
            default:
                return -1;
        }
    }
    return 0;
}