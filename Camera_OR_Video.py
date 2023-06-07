from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time
from Read_Phone_Camera_Config import Read_Phone_Camera_Config


from Send_Email import Send_Email
from Webhook_send_msg import Wenhook_send, Wenhook_send_1

data = Read_Phone_Camera_Config()
target_folder = data['target_folder']


# 调用手机相机拍照或录屏并上传
def Camera_OR_Video(camera_or_video=0, wait_time=10):
    try:
        # 点亮手机
        os.system("adb shell input keyevent 224")
        time.sleep(1)
        # 解锁屏幕（前提需要在设置里面把手机登录的密码这些都关掉）
        os.system("adb shell input keyevent 82")
        time.sleep(1)
        if camera_or_video == 0:
            print("开始拍照")
            # 启动相机
            os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
            # 多留点时间自动对焦
            time.sleep(3)
            # 按键27拍照
            os.system("adb shell input keyevent 27")
            # 留点时间存储照片防止读取到上一张图片
            time.sleep(5)
            # 获得最新的一张照片的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[1]
        elif camera_or_video == 1:
            print('开始录像')
            os.system("adb shell am start -a android.media.action.VIDEO_CAPTURE")
            # 多留点时间自动对焦
            time.sleep(2)
            # 开始录屏
            os.system("adb shell input keyevent 27")
            # 录屏时间
            time.sleep(wait_time)
            # 结束录屏
            os.system("adb shell input keyevent 27")
            time.sleep(5)
            os.system("adb shell input tap 900 102")
            time.sleep(10)
            # 获得最新的一张视频的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[0]
        else:
            print("输入的内容错误，执行拍照操作")
            print("开始拍照")
            # 启动相机
            os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
            # 多留点时间自动对焦
            time.sleep(3)
            # 按键27拍照
            os.system("adb shell input keyevent 27")
            # 留点时间存储照片防止读取到上一张图片
            time.sleep(5)
            # 获得最新的一张图片的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            # print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[1]
        print("图片名称{}".format(myfilename))
        time.sleep(1)
        # 指定要保存到的目标文件夹路径,构建adb命令
        adb_code = "adb pull /storage/emulated/0/DCIM/Camera/" + myfilename + " " + target_folder
        # 执行adb命令
        os.system(adb_code)
        time.sleep(1)
        # back键 暂退相机
        os.system("adb shell input keyevent 4")
        time.sleep(1)
        # Power键 黑屏
        os.system("adb shell input keyevent 26")
        # time.sleep(2)
        # # 调用邮件发送图片至邮箱
        # Send_Email(myfilename)
        # time.sleep(2)
        # # 企业微信推送图片
        # Wenhook_send(myfilename)
        # time.sleep(2)
        # Wenhook_send_1(myfilename)
        return myfilename
    except Exception as e:
        print(F"Error{e}")

Camera_OR_Video(camera_or_video=0, wait_time=10)




# 处理时间
def photo_time(times=None):
    times = times.split(",")
    scheduler = BlockingScheduler()
    for i in times:
        scheduler.add_job(Camera_OR_Video(), 'cron', day_of_week=None, hour=i[0:2:], minute=i[2:4:], second=i[4:6:],
                          timezone="Asia/Shanghai")
    scheduler.start()
