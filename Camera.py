from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='pytz')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='pytz')

# 拍照
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
        time.sleep(3)
        # 获得最新的一张照片的文件名
        picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
        name_list = picture_url.split("\n")
        myfilename = name_list[1]
        time.sleep(1)
        # 指定要保存到的目标文件夹路径
        target_folder = "./picture/"
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
        return myfilename
    except Exception as e :
        print(F"Error{e}")

# def photo_time():
#     pass




def func() :
    # 创建调度器BlockingScheduler()
    scheduler = BlockingScheduler()

    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '08', minute = '22', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '22', minute = '00', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '22', minute = '04', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '22', minute = '34', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '22', minute = '36', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '23', minute = '04', second = '00',timezone="Asia/Shanghai")
    scheduler.add_job(camera, 'cron', day_of_week = None, hour = '23', minute = '06', second = '00',timezone="Asia/Shanghai")
    scheduler.start()

if __name__ == '__main__' :
    func()