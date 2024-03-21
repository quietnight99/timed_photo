import requests
import base64
import hashlib
import os
from PIL import Image
from datetime import datetime

Wenhook_url = ''
Wenhook_url_1 = ''


def Wenhook_send(picture_name, titles='默认标题', descriptions='默认描述') :
    # API URL

    # 请求体数据
    data = {
        "msgtype" : "news",
        "news" : {
            "articles" : [
                {
                    "title" : titles,
                    "description" : descriptions,
                    "url" : r"\\192.168.30.65\yf1\wengzhichao\picture\{}".format(picture_name),
                    "picurl" : r"\\192.168.30.65\yf1\wengzhichao\picture\{}".format(picture_name),
                }
            ]
        }
    }

    # 发送请求
    response = requests.post(url = Wenhook_url, json = data)
    print(response.text)


# 企业微信直接推送图片，但要小于2M所以对图片进行压缩
def load_image(file_path) :
    # 图片路径
    picture_url = r"\\192.168.30.65/yf1/wengzhichao/picture/"
    # 图片路径+图片名称
    file_path = picture_url + file_path
    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 如果文件大小小于 1.8M，直接读取
    if file_size <= 1.8 * 1024 * 1024 :
        with open(file_path, 'rb') as f :
            image_data = f.read()
    else :
        # 如果文件大小大于 1.8M，压缩至小于 1.8M 后读取
        max_size = 1.8 * 1024 * 1024
        output_file = 'compressed.jpg'
        with Image.open(file_path) as im :
            im.thumbnail((1024, 1024))
            im.save(output_file, optimize = True, quality = 85)
            while os.path.getsize(output_file) > max_size :
                im = im.resize((int(im.width * 0.9), int(im.height * 0.9)), resample = Image.LANCZOS)
                im.save(output_file, optimize = True, quality = 85)

        with open(output_file, 'rb') as f :
            image_data = f.read()

    return image_data


def Wenhook_send_time() :
    # API URL
    url = Wenhook_url_1
    # 创建一个 datetime 对象
    now = datetime.now()
    # 格式化 datetime 对象为字符串
    formatted_date = now.strftime("%H:%M:%S")
    # 请求体数据
    data = {
        "msgtype" : "text",
        "text" : {
            "content" : str(formatted_date),
        }
    }

    # 发送请求
    response = requests.post(url = url, json = data)
    print(response.text)




def Wenhook_send_1(picture_name) :
    # API URL
    url = Wenhook_url_1
    Wenhook_send_time()
    picture_data = load_image(picture_name)
    base64_data = base64.b64encode(picture_data).decode('utf-8')
    md5_value = hashlib.md5(picture_data).hexdigest()
    # 请求体数据
    data = {
        "msgtype" : "image",
        "image" : {
            "base64" : base64_data,
            "md5" : md5_value,
            "pic_url" : ""
        }
    }

    # 发送请求
    response = requests.post(url = url, json = data)
    print(response.text)
# #
# # Wenhook_send('IMG_20230517_123035.jpg')
# Wenhook_send_1('IMG_20230531_100307.jpg')
