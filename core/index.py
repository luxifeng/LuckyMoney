# -*- coding:utf-8 -*-
"""
指数层面信息，包括获取指数列表、成分股和权重

@author: Lucy
@file: index.py
@time: 2019/03/02
"""

import time
from datetime import datetime
from core.market import MarketInfo
import util.dateutil as dtu
import util.dbutil as dbu
import util.tsutil as tsu


class IndexInfo:

    def __init__(self, market_info):
        self._market_info = market_info

    def save_index_list(self):
        """
        保存中证、上交所、深交所指数列表
        与已存在的数据合并，保持一份最新
        """
        table_index_list = "index_basic"
        sql_delete_index_basic = 'DELETE FROM %s' % table_index_list
        try:
            index_list_csi = tsu.query_index_list("CSI")
            index_list_sse = tsu.query_index_list('SSE')
            index_list_szse = tsu.query_index_list('SZSE')
            index_list_msci = tsu.query_index_list('MSCI')
            index_list_cicc = tsu.query_index_list('CICC')
            index_list_sw = tsu.query_index_list('SW')
            index_list_cni = tsu.query_index_list('CNI')
            index_list_oth = tsu.query_index_list('OTH')
            index_list = index_list_csi.append([index_list_sse, index_list_szse, index_list_msci, index_list_cicc,
                                                index_list_sw, index_list_cni, index_list_oth])
            index_list['base_date'] = dtu.tsformat_col_to_datetime(index_list['base_date'])
            index_list['list_date'] = dtu.tsformat_col_to_datetime(index_list['list_date'])
            index_list['exp_date'] = dtu.tsformat_col_to_datetime(index_list['exp_date'])
            dbu.save_df(index_list, table_index_list, if_exists='replace')
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
            trade_date_tmp = dtu.tsformat_to_datetime(trade_date)
        if isinstance(trade_date, datetime):
            trade_date_tmp = dtu.datetime_to_dbformat(trade_date)
        table_index_comp = 'index_comp'
        sql_index_comp = "SELECT count(1) AS count FROM index_comp WHERE trade_date='%s'" % trade_date_tmp
        try:
            # check if data exists
            res = dbu.read_df(sql_index_comp)
            count = res['count'].iloc[0]
            if count > 0:
                print("Daily index component exists: %s" % trade_date)
                return
            # load date
            index_comp = tsu.query_index_component_daily(trade_date)
            # save
            if index_comp.shape[0] > 0:
                dbu.save_df(index_comp, table_index_comp)
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
        frames = []
        while int(date_iterator) <= int(end_date):
            if not self._market_info.is_trade_date(date_iterator):
                print("Not a trade date: %s" % date_iterator)
            else:
                self._append_index_component_daily(date_iterator)
            date_iterator = dtu.datetime_to_tsformat(dtu.get_next_day(date_iterator))
        if len(frames) == 0:
            return

