# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: dateutil.py
@time: 2019/03/03
"""

import calendar
import pandas as pd
from datetime import datetime, timedelta, date

DATE_FORMAT_TUSHARE = '%Y%m%d'
DATE_FORMAT_DB = '%Y-%m-%d'


def get_first_day_of_next_month(my_date):
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


def get_last_day(my_date):
    """
    获取上一天
    :param my_date: datetime / str
    """
    if isinstance(my_date, datetime):
        next_day = my_date + timedelta(days=-1)
        return next_day
    if isinstance(my_date, str):
        date_tmp = tsformat_to_datetime(my_date)
        next_day = date_tmp + timedelta(days=-1)
        return next_day
    raise Exception("Unexpected data type")


def get_next_day(my_date):
    """
    获取下一天
    :param my_date: datetime / str
    """
    if isinstance(my_date, datetime):
        next_day = my_date + timedelta(days=1)
        return next_day
    if isinstance(my_date, str):
        date_tmp = tsformat_to_datetime(my_date)
        next_day = date_tmp + timedelta(days=1)
        return next_day
    raise Exception("Unexpected data type")


def datetime_to_tsformat(my_date):
    """
    date转yyyymmdd str
    :param my_date: datetime
    """
    if isinstance(my_date, (datetime, date)):
        return my_date.strftime(DATE_FORMAT_TUSHARE)
    raise Exception("Unexpected data type")


def datetime_to_dbformat(my_date):
    """
    date转yyyy-mm-dd str
    :param my_date: datetime
    """
    if isinstance(my_date, (datetime, date)):
        return my_date.strftime(DATE_FORMAT_DB)
    raise Exception("Unexpected data type")


def tsformat_to_datetime(my_date):
    """
    yyyymmdd str转datetime
    :param my_date str
    """
    if isinstance(my_date, str):
        return datetime.strptime(my_date, DATE_FORMAT_TUSHARE)
    raise Exception("Unexpected data type")


def dbformat_to_datetime(my_date):
    """
    yyyy_mm_dd str转datetime
    :param my_date: str
    """
    if isinstance(my_date, str):
        return datetime.strptime(my_date, DATE_FORMAT_DB)
    raise Exception("Unexpected data type")


def tsformat_to_dbformat(my_date):
    """
    yyyymmdd -> yyyy-mm-dd
    :param my_date:
    :return:
    """
    if isinstance(my_date, str):
        return datetime_to_dbformat(tsformat_to_datetime(my_date))
    raise Exception("Unexpected data type")


def dbformat_to_tsformat(my_date):
    """
    yyyy-mm-dd -> yyyymmdd
    :param my_date:
    :return:
    """
    if isinstance(my_date, str):
        return datetime_to_tsformat(dbformat_to_datetime(my_date))
    raise Exception("Unexpected data type")


def tsformat_col_to_datetime(col):
    return pd.to_datetime(col, format=DATE_FORMAT_TUSHARE, errors='coerce')


def datetime_col_to_tsformat(col):
    return col.apply(lambda x: datetime.strftime(x, DATE_FORMAT_TUSHARE))


def tuple_to_date(my_tuple):
    """
    tuple构建日期
    :param my_tuple:
    :return:
    """
    if isinstance(my_tuple, tuple) and len(my_tuple) >= 3:
        my_date = date(my_tuple[0], my_tuple[1], my_tuple[2])
        return my_date
    raise Exception("Unexpected data type")


def tsformat_compare(my_date_1, my_date_2):
    """
    比较日期大小
    :param my_date_1: str
        yyyymmdd
    :param my_date_2: str
        yyyymmdd
    :return: int
        大于：1
        等于：0
        小于：-1
    """
    a = int(my_date_1)
    b = int(my_date_2)
    if a > b:
        return 1
    elif a == b:
        return 0
    else:
        return -1