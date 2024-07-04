#include <stdio.h>
#include <stdlib.h>
#include "getxattr.c"

int main() {
    char command[8192];
    char file[4096];
    char kv_cache_path[4096];

    while(1) {
        //读取消息队列
        re_msg(file_path);

        //读取扩展属性
        get_xattr(file_path, "user.kvcache", kv_cache_path, 4096);

        // 使用sprintf构建命令字符串
        sprintf(command, "python -m inf_llm.gen --model-path " \
        "Qwen/Qwen1.5-0.5B-Chat --inf-llm-config-path config/qwen0b5-inf-llm.yaml " \
        "--prompt-file %s --store-kv-cache-file %s", file_path, kv_cache_path);

        //执行命令
        system(command);
    }

    return 0;
}