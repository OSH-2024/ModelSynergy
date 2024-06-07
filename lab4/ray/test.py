import os
import time
import cv2
import numpy as np
from glob import glob

def process_image(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 构造输出路径
    output_path = os.path.join('_serial_output', '_out_sial_' + os.path.basename(image_path))
    # 保存处理后的图像
    cv2.imwrite(output_path, gray_image)
    return output_path

# 创建输出目录
if not os.path.exists('_serial_output'):
    os.makedirs('_serial_output')

# 获取所有图像文件路径
image_files = glob('generated_images/*.jpg') + glob('generated_images/*.png')  # 假设图像存储在images文件夹中

# 记录开始时间
start_time = time.time()

# 处理图像文件
for image_path in image_files:
    output_path = process_image(image_path)

# 记录结束时间
end_time = time.time()

print(f"Processed {len(image_files)} images.")
print(f"Time taken: {end_time - start_time} seconds")