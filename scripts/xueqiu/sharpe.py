# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: sharpe.py
@time: 2018/08/19
"""

import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt

dir_path = 'D:/workspace/StockIndex/data/xueqiu_fund_bak/'
day_per_year = 252
week_per_year = 50
month_per_year = 12
no_risk_ratio = 0.015 # 一年定期利率

def calSharpeRatio(file, period):
    # 读取sheet1中的内容，存放在data中，数据类型为DataFrame
    path = dir_path + file
    data = pd.read_csv(path, encoding='utf-8', sep=",",header=0,engine='python')
    if data['date'].min() > '2018-01-31':
        return
    ret_rate = (data['fund_value'] - data['fund_value'].shift(1)) / data['fund_value'].shift(1)
    # 年化收益率 =[（投资内收益 / 本金）/ 投资天数] * 365 ×100%
    year_ret = ret_rate.mean() * period
    # 年化波动率 = 周收益率标准差*sqrt(50)
    std = ret_rate.std()
    volatility = std * np.sqrt(period)
    # 年化夏普
    sharperatio = (year_ret - no_risk_ratio) / volatility
    # 最大回撤
    down = (data['fund_value'].min() - data['fund_value'].max()) / data['fund_value'].min()
    fund_name = file.split('_&&_')[1]
    fund_code = file.split('_&&_')[2]
    fund_manager = file.split('_&&_')[3].replace('.csv', '')
    print('%s,%s,%s,%s,%s,%s,%s' % (fund_name, fund_code, fund_manager, round(sharperatio, 3), round(year_ret, 7), round(volatility, 3), round(down, 7)))


if __name__ == '__main__':
    print('基金名字,基金代码,主理人,夏普比率,收益率,波动率,最大回撤率')
    # 获取私募代码列表
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_name = str(file)
            type = file_name.split('_&&_')[0]
            if type is 'd':
                calSharpeRatio(file_name, day_per_year)
            elif type is 'w':
                calSharpeRatio(file_name, week_per_year)
            elif type is 'm':
                calSharpeRatio(file_name, month_per_year)
