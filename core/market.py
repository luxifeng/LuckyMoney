# -*- coding:utf-8 -*-
"""
市场层面信息
主要是获取交易日

@author: Lucy
@file: market.py
@time: 2018/01/28
"""
import xlrd
import util.tsutil as tsu
import util.dateutil as dtu


FIELD_IS_OPEN = 'is_open'
FIELD_CAL_DATE = 'cal_date'


class MarketInfo:

    def __init__(self):
        self._trade_date = {}
        self._delisted_stock = {}

    def load_trade_date(self, start_date, end_date):
        """
        获取日期与是否开市
        :param start_date: str
            起始日期，yyyymmdd，eg: 20180101
        :param end_date: str
            结束日期，yyyymmdd，eg: 20180101
        :return: self
        """
        if start_date is None or end_date is None:
            raise Exception("Date parameter error")
        all_trade_date = tsu.query_trade_date(start_date, end_date)
        self._trade_date.clear()
        for row in all_trade_date.iterrows():
            self._trade_date[row[1][FIELD_CAL_DATE]] = row[1][FIELD_IS_OPEN]
        return self

    def is_trade_date(self, my_date):
        """
        判断是否交易日
        :param my_date: str
            输入日期，yyyymmdd，eg: 20180101
        :return: bool
        """
        if not isinstance(my_date, str):
            return False
        if my_date not in self._trade_date:
            res = tsu.query_trade_date(start_date=my_date, end_date=my_date)
            self._trade_date[my_date] = res[FIELD_IS_OPEN].iloc[0]
        return self._trade_date[my_date] == 1

    def load_delisted_stock(self, file_path):
        """
        获取退市股票与退市日期
        e.g:
        代码	名称	退市日期	终止上市原因	退市时股价(元)	退市时每股净资产(元)	重组后代码	重组后简称	重组后上市日期	退入三板日期	三板代码	三板简称	退市股证券类型	重组后证券类型
        000979.SZ	中弘退	2018-12-28	其他被终止上市的情形	0.2200	0.6749	——	——	——	——	——	——	A股	——
        :param file_path: str
            文件路径
        :return: self
        """
        workbook = xlrd.open_workbook(file_path)
        sheet1 = workbook.sheet_by_index(0)
        row_num = sheet1.nrows
        self._delisted_stock.clear()
        for i in range(1, row_num + 1):
            if sheet1.cell(i, 0).ctype == 0:
                break
            ts_code = sheet1.cell_value(i, 0)
            date_tuple = xlrd.xldate_as_tuple(sheet1.cell_value(i, 2), workbook.datemode)
            delisted_date = dtu.datetime_to_tsformat(dtu.tuple_to_date(date_tuple))
            self._delisted_stock[ts_code] = delisted_date
        return self

    def is_delisted(self, ts_code, curr_date):
        """
        判断该日期是否退市
        :param ts_code: str
        :return: date or None
        """
        delisted_date = self._delisted_stock[ts_code]
        if delisted_date is None:
            return False
        if dtu.tsformat_compare(curr_date, delisted_date) >= 0:
            return True
        return False

