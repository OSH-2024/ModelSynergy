import os
import xattr
from get import get_xattr
from set import set_xattr
from rmv import rmv_xattr

# 设置文件的扩展属性
file_path = '../test.txt'
attribute_name = 'user.comment'
attribute_value = b'This is a sample comment, hi'

# # 创建一个示例文件
# with open(file_path, 'w') as f:
#     f.write('Hello, World!')

print (file_path)
# 设置扩展属性
set_xattr(file_path, attribute_name, attribute_value)

# 获取扩展属性
success, value = get_xattr(file_path, attribute_name)
if success:
    print(f'Attribute value: {value.decode("utf-8")}')
else:
    print('Attribute not found') 

# 列出所有扩展属性
attributes = xattr.listxattr(file_path)
print(f'Attributes: {attributes}')

# 删除扩展属性
rmv_xattr(file_path, attribute_name)

success, value = get_xattr(file_path, attribute_name)
print(success, value)