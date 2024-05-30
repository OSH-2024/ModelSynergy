import xattr

## 获取文件的扩展属性
# @param file_path 文件路径
# @param attr_name 属性名
def get_xattr(file_path, attr_name):
    # try:尝试获取文件扩展属性，当文件不存在该属性时，会抛出KeyError异常
    try:
        # 获取文件的扩展属性
        value = xattr.get(file_path, attr_name)
        # 返回True和属性值
        return True, value
    except KeyError:
        return False, None

# # 使用示例
# has_attr, value = get_xattr('path_to_your_file', 'user.my_attr')
# if has_attr:
#     print('The file has the attribute. The value is:', value)
# else:
#     print('The file does not have the attribute.')