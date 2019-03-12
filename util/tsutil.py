# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: dateutil.py
@time: 2019/03/03
"""

import tushare as ts

from common.constant import const


class tsutil:

    # pro token
    ts.set_token(const.TS_TOKEN)
    # init api
    pro = ts.pro_api()

    @classmethod
    def query_stock_basic(cls):
        query_stock_basic = 'stock_basic'
        fields_stock_basic = 'ts_code,symbol,name,area,industry,fullname,enname,market,' \
                             'exchange,curr_type,list_status,list_date,delist_date,is_hs'
        return cls.pro.query(query_stock_basic, fields=fields_stock_basic)