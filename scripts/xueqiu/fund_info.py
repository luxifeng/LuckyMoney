#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: fund_info.py
@time: 2018/08/02
"""


import random
import pymysql
import requests
from scripts import constants as ct
import sys

# 请求信息
headers = {
    # 请求一次雪球网就会生成cookie
    'Cookie': ct.constant.COOKIE,
    # 浏览器用户代理
    'User-Agent': random.choice(ct.constant.AGENTS)
}

# 请求地址
url_fund_list = "https://xueqiu.com/private_fund/v3/rank/list.json?order_by=PROFIT&typical=&strategy=&is_open=&fund_type=&period=all&profit_range=0&max_drawdown_range=0"  # 关注人请求地址
url_fund_hist = "https://xueqiu.com/private_fund/nav_daily/day.json?symbol=%s&period=all"

# 历史收益
def writeRes(private, public, manager_nick_name):
    fund_sym = private['symbol']
    fund_name = private['name']
    fund_hist = private['list']
    index_name = public['symbol']
    index_hist = public['list']

    # if (fund_hist[0])['date'] > '2017-08-15':
    #     return

    try:
        f = open("D:/workspace/StockIndex/data/xueqiu_fund/%s_&&_%s_&&_%s.csv" % (manager_nick_name, fund_sym, fund_name), 'w')
        header = "date,fund_value,fund_percent,index_value,index_percent"
        f.writelines(header + "\n")

        for i in range(len(fund_hist)):
            item1 = fund_hist[i]
            item2 = index_hist[i]
            time = item1['date']
            value1 = item1['value']
            percent1 = item1['percent']
            value2 = item2['value']
            percent2 = item2['percent']
            line = "%s,%s,%s,%s,%s\n" % (time, value1, percent1, value2, percent2)
            f.writelines(line)


        f.close()

    except FileNotFoundError:
        print("文件不存在")
    except PermissionError:
        print("无权操作该文件")

# 私募list
def parse_fund_json(fund_json):
    if len(fund_json) == 0:
        return
    for fund in fund_json:
        # 提取必要字段
        sysbol = fund['symbol']
        name = fund['name']
        manager_nick_name = fund['manager_nick_name']
        new_url = url_fund_hist % (sysbol)
        one_page = requests.get(new_url, headers=headers).json()
        private = one_page[0]
        public = one_page[1]
        writeRes(private, public, manager_nick_name)

# 根据user_id获取取用户的关注人和粉丝列表
def get_fund_data():
    # 请求返回的是json格式文本
    response_fund = requests.get(url_fund_list, headers=headers).json()
    fund_data = response_fund['data']
    parse_fund_json(fund_data)

if __name__ == '__main__':
    get_fund_data()