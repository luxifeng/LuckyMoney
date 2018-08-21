# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: mysql_2_mongodb.py
@time: 2018/05/24
"""

import pymysql

# 数据库连接
mysql_conn = pymysql.connect(host='localhost', user='root', password='123456', db='xueqiu', port=3306, charset='utf8')
cur = mysql_conn.cursor()

mysql_conn_remote = pymysql.connect(host='207.246.101.37', user='xueqiu_user', password='feng123456', db='xueqiu', port=3306, charset='utf8')
cur_remote = mysql_conn_remote.cursor()
# 变量
variable = ["user_id", "description", "screen_name", "friends_count", "followers_count", "province", "city", "gender", "profile"]
split_num = 10000

# sql语句
sql_user_query = "SELECT user_id,description,screen_name,friends_count,followers_count,province,city,gender,profile FROM xueqiu_users where id >= %s and id < %s"
sql_user_insert = "INSERT INTO xueqiu_users (user_id, description, screen_name, friends_count, followers_count, province, city, gender, profile) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
sql_user_count = "SELECT max(id) from xueqiu_users"


def query_user_count_from_mysql():
    try:
        cur.execute(sql_user_count)
        rows = cur.fetchone()
        return int(rows[0])
    except Exception as e:
        cur.close()  # 释放游标
        cur_remote.close()  # 释放游标
        mysql_conn.close()  # 释放资源
        mysql_conn_remote.close()  # 释放资源
        raise e


# 查询数据库，得到数据库已存在的用户id
def query_user_data_from_mysql(num):
    start = 0
    end = start + split_num
    while(start <= num):
        try:
            if end > num:
                end = num + 1
            print(sql_user_query % (start, end))
            cur.execute(sql_user_query % (start, end))
            rows = cur.fetchall()
            rec_list = []
            for r in rows:
                one_rec = []
                for k in range(len(variable)):
                    one_rec.append(r[k])
                rec_list.append(one_rec)
            cur_remote.executemany(sql_user_insert, rec_list)
            mysql_conn_remote.commit()

            start = end
            end = start + split_num
        except Exception as e:
            cur.close()
            mysql_conn.close()
            cur_remote.close()
            mysql_conn_remote.close()
            raise e


if __name__ == '__main__':
    num = query_user_count_from_mysql()
    query_user_data_from_mysql(num)
    cur.close()  # 释放游标
    cur_remote.close()  # 释放游标
    mysql_conn.close()  # 释放资源
    mysql_conn_remote.close()  # 释放资源
