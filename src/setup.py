# Time
# Auth: ChengSixiang
# Chng-Desc:

# Time 2024/7/3
# Auth: YangJiahe
# Chng-Desc: 
# 命令名改为小写 modelsynergy
# 增加 xattr pyxattr 的依赖设置

from setuptools import setup, find_packages

setup(
    name='modelsynergy',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'xattr==1.1.0',
        'pyxattr==0.8.1',
    ],
    entry_points={
        'console_scripts': [
            'modelsynergy=model_synergy.control:main',
        ],
    }
)