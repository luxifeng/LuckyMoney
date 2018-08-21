#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: xueqiu_zh.py
@time: 2018/05/20
"""

import random
import pymysql
import requests
from scripts import constants as ct

# 请求信息
headers = {
    'Cookie': 'bid=da3ae7d16ca9cb3aeb19faaf825aa615_jh96y4qc;device_id=2e19e87a056acd56fcd5b22f53e14a29;remember=1;remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y;s=e811tpeu81;snbim_minify=true;u=1536976596;u.sig=Mkg4DlLstcPwxcz_ISfoVaTdUpQ;xq_a_token=c33166a172a010e40e47f196c4d314b573ad5d84;xq_a_token.sig=2Td6XL1jgPwRmOvYilR5Le2jSYI;xq_is_login=1;xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q;xq_r_token=5c4a8ac90cbc860229818cc46e4ef470dd0cd2ca;xq_r_token.sig=a0sJ23EUQuUf38NJFG143HPgh2M',
    'User-Agent': random.choice(ct.constant.AGENTS)
}
# 请求地址
xueqiu_url_trade = "https://xueqiu.com/v4/statuses/user_timeline.json?page=%s&user_id=%s&source=买卖"
# 数据库连接
conn = pymysql.connect(host='localhost', user='root', password='123456', db='xueqiu', port=3306, charset='utf8')
cur = conn.cursor()
# sql语句
sql_trade_insert = "INSERT INTO xueqiu_users (user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile) VALUES ('%s','%s','%s',%s,%s,'%s','%s','%s','%s');"
# 已访问用户
global visited_user
visited_user = []


# 保存到数据库
def save_user_data_2_mysql(user_id, description, screen_name, friends_count, followers_count, province, city, gender,
                           profile):
    sql = sql_trade_insert % (user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile)
    print(sql)
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        cur.close()  # 释放游标
        conn.close()  # 释放资源
        raise e

# 提取
def extrace_trade_data(trade):
    trade_id = trade['id']
    create_time = trade['created_at']
    retweet_count = int(trade['retweet_count'])
    reply_count = int(trade['retweet_count'])
    fav_count = int(trade['retweet_count'])
    description = trade['description'].replace("\\", "")
    source = trade['source ']

    return

# 提取交易json结构
def parse_trade_json(trade_json):
    if len(trade_json) == 0:
        return
    for trade in trade_json:
        extrace_trade_data(trade)

# 每个用户交易行为
def get_user_trade(user_id):
    pageNum = 1;
    pageMax = 1;
    while(pageNum <= pageMax):
        url_trade = xueqiu_url_trade % (pageNum, user_id)
        requests_trade = requests.get(url_trade, headers = headers).json()
        pageMax = requests_trade['maxPage']
        trades_page_n = requests_trade['statuses']
        parse_trade_json(trades_page_n)
        pageNum += 1


# 查询数据库
def query_user_data_from_mysql():
    try:
        cur.execute(sql_user_query)
        rows = cur.fetchall()
        for r in rows:
            visited_user.append(str(r[0]))
    except Exception as e:
        cur.close()  # 释放游标
        conn.close()  # 释放资源
        raise e

