# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: stock_info.py
@time: 2019/03/03
"""

import logging
import os
import time
import tushare as ts
import pandas as pd
from datetime import datetime
from core.market_info import MarketInfo
from common.constant import const
from util.dateutil import dateutil
from util.dbutil import dbutil
from util.tsutil import tsutil

enum_to_int = {
    "list_status": {"L": 0, "D": 1, "P": 2},  # 上市状态
    "is_hs": {"N": 0, "H": 1, "S": 2}  # 是否沪深港通
}


class StockInfo:

    def save_stock_list(self):
        """
        保存上市股票信息
        该接口只有上市股票数据，没有退市股票数据
        替换已存在数据，保持一份最新
        """
        table_stock_basic = 'stock_basic'
        try:
            # ts_code to drop
            stock_exist = dbutil.read_df("SELECT ts_code FROM %s" % table_stock_basic)
            ts_code_drop = stock_exist['ts_code']
            # load data from tushare
            stock_list = tsutil.query_stock_basic()
            # difference set
            flag = stock_list['ts_code'].isin(ts_code_drop)
            diff_flag = [not f for f in flag]
            stock_list = stock_list[diff_flag]
            # type conversion
            stock_list.replace(to_replace=enum_to_int, inplace=True)
            stock_list['list_date'] = dateutil.col_to_datetime()
            stock_list['delist_date'] = pd.to_datetime(stock_list['delist_date'],
                                                       format=const.DATE_FORMAT_TUSHARE,
                                                       errors='coerce')
            # insert new records
            dbutil.save_df(stock_list, table_stock_basic)
            print("Successfully load stock list: %d" % stock_list.shape[0])
        except Exception as e:
            print(e)
            return False

    def _append_daily_info(self, yyyymmdd):
        """
        保存每日行情数据和指标
        :param yyyymmdd: str
            example: '20190101'
        """
        query_price_daily = 'daily'
        fields_price_daily = 'ts_code,trade_date,open,high,low,close,vol,amount'
        query_basic_daily = 'daily_basic'
        fields_basic_daily = 'ts_code,trade_date,pe,pe_ttm,pb,total_share,float_share,total_mv,circ_mv'
        table_stock_price = 'stock_price'
        sql_stock_price = "SELECT count(1) AS count FROM stock_price WHERE trade_date='%s'" % \
                          dateutil.datetime_to_yyyy_mm_dd(dateutil.yyyymmdd_to_datetime(yyyymmdd))
        try:
            # check if data exists
            res = pd.read_sql_query(sql_stock_price, con=self._engine)
            count = res['count'].iloc[0]
            if count > 0:
                print("Daily price exists: %s" % yyyymmdd)
                return
            # load date
            price_daily = self._pro.query(query_price_daily, trade_date=yyyymmdd, fields=fields_price_daily)
            basic_daily = self._pro.query(query_basic_daily, trade_date=yyyymmdd, fields=fields_basic_daily)
            info_daily = pd.merge(price_daily, basic_daily, how='left', on=['ts_code', 'trade_date'])
            # save
            self._save_to_db(info_daily, table_stock_price)
            print("Successful load daily price: %s" % yyyymmdd)
            time.sleep(2)
        except Exception as e:
            print("Failed to load daily price: %s" % yyyymmdd)
            raise e

    def save_daily_info(self, start_date, end_date):
        """
        按日保存个股数据
        :param start_date: str
            example:'20180101'
        :param end_date:
            example:'20180101'
        :param dir:
            dir path to save daily stock info
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
                self._append_daily_info(date_iterator)
            date_iterator = dateutil.get_next_day(date_iterator)
        if len(frames) == 0:
            return

    def _get_stock_profit(self, stock_code, start_date, end_date):
        """
        按个股保存利润数据
        :param stock_code: str
        :param start_date: str
        :param end_date: str
        """
        query_stock_profit = 'income'
        fields_stock_profit = 'ts_code,ann_date,f_ann_date,end_date,report_type,basic_eps,diluted_eps,' \
                              'total_revenue,operate_profit,total_profit,income_tax,n_income,n_income_attr_p'
        try:
            # stock profit exit
            stock_profit = self._pro.query(query_stock_profit, ts_code=stock_code, start_date=start_date,
                                           end_date=end_date, fields=fields_stock_profit)
            # type conversion
            stock_profit['ann_date'] = pd.to_datetime(stock_profit['ann_date'],
                                                      format=const.DATE_FORMAT_TUSHARE,
                                                      errors='coerce')
            stock_profit['f_ann_date'] = pd.to_datetime(stock_profit['f_ann_date'],
                                                        format=const.DATE_FORMAT_TUSHARE,
                                                        errors='coerce')
            stock_profit['end_date'] = pd.to_datetime(stock_profit['end_date'],
                                                      format=const.DATE_FORMAT_TUSHARE,
                                                      errors='coerce')
            time.sleep(5)
            return stock_profit
        except Exception as e:
            print("Failed to load stock profit: %s" % stock_code)
            raise e

    def save_stock_profit(self, start_date, end_date):
        """
        按个股保存利润数据
        个股列表来自数据库
        :param start_date: str
            如'20181201'
        :param end_date: str
            如'20181201'
        """
        sql_stock_list = 'SELECT ts_code FROM stock_basic'
        table_stock_profit = 'stock_profit'
        try:
            # load stock list
            stock_list = pd.read_sql(sql_stock_list, con=self._engine)
            # iterate
            for stock_code in stock_list['ts_code']:
                stock_profit = self._get_stock_profit(stock_code, start_date=start_date, end_date=end_date)
                # insert latest records
                if stock_profit.shape[0] > 0:
                    self._save_to_db(stock_profit, table_stock_profit)
                    print("Successfully load stock profit: %s, start: %s, end: %s" % (stock_code, start_date, end_date))
                else:
                    print("No stock profit: %s, start: %s, end: %s" % (stock_code, start_date, end_date))
        except Exception as e:
            print(e)

    def save_stock_profit_auto(self):
        """
        按个股保存利润数据
        个股列表来自数据库
        起始时间为数据库中group by stock_code的max(实际公布日期)的下个月
        结束时间为今日
        """
        sql_stock_list = 'SELECT ts_code FROM stock_basic'
        sql_stock_profit = 'SELECT ts_code, MAX(f_ann_date) AS date FROM stock_profit GROUP BY ts_code'
        table_stock_profit = 'stock_profit'
        try:
            # load historic data
            max_date = {}
            profit_hist = pd.read_sql_query(sql_stock_profit, con=self._engine)
            for row in profit_hist.iterrows():
                max_date[row[1]['ts_code']] = row[1]['date']
            # load stock list
            stock_list = pd.read_sql(sql_stock_list, con=self._engine)
            # iterate
            for stock_code in stock_list['ts_code']:
                start_date = max_date.get(stock_code, None)
                end_date = dateutil.datetime_to_yyyymmdd(datetime.now())
                if not start_date is None:
                    start_date = dateutil.datetime_to_yyyymmdd(dau.get_first_day_of_next_month(start_date))
                    if start_date > end_date:
                        continue
                stock_profit = self._get_stock_profit(stock_code, start_date=start_date, end_date=end_date)
                # insert latest records
                if stock_profit.shape[0] > 0:
                    self._save_to_db(stock_profit, table_stock_profit)
                    print("Successfully load stock profit: %s, start: %s, end: %s" % (stock_code, start_date, end_date))
                else:
                    print("No stock profit: %s, start: %s, end: %s" % (stock_code, start_date, end_date))
        except Exception as e:
            print(e)


si = StockInfo()
# si.save_stock_list()
# si.save_stock_info(const.FILE_STOCK_LIST, const.DIR_STOCK_INFO)
si.save_daily_info('20140720', '20190310')
# si.save_stock_profit_auto()
