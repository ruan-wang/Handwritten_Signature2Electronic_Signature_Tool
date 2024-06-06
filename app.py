'''
import cv2
from PIL import Image

def convert_signature_to_transparent_png(input_path, output_path):
    # 读取图片
    image = cv2.imread(input_path)
    # 转换到灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用二值化处理
    # 使用OTSU自动阈值
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 创建一个RGBA图像（具有透明通道）
    w, h = binary.shape
    transparent_image = Image.new("RGBA", (h, w), (0, 0, 0, 0))
    pixels = transparent_image.load()
    
    # 将二值化图像中的白色转换为透明，黑色转换为黑色
    for i in range(w):
        for j in range(h):
            if binary[i, j] == 0:
                pixels[j, i] = (0, 0, 0, 255)  # 黑色
            else:
                pixels[j, i] = (0, 0, 0, 0)  # 透明
    
    # 保存图像
    transparent_image.save(output_path)

# 使用函数
convert_signature_to_transparent_png('/nfs/home/1002_sunbo/RW_Experiments/Personal_project/Github_code/Image/name.jpg', '/nfs/home/1002_sunbo/RW_Experiments/Personal_project/Github_code/Image/output_signature.png')


'''
import streamlit as st
import cv2
from PIL import Image
import numpy as np
from io import BytesIO

def convert_signature_to_transparent_png(input_image):
    # 读取图片
    image = np.array(input_image.convert('RGB'))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 转换到灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用二值化处理
    # 使用OTSU自动阈值
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 创建一个RGBA图像（具有透明通道）
    w, h = binary.shape
    transparent_image = Image.new("RGBA", (h, w), (0, 0, 0, 0))
    pixels = transparent_image.load()
    
    # 将二值化图像中的黑色转换为透明，白色转换为黑色
    for i in range(w):
        for j in range(h):
            if binary[i, j] == 255:
                pixels[j, i] = (0, 0, 0, 255)  # 黑色
            else:
                pixels[j, i] = (0, 0, 0, 0)  # 透明
    
    return transparent_image




def main():
    st.title("手写签名转换为电子签名工具")
    uploaded_file = st.file_uploader("请选择一张手写签名图片", type=["jpg", "jpeg", "png"], help="支持的文件类型: jpg, jpeg, png. 最大文件大小: 10MB")

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file)
        result_image = convert_signature_to_transparent_png(input_image)
        
        # 显示结果
        st.image(result_image, caption='处理后的签名', use_column_width=True)
        
        # 保存按钮
        buf = BytesIO()
        result_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="下载电子签名",
            data=byte_im,
            file_name="电子签名.png",
            mime="image/png"
        )




if __name__ == "__main__":
    main()




#python /nfs/home/1002_sunbo/RW_Experiments/Personal_project/Github_code/text.py
