# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: dateutil.py
@time: 2019/03/03
"""

import calendar
import pandas as pd
from common.constant import const
from datetime import datetime, timedelta, date


class dateutil:

    DATE_FORMAT_TUSHARE = '%Y%m%d'
    DATE_FORMAT_DB = '%Y-%m-%d'

    @classmethod
    def get_first_day_of_next_month(cls, my_date):
        """
        获取下个月的第一天
        :param date: datetime
        """
        if isinstance(my_date, (datetime, date)):
            first_day = datetime(my_date.year, my_date.month, 1)
            days_num = calendar.monthrange(first_day.year, first_day.month)[1]
            first_day_of_next_month = first_day + timedelta(days=days_num)
            return first_day_of_next_month
        raise Exception("Unexpected data type: %s", type(my_date))

    @classmethod
    def get_next_day(cls, my_date):
        """
        获取下一天
        :param my_date: datetime / str
        """
        if isinstance(my_date, datetime):
            next_day = my_date + timedelta(days=1)
            return next_day
        if isinstance(my_date, str):
            date_tmp = cls.tsformat_to_datetime(my_date)
            next_day = date_tmp + timedelta(days=1)
            return next_day
        raise Exception("Unexpected data type")

    @classmethod
    def datetime_to_tsformat(cls, my_date):
        """
        date转yyyymmdd str
        :param my_date: datetime
        """
        if isinstance(my_date, datetime):
            return my_date.strftime(cls.DATE_FORMAT_TUSHARE)
        raise Exception("Unexpected data type")

    @classmethod
    def datetime_to_dbformat(cls, my_date):
        """
        date转yyyy-mm-dd str
        :param my_date: datetime
        """
        if isinstance(my_date, datetime):
            return my_date.strftime(const.DATE_FORMAT_ONE)
        raise Exception("Unexpected data type")

    @classmethod
    def tsformat_to_datetime(cls, my_date):
        """
        yyyymmdd str转datetime
        :param my_date str
        """
        if isinstance(my_date, str):
            return datetime.strptime(my_date, const.DATE_FORMAT_TUSHARE)
        raise Exception("Unexpected data type")

    @classmethod
    def dbformat_to_datetime(cls, my_date):
        """
            yyyy_mm_dd str转datetime
            :param my_date: str
            """
        if isinstance(my_date, str):
            return datetime.strptime(my_date, const.DATE_FORMAT_ONE)
        raise Exception("Unexpected data type")

    @classmethod
    def tsformat_col_to_datetime(cls, col):
        return pd.to_datetime(col, format=const.DATE_FORMAT_TUSHARE, errors='coerce')