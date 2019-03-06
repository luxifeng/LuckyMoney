# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: date_util.py
@time: 2019/03/03
"""

import calendar
from common.constant import const
from _datetime import datetime, timedelta


def get_first_day_of_next_month(date):
    """
    获取下个月的第一天
    :param date: datetime
    """
    if isinstance(date, datetime):
        first_day = datetime(date.year, date.month, 1)
        days_num = calendar.monthrange(first_day.year, first_day.month)[1]
        first_day_of_next_month = first_day + timedelta(days=days_num)
        return first_day_of_next_month
    raise Exception("Unexpected data type")


def get_next_day(date):
    """
    获取下一天
    :param date: datetime / str
    """
    if isinstance(date, datetime):
        next_day = date + timedelta(days=1)
        return next_day
    if isinstance(date, str):
        date_tmp = yyyymmdd_to_datetime(date)
        next_day = date_tmp + timedelta(days=1)
        return datetime_to_yyyymmdd(next_day)
    raise Exception("Unexpected data type")


def datetime_to_yyyymmdd(date):
    """
    date转yyyymmdd str
    :param date: datetime
    """
    if isinstance(date, datetime):
        return date.strftime(const.DATE_FORMAT_TUSHARE)
    raise Exception("Unexpected data type")


def yyyymmdd_to_datetime(yyyymmdd):
    """
    yyyymmdd str转datetime
    :param date: datetime
    """
    if isinstance(yyyymmdd, str):
        return datetime.strptime(yyyymmdd, const.DATE_FORMAT_TUSHARE)
    raise Exception("Unexpected data type")
