# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: dbutil.py
@time: 2019/03/12
"""

import pandas as pd
from sqlalchemy import create_engine

from common.constant import const


class dbutil:
    # mysql engine
    __engine = create_engine(const.MYSQL_CONN)

    @classmethod
    def connect(cls):
        return cls.__engine


def save_df(df, table, if_exists='append'):
    """
    保存dataframe到数据库
    """
    pd.io.sql.to_sql(df, table, con=dbutil.connect(), if_exists=if_exists, index=False, chunksize=5000)

def read_df(sql):
    """
    读取数据库数据到dataframe
    """
    return pd.read_sql_query(sql, con=dbutil.connect())
