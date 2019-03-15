# -*- coding:utf-8 -*-
"""
市场层面信息
主要是获取交易日

@author: Lucy
@file: market.py
@time: 2018/01/28
"""

from datetime import datetime
from util.tsutil import tsutil
from util.dateutil import dateutil

class MarketInfo:

    def get_all_trade_date(self):
        """
        获取交易日期，2000年1月1日至今
        """
        now = dateutil.datetime_to_tsformat(datetime.now())
        try:
            trade_date = tsutil.query_trade_date('20000101', now)
            return trade_date
        except Exception as e:
            print(e)

    def is_trade_date(self, my_date):
        """
        判断是否交易日
        :param date: datetime or str
        """
        if isinstance(my_date, datetime):
            ndate = dateutil.datetime_to_tsformat(my_date)
        elif isinstance(my_date, str):
            ndate = my_date
        else:
            return False
        try:
            res = tsutil.query_trade_date(start_date=ndate, end_date=ndate)
            if res['is_open'].iloc[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
