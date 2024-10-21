import psutil  # 进程运行情况
import platform  # 包含系统信息查询函数
import os
import logging
#
# # 硬件信息
svmem = psutil.virtual_memory()
mem_total = svmem.total  # 系统内存总数
mem_used = svmem.used  # 内存已使用
mem_free = svmem.free  # 内存空闲大小
mem_per = svmem.percent  # 内存使用率
system_version = platform.linux_distribution()  # 获取linux发行版本详细信息
system_machine = platform.machine()  # 获取操作系统架构
with open('/proc/cpuinfo') as f:  # 获取cpu型号
    for line in f:
        if line.strip():
            if line.rstrip('\n').startswith('model name'):
                cpu_name = line.rstrip('\n').split(':')[1]
                break
cpu_type = cpu_name.split()[0]
cpu_count = psutil.cpu_count()  # cpu核数
host_name = platform.node()  # 电脑名称
stinfo = os.statvfs('/home')
print('CPU使用率', psutil.cpu_percent(1))
print('每个核的cpu使用率', psutil.cpu_percent(percpu=True))
print('硬盘使用', psutil.disk_usage("/home").percent)
# stinfo = os.statvfs('/')
st_info = stinfo.f_bsize * stinfo.f_blocks / 1024 / 1024 / 1024  # 获取磁盘大小
st_free_info = stinfo.f_bavail * stinfo.f_frsize / 1024 / 1024 / 1024  # 磁盘剩余大小
print('系统内存总数', mem_total)
print('内存已使用', mem_used)
print('内存空闲大小', mem_free)
print('内存使用率', mem_per)
print('cpu核数', cpu_count)
print('电脑名称', host_name)
print('获取磁盘大小', st_info)
print('磁盘剩余大小', st_free_info)
# os.system('python3 /home/KL/DigapisKl/mastercontrol/es_search.py')
if mem_per >= 90:
    print(1)
a = '%.2f' % (st_free_info / st_info)
print(a)
