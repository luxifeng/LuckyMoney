# -*- coding:utf-8 -*-
"""
市场层面信息

@author: Lucy
@file: market_info.py
@time: 2018/01/28
"""

import logging
import tushare as ts
from datetime import datetime
from common.constant import const

handler = logging.FileHandler(const.FILE_LOG)
fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter) #设置输出内容的格式
logger = logging.getLogger()
logger.setLevel('INFO')
logger.addHandler(handler)

class MarketInfo:

    def __init__(self):
        # pro token
        ts.set_token(const.TS_TOKEN)
        # init api
        self._pro = ts.pro_api()

    def get_all_trade_date(self):
        """
        获取交易日期，2000年1月1日至今
        """
        now = datetime.now().strftime(const.DATE_FORMAT_TUSHARE)
        try:
            trade_date = self._pro.query('trade_cal', exchange='', start_date='20000101', end_date=now)
            return trade_date
        except Exception as e:
            logger.error(e)

    def is_trade_date(self, date):
        """
        判断是否交易日
        :param date: datetime or str
        """
        if isinstance(date, datetime):
            ndate = date.strftime(const.DATE_FORMAT_TUSHARE)
        elif isinstance(date, str):
            ndate = date
        else:
            return False
        res = self._pro.query('trade_cal', exchange='', start_date=ndate, end_date=ndate)
        if res['is_open'].iloc[0] == 1:
            return True
        else:
            return False
