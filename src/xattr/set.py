# Time: 2024/6/2 16:00
# Auth: YangJiahe
# Desc: 设置文件的扩展属性 还未完成(判断是否已经有该属性)
# version: 1.0

# @param file_path 文件路径
# @param attr_name 属性名
# @param attr_value 属性值 为bytes类型

import ctypes
import os
import stat
from ctypes import c_char_p, c_void_p, c_size_t, c_int

libc = ctypes.CDLL('libc.so.6', use_errno=True)
libc.setxattr.argtypes = [c_char_p, c_char_p, c_void_p, c_size_t, c_int]
libc.setxattr.restype = c_int

def set_file_xattr(path, name, value):

    path_bytes = path.encode('utf-8')
    name_bytes = name.encode('utf-8')
    value_bytes = value.encode('utf-8')
    
    try:
        libc.setxattr(path_bytes, name_bytes, value_bytes, len(value_bytes), 0)
        return True
    except OSError as e:  # 特别捕获OSError
        if e.errno == 95:
            print(f"Error setting attribute: {e}")
        elif e.errno == 1:
            # 当文件不存在时，会抛出OSError异常，错误码为1即FileNotFoundError
            print(f"Error setting attribute: {e}")
            print("No such file or directory")
        elif e.errno == 13:
            # 当没有权限时，会抛出OSError异常，错误码为13即PermissionError
            # 获取当前的权限
            # current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
            # 添加写权限
            # os.chmod(path, current_permissions | stat.S_IWUSR)
            # 重新设置属性
            # try:
            #     set_file_xattr(path, name, value)
            #     return True
            # except Exception as e:
            #     print(f"Error setting attribute: {e}")
            #     return False
            print(f"Permission denied: {e}")
        return False

if __name__ == "__main__":
    set_file_xattr("/home/qsqsdac/test/abc.txt", "kv_cache_path", "/home/qsqsdac/test/1.txt")

