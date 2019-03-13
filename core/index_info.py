# -*- coding:utf-8 -*-
"""
指数层面信息

@author: Lucy
@file: index_info.py
@time: 2019/03/02
"""

import os
import pandas as pd
import time
from datetime import datetime
from common.constant import const
from core.market_info import MarketInfo
from util.dateutil import dateutil
from util.dbutil import dbutil
from util.tsutil import tsutil


class IndexInfo:

    def save_index_list(self, file_path):
        """
        保存中证、上交所、深交所指数列表
        与已存在的数据合并，保持一份最新
        :param file_path: str
            path to save index list
        :return bool
        """
        table_index_list = "index_basic"
        try:
            index_list_csi = tsutil.query_index_list("CSI")
            index_list_sse = tsutil.query_index_list('SSE')
            index_list_szse = tsutil.query_index_list('SZSE')
            index_list = index_list_csi.append([index_list_sse, index_list_szse])
            dbutil.save_df(index_list, table_index_list)
            print("Successfully load index list")
        except Exception as e:
            print("Failed to load index list")
            raise e

    def _append_index_component_daily(self, trade_date):
        """
        保存或追加某日指数的成分股
        每分钟最多访问该接口70次
        :param trade_date: str
            example: 20190101
        """
        trade_date_tmp = trade_date
        if isinstance(trade_date, str):
            trade_date_tmp = dateutil.tsformat_to_datetime(trade_date)
        if isinstance(trade_date, datetime):
            trade_date_tmp = dateutil.datetime_to_dbformat(trade_date)
        table_index_comp = 'index_comp'
        sql_index_comp = "SELECT count(1) AS count FROM index_comp WHERE trade_date='%s'" % trade_date_tmp
        try:
            # check if data exists
            res = dbutil.read_df(sql_index_comp)
            count = res['count'].iloc[0]
            if count > 0:
                print("Daily price exists: %s" % trade_date)
                return
            # load date
            index_comp = tsutil.query_index_component_daily(trade_date)
            # save
            if index_comp.shape[0] > 0:
                dbutil.save_df(index_comp, table_index_comp)
                print("Successful load daily index component: %s" % trade_date)
            else:
                print("No data: %s" % trade_date)
            time.sleep(2)
        except Exception as e:
            print("Failed to load daily index component: %s" % trade_date)
            raise e

    def save_index_stock_component(self, start_date, end_date):
        """
        保存指数成分
        :param start_date: str
        :param end_date: str
        """
        date_iterator = start_date
        mi = MarketInfo()
        all_trade_date = mi.get_all_trade_date()
        trade_date_dict = {}
        for row in all_trade_date.iterrows():
            trade_date_dict[row[1]['cal_date']] = row[1]['is_open']
        frames = []
        while int(date_iterator) <= int(end_date):
            is_open = trade_date_dict.get(date_iterator, 0)
            if is_open == 0:
                print("Not a trade date: %s" % date_iterator)
            else:
                self._append_index_component_daily(date_iterator)
            date_iterator = dateutil.datetime_to_tsformat(dateutil.get_next_day(date_iterator))
        if len(frames) == 0:
            return


ii = IndexInfo()
# ii.save_index_list(const.FILE_INDEX_LIST)
ii.save_index_stock_component('20000101', '20091231')
