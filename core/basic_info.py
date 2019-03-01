# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: get_stock_list.py
@time: 2018/01/28
"""

import tushare as ts
import pandas as pd
from datetime import datetime
from core.constants import const

class BasicInfo():
    """
    basic info of market, including stock list, trade date and so on
    """

    def __init__(self):

    def get_stock_list(self):
        # pro token
ts.set_token(const.TS_TOKEN)

# init api
pro = ts.pro_api()

# get stock listed
fields = 'ts_code,symbol,name,area,industry,market,list_status,list_date,delist_date,is_hs'
stock_list = pro.stock_basic(fields=fields)

# to data frame
df = pd.DataFrame(stock_list)

# save path
path = const.DIR_STOCK_LIST + datetime.now().strftime("%Y-%m-%d") + ".csv"
df.to_csv(path, header=True, index=False)
