# -*- coding:utf-8 -*-
"""
@author: Lucy
@file: dateutil.py
@time: 2019/03/03
"""

import tushare as ts

from common.constant import const


class tsutil:

    # pro token
    ts.set_token(const.TS_TOKEN)
    # init api
    pro = ts.pro_api()

    @classmethod
    def query_stock_list(cls):
        query_stock_basic = 'stock_basic'
        fields_stock_basic = 'ts_code,symbol,name,area,industry,fullname,enname,market,' \
                             'exchange,curr_type,list_status,list_date,delist_date,is_hs'
        return cls.pro.query(query_stock_basic, fields=fields_stock_basic)

    @classmethod
    def query_stock_price_daily(cls, trade_date):
        query_price_daily = 'daily'
        fields_price_daily = 'ts_code,trade_date,open,high,low,close,vol,amount'
        return cls.pro.query(query_price_daily, trade_date=trade_date, fields=fields_price_daily)

    @classmethod
    def query_stock_basic_daily(cls, trade_date):
        query_basic_daily = 'daily_basic'
        fields_basic_daily = 'ts_code,trade_date,pe,pe_ttm,pb,total_share,float_share,total_mv,circ_mv'
        return cls.pro.query(query_basic_daily, trade_date=trade_date, fields=fields_basic_daily)

    @classmethod
    def query_stock_profit(cls, stock_code, start_date, end_date):
        query_stock_profit = 'income'
        fields_stock_profit = 'ts_code,ann_date,f_ann_date,end_date,report_type,basic_eps,diluted_eps,' \
                              'total_revenue,operate_profit,total_profit,income_tax,n_income,n_income_attr_p'
        return cls.pro.query(query_stock_profit, ts_code=stock_code, start_date=start_date,
                  end_date=end_date, fields=fields_stock_profit)

    @classmethod
    def query_index_list(cls, market):
        return cls.pro.query('index_basic', market=market)

    @classmethod
    def query_index_component_daily(cls, trade_date):
        return cls.pro.query('index_weight', trade_date=trade_date)