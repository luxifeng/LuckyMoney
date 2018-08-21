#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: get_today_data.py
@time: 2018/01/28
"""

import datetime
import tushare as ts
import pandas as pd
from scripts import constants as ct

today = datetime.date.today().strftime('%Y-%m-%d')

# 读取股票列表
path = ct.constant.STOCK_LIST_FILE_DIR + today + ct.constant.STOCK_LIST_FILE_TYPE
f = open(path, 'r')
stock_list = f.readlines()
f.close()


# 获取所有股票交易数据
for stock in stock_list:
    stock = stock.strip('\n')
    print('获取' + stock + '数据中...')
    df = ts.get_k_data(stock, ktype = 'D', start = today)
    if df.empty:
        print('数据为空')
        continue
    else:
        print('获取成功')
    df = df[ct.constant.STOCK_DATA_FIELDS]
    stock_path = ct.constant.STOCK_DATA_FILE_DIR + stock + ct.constant.STOCK_DATA_FILE_TYPE
    try:
        stock_file = open(stock_path, 'a')
        df.to_csv(stock_file, header = False)
        stock_file.close()
    except FileNotFoundError:
        print('文件不存在')
    except PermissionError:
        print('无权访问文件')
