#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: __init__.py.py
@time: 2018/01/28
"""
import time

if __name__ == '__main__':
    timeStamp = 1427349630000
    timeStamp /= 1000.0
    print(timeStamp)
    timearr = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
    print(otherStyleTime)