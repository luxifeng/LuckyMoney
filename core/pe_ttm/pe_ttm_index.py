#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: cal_index_pe.py
@time: 2018/01/28
"""

import tushare as ts
import pandas as pd

## 选择指数
index_list = ['000016', '000017']
date = '2005-01-01'

## 根据指数代码获取指数成分股
def get_constituent_stocks(index_code, date): # TODO
    file_path = "./data/constitute/" + index_code + '.txt'
    file_object = open(file_path, 'r')
    lines = file_object.readlines()
    stocks = []
    for line in lines:
        stocks.append(line.strip())
    return stocks

## 根据个股代码计算个股PE = 股价/每股收益
def cal_stock_pe(stock_code):

    final_stock_pe = 0
    return final_stock_pe

## 计算指数PE = n/Σ(1/PE)
def cal_index_pe(constituent_stocks, date):
    sum_stock_pe = float(0)
    for stock_code in enumerate(constituent_stocks):
        temp_pe = cal_stock_pe(stock_code, date)
        sum_stock_pe += 1 / temp_pe

    num_of_stocks = len(constituent_stocks)
    if num_of_stocks > 0:
        final_index_pe = num_of_stocks / sum_stock_pe
        return final_index_pe
    else:
        return float('NaN')


for index_code in enumerate(index_list):
    ## 获取指数成分股
    constituent_stocks = get_constituent_stocks(index_code, date)
    ## 计算当日指数PE
    index_pe = cal_index_pe(constituent_stocks, date)
    ## 写文件
    file_path = "./data/pe/" + index_code + '.csv'
    file_object = open(file_path, 'w+')
    file_object.write(date + ',' + index_pe + '\n')
    file_object.close()

