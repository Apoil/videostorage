from __future__ import print_function
import os


def process_list():
    pids = []
    for subdir in os.listdir('/tools'):
        if subdir.isdigit():
            pids.append(subdir)
    return pids


if __name__ == '__main__':
    pids = process_list()
    print('Total number of running processes:: {0}'.format(len(pids)))
