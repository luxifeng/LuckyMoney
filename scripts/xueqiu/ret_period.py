# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: ret_period.py
@time: 2018/08/22
"""
import os
import pandas as pd

dir_path = 'D:/workspace/StockIndex/data/xueqiu_fund_bak/'

# 判断基金收益是周公布还是月公布
if __name__ == '__main__':
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_name = str(file)
            path = dir_path + file_name
            data = pd.read_csv(path, encoding='utf-8', sep=",", header=0, engine='python')
            print(data['date'])
            value = input('input a int:')
            os.rename(dir_path + file_name, dir_path + value + "_&&_" + file_name)
