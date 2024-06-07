from PIL import Image, ImageDraw, ImageFont
import os
import random

# 生成图像的保存目录
output_dir = 'generated_images'
os.makedirs(output_dir, exist_ok=True)

# 生成图像的数量
num_images = 10000

# 生成图像的尺寸
image_width = 512
image_height = 512

# 生成图像
for i in range(num_images):
    # 创建新图像
    image = Image.new('RGB', (image_width, image_height), color='white')
    
    # 为图像创建绘制对象
    draw = ImageDraw.Draw(image)
    
    # 添加随机颜色的背景矩形
    rect_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.rectangle((0, 0, image_width, image_height), fill=rect_color)
    
    # 添加随机文本
    text = 'Complex Image'
    text_color = (255, 255, 255)  # 白色

    try:
        # 使用系统自带的字体
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 适用于大多数Linux系统
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        # 如果失败，使用默认字体
        print("Failed to load system font. Using default font.")
        font = ImageFont.load_default()

    # 获取文本边界框
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = ((image_width - text_width) // 2, (image_height - text_height) // 2)
    draw.text(text_position, text, fill=text_color, font=font)
    
    # 添加随机点
    num_points = random.randint(100, 500)
    for _ in range(num_points):
        point_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x = random.randint(0, image_width)
        y = random.randint(0, image_height)
        draw.point((x, y), fill=point_color)
    
    # 添加随机线段
    num_lines = random.randint(5, 20)
    for _ in range(num_lines):
        line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x1 = random.randint(0, image_width)
        y1 = random.randint(0, image_height)
        x2 = random.randint(0, image_width)
        y2 = random.randint(0, image_height)
        draw.line((x1, y1, x2, y2), fill=line_color, width=random.randint(1, 5))
    
    # 保存图像
    filename = os.path.join(output_dir, f'image_{i}.png')
    image.save(filename)
    print(f'Generated image: {filename}')
