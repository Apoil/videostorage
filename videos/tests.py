from django.shortcuts import render
from django.test import TestCase
import os
import platform
import ctypes
import sys
import psutil
import json

def get_free_space_mb(folder):
    """
    获取磁盘剩余空间
    :param folder: 磁盘路径 例如 D:\\
    :return: 剩余空间 单位 G
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 // 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 // 1024


"""
current_directory = os.path.dirname(os.path.abspath(__file__))获取当前路径
print(current_directory)
print(get_free_space_mb(current_directory),'GB')
"""

def used_disk():
    '''
    获取当前文件所在磁盘容量信息
    '''
    #获取磁盘使用情况
    disk_usage = psutil.disk_usage('/')
    #获取磁盘的总容量
    total = disk_usage.total / (1024.0 ** 3)
    #获取磁盘已使用的容量
    used = disk_usage.used / (1024.0 ** 3)
    #获取磁盘可用的容量
    free = disk_usage.free / (1024.0 ** 3)
    #print输出磁盘使用情况
    print('总容量:',total,'GB','已用:',used,'GB','空余:',free,'GB')
    disk={'total':total,'used':used,'free':free}
    print(disk)
    print(disk['total'])


def used_disk1():
    disk_usage = psutil.disk_usage('/')
    total = disk_usage.total / (1024.0 ** 3)
    used = disk_usage.used / (1024.0 ** 3)
    free = disk_usage.free / (1024.0 ** 3)
    
    # 手动序列化为JSON格式
    disk_info = json.dumps({
        'total': total,
        'used': used,
        'free': free
    })
    print(disk_info)



