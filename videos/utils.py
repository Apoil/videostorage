import cv2
import os
import random
from datetime import datetime
from django.core.files import File
from tempfile import NamedTemporaryFile

def ensure_tmp_dir_exists():
    """确保/tmp目录存在，如果不存在则创建它"""
    tmp_dir = '/tmp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

def save_video_first_frame(video_file):
    ensure_tmp_dir_exists()  # 确保/tmp目录存在

    # 使用 OpenCV 读取视频文件
    vc = cv2.VideoCapture(video_file.temporary_file_path())  # 获取临时文件路径
    if vc.isOpened():
        # 设置视频的起始位置到第1秒
        fps = vc.get(cv2.CAP_PROP_FPS)  # 获取帧率
        frame_number = int(fps*240)  # 第240秒的帧数
        vc.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  # 设置视频到第1秒的位置

        rval, frame = vc.read()  # 读取这一秒的第一帧
        if rval:
            screenshot_name = 'shot_' + str(random.randint(1, 9999)) + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
            screenshot_path = os.path.join('/tmp', screenshot_name)
            cv2.imwrite(screenshot_path, frame)  # 存储为图像
            vc.release()

            # 使用 NamedTemporaryFile，不带 delete 参数
            with NamedTemporaryFile(suffix='.jpg', mode='wb', delete=False) as cover_temp:
                cover_temp_path = cover_temp.name
                with open(screenshot_path, 'rb') as f:
                    cover_temp.write(f.read())
                cover_temp.flush()

            # 返回 Django 的 File 对象，并使用临时文件路径
            return File(open(cover_temp_path, 'rb'), name=screenshot_name)

    vc.release()
    return None
