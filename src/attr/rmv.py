# Time: 2024/7/3
# Auth: YangJiahe
# Desc: 删除文件的扩展属性
# version: 1.0

# @param file_path 文件路径
# @param attr_name 属性名

import xattr

def rmv_xattr(file_path, attr_name):
    """
    删除指定文件的指定扩展属性。
    
    :param file_path: 文件路径
    :param attr_name: 要删除的属性名
    :return: 如果删除成功返回True, 否则返回False
    """
    try:
        attrs = xattr.xattr(file_path)
        if attr_name.encode('utf-8') in attrs:
            del attrs[attr_name]
            return True
        else:
            print(f"attribute {attr_name} is not in {file_path}。")
            return False
    except Exception as e:
        print(f"error in remove attribute {e}")
        return False