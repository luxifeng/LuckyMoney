# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: user_info.py
@time: 2018/08/19
"""

import random
import requests
from scripts import constants as ct
import os
import pymysql
import time
import datetime

# 请求信息
headers = {
    # 请求一次雪球网就会生成cookie
    'Cookie': ct.constant.COOKIE,
    # 浏览器用户代理
    'User-Agent': random.choice(ct.constant.AGENTS)
}

# 请求地址
url_fund_link = "https://xueqiu.com/S/%s"  # 私募地址
url_user_link = "https://xueqiu.com/u/%s"  # 用户地址
url_user_post = "https://xueqiu.com/v4/statuses/user_timeline.json?page=%s&user_id=%s"  # 帖子
url_user_zh = "https://xueqiu.com/cubes/list.json?user_id=%s"  # 组合
url_user_follow = "https://xueqiu.com/friendships/followers.json?uid=%s&pageNo=1"

# database
mysql_conn_remote = pymysql.connect(host='207.246.101.37',
                                    user='xueqiu_user',
                                    password='feng123456',
                                    db='xueqiu',
                                    port=3306,
                                    charset='utf8',
                                    connect_timeout = 36000)
cur_remote = mysql_conn_remote.cursor()
sql_user_query = "SELECT user_id FROM xueqiu_users where screen_name='%s'"


def get_user_info(user_code):
    response_post_first = requests.get(url_user_post % (1, user_code), headers=headers).json()
    maxPage = response_post_first['maxPage']
    f = open("D:/workspace/StockIndex/data/xueqiu_user/post/%s.csv" % (user_code), 'w')
    try:
        header = "create_time,edit_time,retweet_count,reply_count,like_count,truncated,page\n"
        f.writelines(header)
        for index in range(1, maxPage + 1):
            if user_code == '4206051491' and index <= 655:
                continue
            time.sleep(10)
            print(user_code, ": page =", index, ", time =", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            response_post = requests.get(url_user_post % (index, user_code), headers=headers, timeout = 120).json()
            post_list = response_post['statuses']
            for post in post_list:
                create_time = ''
                edit_time = ''
                if post['created_at'] is not None:
                    create_timestamp = int(post['created_at']) / 1000.0  # 创建时间
                    timearr = time.localtime(create_timestamp)
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
                if post['edited_at'] is not None:
                    edit_timestamp = int(post['edited_at']) / 1000.0  # 编辑时间
                    timearr = time.localtime(edit_timestamp)
                    edit_time = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
                retweet_count = post['retweet_count']  # 转发
                reply_count = post['reply_count']  # 回复
                like_count = post['like_count']  # 赞
                truncated = post['truncated']
                line = "%s,%s,%s,%s,%s,%s,%s\n" % (create_time, edit_time, retweet_count, reply_count, like_count, truncated,index)
                f.writelines(line)
    except FileNotFoundError:
        print("文件不存在")
    except PermissionError:
        print("无权操作该文件")
    except KeyError:
        print("××× key error:" + user_code)
    finally:
        f.close()
    return


def get_fund_data(manager, fund_code):
    response_fund = requests.get(url_fund_link % fund_code, headers=headers).text
    follower_count_ind = response_fund.find('follower_count')
    left_bracket_index = response_fund.find(':', follower_count_ind)
    right_bracket_index = response_fund.find(',', follower_count_ind)
    follower_count = response_fund[(left_bracket_index + 1):right_bracket_index]
    response_follow = requests.get(url_user_follow % manager, headers=headers).json()
    user_follow = response_follow['count']
    try:
        f = open("C:/Users/Lucy/res.csv", 'a')
        f.writelines("%s,%s,%s,%s\n" % (fund_code, follower_count, manager, user_follow))
        f.close()
    except:
        print("error!!!")
    get_user_info(manager)


if __name__ == '__main__':
    # 获取私募代码列表
    try:
        # mysql_conn_remote.connect_timeout = 36000
        for root, dirs, files in os.walk("D:/workspace/StockIndex/data/xueqiu_fund"):
            for file in files:
                manager_names = str(file).split("_&&_")
                manager_name = manager_names[0]
                fund_code = str(file).split("_&&_")[1]
                cur_remote.execute(sql_user_query % manager_name)
                rows = cur_remote.fetchall()
                rec_list = []
                for r in rows:
                    rec_list.append(r[0])
                if len(rec_list) == 0:
                    print("找不到%s!" % manager_name)
                else:
                    if not os.path.exists("D:/workspace/StockIndex/data/xueqiu_user/post/%s.csv" % (rec_list[0])):
                        get_fund_data(rec_list[0], fund_code)
    finally:
        cur_remote.close()
