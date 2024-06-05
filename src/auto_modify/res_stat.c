// 此程序用于监控计算资源使用情况，用于判断大模型后台运行条件

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUF 1024
#define MAX_CPU 10.0  // 后续测试后调整到合适值
#define MAX_MEM 10.0
#define MAX_GPU 10.0

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

double get_gpu_usage() {  // GPU
    // 当前程序限定为Intel GPU，且需要安装intel_gpu_top
    // 尚未测试

    FILE* fp;
    char buf[MAX_BUF];
    char* match;
    int render_usage;

    fp = popen("intel_gpu_top -s1 -o- | grep render", "r");
    fgets(buf, MAX_BUF, fp);
    pclose(fp);

    match = strstr(buf, "render busy:");
    sscanf(match, "render busy: %d%%", &render_usage);

    return (double)render_usage;
}

int main() {
    double cpu_usage = get_cpu_usage();
    double mem_usage = get_mem_usage();

    if(cpu_usage < MAX_CPU && mem_usage < MAX_MEM && gpu_usage < MAX_GPU) {
        printf("CPU usage: %.2f%%\n", cpu_usage);
        printf("Memory usage: %.2f%%\n", mem_usage);
        //printf("GPU usage: %.2f%%\n", gpu_usage);
        return 1;
    }

    return 0;
}