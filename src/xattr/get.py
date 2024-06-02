# Time: 2024/5/30/9:50
# Auth: YangJiahe
# Desc: 设置文件的扩展属性
# version: 1.1

# @param file_path 文件路径
# @param attr_name 属性名

import xattr
import os
import stat

def get_xattr(file_path, attr_name):
    # try:尝试获取文件扩展属性，当文件不存在该属性时，会抛出KeyError异常
    try:
        # 获取文件的扩展属性
        value = xattr.get(file_path, attr_name)
        # 返回True和属性值
        return True, value
    except Exception as e:
        if e.errno == 95:
            # 当文件系统不支持扩展属性时，会抛出OSError异常，错误码为95即OperationNotSupportedError
            print(f"Error getting attribute: {e}")
            print("Operation not supported on the filesystem")
        elif e.errno == 1:
            # 当文件不存在时，会抛出OSError异常，错误码为1即FileNotFoundError
            print(f"Error getting attribute: {e}")
            print("No such file or directory")
        elif e.errno == 13:
            # 当没有权限时，会抛出OSError异常，错误码为13即PermissionError
            # 获取当前的权限
            current_permissions = stat.S_IMODE(os.lstat(file_path).st_mode)
            # 添加读权限
            os.chmod(file_path, current_permissions | stat.S_IRUSR)
            # 重新获取属性
            try:
                value = xattr.get(file_path, attr_name)
                return True, value
            except Exception as e:
                print(f"Error getting attribute: {e}")
                return False, None
        return False, None

# # Example
# has_attr, value = get_xattr('path_to_your_file', 'user.my_attr')
# if has_attr:
#     print('The file has the attribute. The value is:', value)
# else:
#     print('The file does not have the attribute.')