"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     image.py
@Author:   shenfan
@Time:     2020/12/14 11:52
"""
# 百度tesseract-ocr使用

from aip import AipOcr
import os

""" API """
APP_ID = '23148495'
API_KEY = 'EsAkbYBii7tb3XB4NvuS4A14'
SECRET_KEY = 'IVv2ICrjDjDQsYmeRbqmfpwuqSWDYp7R'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    """ 可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 是否检测语言
    options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    image = get_file_content(image_path)

    """ 带参数调用通用文字识别 """
    result = client.basicGeneral(get_file_content(filePath), options)

    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    print(type(result), "和", type(text))

    """ save """
    fs = open("ocr.txt", 'w+')  # 将str,保存到txt
    fs.write(text)
    fs.close()
    print(os.path.dirname("ocr.txt"))
    return text


if __name__ == '__main__':
    filePath = r'C:\Users\SHENFAN\Desktop\中设数字\个人账号信息.png'
    print(img_to_str(filePath))
    print("识别完成。")





