# Time: 2024/5/30/12:13
# Auth: YangJiahe
# Desc: 设置文件的扩展属性 还未完成(判断是否已经有该属性)
# version: 1.0

# @param file_path 文件路径
# @param attr_name 属性名
# @param attr_value 属性值 为bytes类型

import xattr
import os
import stat

def set_xattr(file_path, attr_name, attr_value):
    try:
        xattr.set(file_path, attr_name, attr_value)
        return True
    # 捕获所有异常
    except Exception as e:
        if e.errno == 95:
            # 当文件系统不支持扩展属性时，会抛出OSError异常，错误码为95即OperationNotSupportedError
            print(f"Error setting attribute: {e}")
            print("Operation not supported on the filesystem")
        elif e.errno == 1:
            # 当文件不存在时，会抛出OSError异常，错误码为1即FileNotFoundError
            print(f"Error setting attribute: {e}")
            print("No such file or directory")
        elif e.errno == 13:
            # 当没有权限时，会抛出OSError异常，错误码为13即PermissionError
            # 获取当前的权限
            current_permissions = stat.S_IMODE(os.lstat(file_path).st_mode)
            # 添加写权限
            os.chmod(file_path, current_permissions | stat.S_IWUSR)
            # 重新设置属性
            try:
                xattr.set(file_path, attr_name, attr_value)
                return True
            except Exception as e:
                print(f"Error setting attribute: {e}")
                return False
        return False

# # Example
# file_path = 'path_to_your_file'
# associated_file_path = 'path_to_associated_file'
# attr_name = 'user.my_attr'

# # 将关联文件的路径设置为扩展属性的值
# # 注意：需要将字符串转换为bytes类型，使用encode()方法
# set_xattr(file_path, attr_name, associated_file_path.encode())