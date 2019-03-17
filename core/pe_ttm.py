# -*- coding:utf-8 -*-
"""
最后的目标！
计算指数pe ttm！

计算公式：
pe_ttm = 总市值 / 最近4个季度净利润之和
总市值 = 股价 * 总股本

@author: Lucy
@file: pe_ttm.py
@time: 2019/03/15
"""

import pandas as pd
from datetime import datetime
from core.market import MarketInfo
from util.dateutil import dateutil
from util.dbutil import dbutil
from util.tsutil import tsutil


class PEInfo:

    def _cal_index_pe_ttm(self, index_comp, stock_price, stock_profit):
        """
        计算指数pe-ttm
        :return:
        """


    def save_index_pe_ttm(self, start_date, end_date):
        """
        保存指数pe-ttm
        :param start_date: str
        :param end_date: str
        """
        sql_stock_price = 'SELECT ts_code, trade_date, close, total_share FROM stock_price WHERE trade_date=\'%s\''
        sql_index_comp = 'SELECT index_code, con_code, trade_date, weight FROM index_comp WHERE trade_date <= '
        date_iterator = end_date
        mi = MarketInfo()
        all_trade_date = mi.get_all_trade_date()
        trade_date_dict = {}
        for row in all_trade_date.iterrows():
            trade_date_dict[row[1]['cal_date']] = row[1]['is_open']
        while int(date_iterator) >= int(start_date):
            is_open = trade_date_dict.get(date_iterator, 0)
            if is_open == 0:
                print("Not a trade date: %s" % date_iterator)
            else:
                sql_stock_price_cur = sql_stock_price % dateutil.tsformat_to_dbformat(date_iterator)
                stock_price = dbutil.read_df(sql_stock_price_cur)

            date_iterator = dateutil.datetime_to_tsformat(dateutil.get_last_day(date_iterator))
