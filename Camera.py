from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time
import warnings
warnings.filterwarnings("ignore", message="urllib3")
from Send_Photo import Send_Photo
from Webhook_send_msg import Wenhook_send,Wenhook_send_1

# 调用手机相机拍照并上传
def camera():
    try :
        now = datetime.now()
        nowtime = now.strftime("%Y-%m-%d %H:%M:%S")
        print(nowtime)
        # 点亮手机
        os.system("adb shell input keyevent 224")
        time.sleep(1)
        # 解锁屏幕（前提需要在设置里面把手机登录的密码这些都关掉）
        os.system("adb shell input keyevent 82")
        time.sleep(1)
        # 启动相机
        os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
        # 多留点时间自动对焦
        time.sleep(3)
        # camera键 拍照
        os.system("adb shell input keyevent 27")
        # 留点时间存储照片防止读取到上一张图片
        time.sleep(5)
        # 获得最新的一张照片的文件名
        picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
        name_list = picture_url.split("\n")
        # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
        myfilename = name_list[1]
        print("图片名称{}".format(myfilename))
        time.sleep(1)
        # 指定要保存到的目标文件夹路径
        target_folder = r"\\192.168.30.65/yf1/wengzhichao/picture/"
        # 构建adb命令
        adb_code = "adb pull /storage/emulated/0/DCIM/Camera/" + myfilename + " " + target_folder
        # 执行adb命令
        os.system(adb_code)
        time.sleep(1)
        # back键 暂退相机
        os.system("adb shell input keyevent 4")
        time.sleep(1)
        # Power键 黑屏
        os.system("adb shell input keyevent 26")
        time.sleep(2)

        # # 调用邮件发送图片至邮箱
        # Send_Photo(myfilename)
        # time.sleep(2)

        # 企业微信推送图片
        # Wenhook_send(myfilename)
        # time.sleep(2)

        Wenhook_send_1(myfilename)
        # return myfilename
    except Exception as e :
        print(F"Error{e}")

# 处理时间
def photo_time(times=None):
    times = times.split(",")
    scheduler = BlockingScheduler()
    for i in times:
        scheduler.add_job(camera, 'cron', day_of_week = None, hour = i[0:2:], minute = i[2:4:], second = i[4:6:],timezone = "Asia/Shanghai")
    scheduler.start()

# time.sleep(1)
# camera()
# time.sleep(2)

photo_time('084900,001000,001200,011200,011400,015900,020100,025900,030100,030900,031100,034900,035100,035900,040100,042900,043100,'
           '055900,060100,065900,070100,111900,112100,124900,125100,150000,150200,170000,170200,'
           '170400,170600,190400,190600')
