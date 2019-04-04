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
    __pro = ts.pro_api()

    @classmethod
    def connect(cls):
        return cls.__pro


def query_stock_list():
    query_stock_basic = 'stock_basic'
    fields_stock_basic = 'ts_code,symbol,name,area,industry,fullname,enname,market,' \
                         'exchange,curr_type,list_status,list_date,delist_date,is_hs'
    return tsutil.connect().query(query_stock_basic, fields=fields_stock_basic)


def query_stock_price_daily(trade_date):
    query_price_daily = 'daily'
    fields_price_daily = 'ts_code,trade_date,open,high,low,close,vol,amount'
    return tsutil.connect().query(query_price_daily, trade_date=trade_date, fields=fields_price_daily)


def query_stock_basic_daily(trade_date):
    query_basic_daily = 'daily_basic'
    fields_basic_daily = 'ts_code,trade_date,pe,pe_ttm,pb,total_share,float_share,total_mv,circ_mv'
    return tsutil.connect().query(query_basic_daily, trade_date=trade_date, fields=fields_basic_daily)


def query_stock_profit(stock_code, start_date, end_date):
    query_stock_profit = 'income'
    fields_stock_profit = 'ts_code,ann_date,f_ann_date,end_date,report_type,basic_eps,diluted_eps,' \
                          'total_revenue,operate_profit,total_profit,income_tax,n_income,n_income_attr_p'
    return tsutil.connect().query(query_stock_profit, ts_code=stock_code, start_date=start_date,
                         end_date=end_date, fields=fields_stock_profit)

def query_index_list(market):
    query_index_basic = 'index_basic'
    fields_index_basic = 'ts_code,name,market,publisher,index_type,category,base_date,base_point,' \
                         'list_date,weight_rule,desc,exp_date'
    return tsutil.connect().query(query_index_basic, market=market, fields=fields_index_basic)


def query_index_component_daily(trade_date):
    return tsutil.connect().query('index_weight', trade_date=trade_date)

def query_index_component(ts_code, start_date, end_date):
    return tsutil.connect().query('index_weight', ts_code=ts_code, start_date=start_date, end_date=end_date)


def query_trade_date(start_date, end_date):
    return tsutil.connect().query('trade_cal', exchange='', start_date=start_date, end_date=end_date)


df = query_index_component('000300.SH', '20190101', '20190330')
print(df.head(5))