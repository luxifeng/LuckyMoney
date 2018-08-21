# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: xueqiu_user_info.py
@time: 2018/05/19
"""
import random
import pymysql
import requests
from scripts import constants as ct
import sys

# 增加递归深度，否则会因为递归深度超过默认而抛出异常
# 事实上在我的电脑上即使设置1000000，当递归深度超过1300+时就会异常退出
sys.setrecursionlimit(1000000)

# 请求信息
headers = {
    # 请求一次雪球网就会生成cookie
    'Cookie': ct.constant.COOKIE,
    # 浏览器用户代理
    'User-Agent': random.choice(ct.constant.AGENTS)
}

# 请求地址
xueqiu_url_follow = "https://xueqiu.com/friendships/groups/members.json?uid=%s&page=%s&gid=0"  # 关注人请求地址
xueqiu_url_fans = "https://xueqiu.com/friendships/followers.json?uid=%s&pageNo=%s"  # 粉丝请求地址

# 数据库连接
conn = pymysql.connect(host='localhost', user='root', password='123456', db='xueqiu', port=3306, charset='utf8')
cur = conn.cursor()

# sql语句
sql_user_insert = "INSERT INTO xueqiu_users (user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile) VALUES ('%s','%s','%s',%s,%s,'%s','%s','%s','%s');"
sql_user_query = "SELECT user_id FROM xueqiu_users"

# 已访问用户
visited_user = []


# 保存到数据库
def save_user_data_2_mysql(user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile):
    sql = sql_user_insert % (
        user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile)
    print(sql)
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        cur.close()  # 释放游标
        conn.close()  # 释放资源
        raise e


# 查询数据库，得到数据库已存在的用户id
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


# 解析user json数据
def parse_user_json(users_json, count):
    if len(users_json) == 0:
        return
    for user in users_json:
        # 提取必要字段
        user_id = user['id']
        description = user['description']
        if description is not None:
            description = description.replace('\\', '')
        screen_name = user['screen_name']
        if screen_name is not None:
            screen_name = screen_name.replace('\\', '')
        friends_count = int(user['friends_count'])
        followers_count = int(user['followers_count'])
        province = user['province']
        city = user['city']
        gender = user['gender']
        profile = user['profile']
        # 若未访问，则加入数据库，并寻找该id的关注人和粉丝
        if str(user_id) not in visited_user:
            save_user_data_2_mysql(user_id, description, screen_name, friends_count, followers_count, province, city,
                                   gender, profile)
            visited_user.append(str(user_id))
            get_user_data(user_id, count + 1)


# 根据user_id获取取用户的关注人和粉丝列表
def get_user_data(user_id, count):
    # 限制递归层数
    if count > 1000:
        return
    print('迭代第%s层' % count)
    # 拿到关注人
    page_num = 1  # 访问页码
    page_max = 1  # 最大可访问页码
    while page_num <= page_max:
        # 访问地址
        url_follow = xueqiu_url_follow % (user_id, page_num)
        # 请求返回的是json格式文本
        response_follow = requests.get(url_follow, headers=headers).json()
        page_max = int(response_follow['maxPage'])
        follow_page_n = response_follow['users']
        # 解析json
        parse_user_json(follow_page_n, count)
        page_num += 1

    # 拿到粉丝
    page_num = 1  # 访问页码
    page_max = 1  # 最大可访问页码
    while page_num <= page_max:
        url_fans = xueqiu_url_fans % (user_id, page_num)
        response_fans = requests.get(url_fans, headers=headers).json()
        page_max = int(response_fans['maxPage'])
        fans_page_n = response_fans['followers']
        parse_user_json(fans_page_n, count)
        page_num += 1


if __name__ == '__main__':
    # 先从数据取到已存在的用户，避免重复访问
    query_user_data_from_mysql()
    print(len(visited_user))
    # 设置一个种子id，该id最好能广泛关注大V或被粉丝广泛关注
    get_user_data('1955602780', 1)
    # 释放游标
    cur.close()
    # 释放资源
    conn.close()
