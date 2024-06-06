// 此程序用于监控计算资源使用情况，用于判断大模型后台运行条件

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUF 1024
#define MAX_CPU 10.0  // 后续测试后调整到合适值
#define MAX_MEM 10.0

double get_cpu_usage() {  // CPU
    FILE* fp;
    char buf[MAX_BUF];
    size_t bytes_read;
    unsigned long long total_user, total_user_low, total_sys, total_idle, total;

    fp = fopen("/proc/stat","r");
    bytes_read = fread(buf, 1, MAX_BUF, fp);
    fclose(fp);

    if(bytes_read == 0 || bytes_read == sizeof(buf))
        return -1.0;

    buf[bytes_read] = '\0';
    sscanf(buf, "cpu %llu %llu %llu %llu", &total_user, &total_user_low, &total_sys, &total_idle);

    total = total_user + total_user_low + total_sys + total_idle;

    return (double)(total_user + total_user_low + total_sys) / total * 100;
}

double get_mem_usage() {  // 内存
    FILE* fp;
    char buf[MAX_BUF];
    size_t bytes_read;
    char* match;
    long total_mem;
    long free_mem;

    fp = fopen("/proc/meminfo", "r");
    bytes_read = fread(buf, 1, MAX_BUF, fp);
    fclose(fp);

    if(bytes_read == 0 || bytes_read == sizeof(buf))
        return -1.0;

    buf[bytes_read] = '\0';
    match = strstr(buf, "MemTotal:");
    sscanf(match, "MemTotal: %ld kB", &total_mem);
    match = strstr(buf, "MemFree:");
    sscanf(match, "MemFree: %ld kB", &free_mem);

    return (double)(total_mem - free_mem) / total_mem * 100;
}

// GPU部分后续配置NVIDIA-SMI命令行工具后完成

int main() {
    double cpu_usage = get_cpu_usage();
    double mem_usage = get_mem_usage();

    if(cpu_usage < MAX_CPU && mem_usage < MAX_MEM) {
        printf("CPU usage: %.2f%%\n", cpu_usage);
        printf("Memory usage: %.2f%%\n", mem_usage);
        return 1;
    }

    return 0;
}