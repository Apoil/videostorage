import psutil
import csv
def processInfo():
    """
    获取全部进程信息
    :return: list
    """
    filename = open('./进程信息' + '.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(filename, dialect='excel')
    heard = ['进程编号','进程名称','执行路径','当前路径','启动命令','父进程ID','父进程','状态','进程用户名','进程创建时间','终端','执行时间','内存信息','打开的文件','相关网络连接','线程数','线程','环境变量',]
    csv_write.writerow(heard)
    # 定义一个获取进程属性的方法
    def getProperty(process, pro: str):
        try:
            ret = eval('process.' + pro)()
        except Exception as e:
            return ''
        return ret

    pids = psutil.pids()

    output = {}
    for pid in pids:
        print(pid)
        usar = []
        try:
            process = psutil.Process(pid)
            parent = getProperty(process, 'parent')
            if parent is str or parent is None:
                parentName = ''
            else:
                parentName = parent.name()
            output[pid] = {
                '进程编号': pid,
                '进程名称': process.name(),
                '执行路径': getProperty(process, 'exe'),
                '当前路径': getProperty(process, 'cwd'),
                '启动命令': getProperty(process, 'cmdline'),
                '父进程ID': process.ppid(),
                '父进程': parentName,
                '状态': process.status(),
                '进程用户名': getProperty(process, 'username'),
                '进程创建时间': process.create_time(),
                '终端': getProperty(process, 'terminal'),
                '执行时间': process.cpu_times(),
                '内存信息': process.memory_info(),
                '打开的文件': getProperty(process, 'open_files'),
                '相关网络连接': process.connections(),
                '线程数': process.num_threads(),
                '线程': getProperty(process, 'threads'),
                '环境变量': getProperty(process, 'environ'),
            }
            usar.append(output[pid]['进程编号'])
            usar.append(output[pid]['进程名称'])
            usar.append(output[pid]['执行路径'])
            usar.append(output[pid]['当前路径'])
            usar.append(output[pid]['启动命令'])
            usar.append(output[pid]['父进程ID'])
            usar.append(output[pid]['父进程'])
            usar.append(output[pid]['状态'])
            usar.append(output[pid]['进程用户名'])
            usar.append(output[pid]['进程创建时间'])
            usar.append(output[pid]['终端'])
            usar.append(output[pid]['执行时间'])
            usar.append(output[pid]['内存信息'])
            usar.append(output[pid]['打开的文件'])
            usar.append(output[pid]['相关网络连接'])
            usar.append(output[pid]['线程数'])
            usar.append(output[pid]['线程'])
            usar.append(output[pid]['环境变量'])


            print(output[pid]['进程编号'])
            csv_write.writerow(usar)

        except Exception as result:
            print(result)

    return output
a = processInfo()
print(a)
