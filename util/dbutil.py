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

    engine = create_engine(const.MYSQL_CONN)

    @classmethod
    def save_df(cls, df, table):
        """
        保存dataframe到数据库
        """
        pd.io.sql.to_sql(df, table, con=cls.engine, if_exists='append', index=False, chunksize=5000)

    @classmethod
    def read_df(cls, sql):
        """
        读取数据库数据到dataframe
        """
        return pd.read_sql_query(sql, con=cls.engine)
