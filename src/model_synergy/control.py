import subprocess
import sys
import os
import mimetypes
from .set import set_xattr
from .get import get_xattr

def store_command(file_path, kv_cache_path):

    command = [
        "python", "-m", "inf_llm.gen",
        "--model-path", "Qwen/Qwen1.5-0.5B-Chat",
        "--inf-llm-config-path", "config/qwen0b5-inf-llm.yaml",
        "--prompt-file", file_path,  # 使用参数file_path
        "--store-kv-cache-file", kv_cache_path  # 使用参数kv_cache_path
    ]

    # 设置扩展属性
    set_xattr(file_path, "user.kvcache", kv_cache_path.encode())
    print("set_over")

    # 调用命令
    result = subprocess.run(command, capture_output=True, text=True)

    # 打印命令的输出
    # print("STDOUT:", result.stdout)
    # print("STDERR:", result.stderr)

def load_command(file_path):
    has_attr, kvcache_path = get_xattr(file_path, 'user.kvcache')
    if not has_attr:
        print("Error: The file does not have the attribute 'user.kvcache'.")
        return
    command = f"python -m inf_llm.chat --model-path Qwen/Qwen1.5-0.5B-Chat --inf-llm-config-path config/qwen0b5-inf-llm.yaml --load-kv-cache-file {kvcache_path}"

    os.system(command)
    print("chat finished")


def process_directory(directory, kv_cache_path):
    for entry in os.scandir(directory):
        if entry.is_file():
            mime_type, _ = mimetypes.guess_type(entry.path)
            if mime_type and mime_type.startswith('text/'):
                store_command(entry.path, kv_cache_path)
            else:
                print(f"Warning: The file '{entry.path}' is not a text file and will be skipped.")
        elif entry.is_dir():
            process_directory(entry.path, kv_cache_path)

def main():
    if sys.argv[1] == "--store" or sys.argv[1] == "-s":
        if len(sys.argv) != 4:
            print("Usage: ModelSynergy --store <file-path> <kv-cache-path>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        kv_cache_path = sys.argv[3]

        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text/'):
                store_command(file_path, kv_cache_path)
            else:
                print(f"Error: The file '{file_path}' is not a text file.")
        elif os.path.isdir(file_path):
            process_directory(file_path, kv_cache_path)
    elif sys.argv[1] == "--load" or sys.argv[1] == "-l":
        if len(sys.argv) != 3:
            print("Usage: ModelSynergy --load <file-path>")
            sys.exit(1)
        
        file_path = sys.argv[2]

        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text/'):
                load_command(file_path)
            else:
                print(f"Error: The file '{file_path}' is not a text file.")
        elif os.path.isdir(file_path):
            print(f"Error: The file '{file_path}' is a directory.")