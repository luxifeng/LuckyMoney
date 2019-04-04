# -*- coding:utf-8 -*-
"""
最后的目标！
计算指数pe ttm(等权重)

计算公式：
指数的PE=指数市值/指数收益=n/∑[1/pe(个股)]

@author: Lucy
@file: pe_ttm.py
@time: 2019/03/15
"""

import pandas as pd
import util.dateutil as dtu
import util.dbutil as dbu


class PEInfo:

    def __init__(self, market_info):
        self._market_info = market_info

    def _daily_stock_pettm(self, last_stock_pettm, curr_date):
        """
        获取当前日期的股票价格池，停牌股票沿用上日数据，退市股票踢出价格池
        :param last_stock_pettm: dict
        :param curr_date: str
            当前日期，yyyymmdd
        :return: dict
        """
        aql_stock_price = "SELECT ts_code, pe_ttm FROM stock_price WHERE trade_date='%s'" % dtu.tsformat_to_dbformat(curr_date)
        curr_stock_pool = dbu.read_df(aql_stock_price)
        if last_stock_pettm is None:
            last_stock_pettm = {}
        for row in curr_stock_pool.iterrows():
            ts_code = row['ts_code']
            ts_pe = row['pe_ttm']
            last_stock_pettm[ts_code] = ts_pe
        for key, value in last_stock_pettm.items():
            # 若退市，则移除
            if self._market_info.is_delisted(key, curr_date):
                last_stock_pettm.pop(key)
        return last_stock_pettm

    def _daily_index_comp(self, index_codes, last_index_comp, curr_date):
        """
        获取当日指数的成分池，若数据库获取不到，则沿用历史数据
        :param index_codes: list
        :param last_index_comp: dataframe
        :param curr_date: str
            yyyymmdd
        :return:
        """
        if not isinstance(index_codes, list) or len(index_codes) == 0:
            return
        index_codes_str = ''
        for index_code in index_codes:
            index_codes_str += ',' + index_code
        index_codes_str = index_codes_str[1:]
        sql_index_comp = "SELECT index_code, con_code FROM index_comp WHERE trade_date='%s' AND index_code in (%s)" % \
                         (dtu.tsformat_to_dbformat(curr_date), index_codes_str)
        curr_index_comp = dbu.read_df(sql_index_comp)
        if last_index_comp is None:
            return curr_index_comp
        # 新有取新，新无取旧
        for index_code in index_codes:
            if index_code in curr_index_comp['index_code']:
                continue
            last_index_subset_flag = last_index_comp['index_code'] == index_code
            curr_index_comp.append(last_index_comp[last_index_subset_flag], ignore_index=True)
        return curr_index_comp

    def _index_pe_ttm(self, curr_index_comp, curr_stock_pettm):
        """
        计算指数pe-ttm
        function: n/∑[1/pe(个股)]
        :param index_comp: dataframe
        :param curr_stock_pettm_dict: dict
        :return: float
        """
        comp_num = curr_index_comp.shape[0]
        stock_pe_sum = 0
        for row in curr_index_comp.iterrows():
            ts_code = row['con_code']
            ts_pe = curr_stock_pettm[ts_code]
            if not ts_pe:
                raise Exception("Stock pe missing:" + ts_code)
            stock_pe_sum += 1 / ts_pe
        return comp_num / stock_pe_sum

    def _market_pettm(self, curr_stock_pettm):
        """
        计算全市场pe-ttm
        :param curr_stock_pettm: dict
        :return: float
        """
        comp_num = curr_stock_pettm.shape[0]
        stock_pe_sum = 0
        for key, value in curr_stock_pettm.items():
            if not value:
                raise Exception("Stock pe missing:" + key)
            stock_pe_sum += 1 / value
        return comp_num / stock_pe_sum

    def _daily_index_pettm(self, curr_index_comp, curr_stock_pettm):
        """
        获取当日指数pettm
        注意还包括全市场pettm
        :param curr_index_comp: dataframe
        :param curr_stock_pettm: dict
        :return: dataframe
        """
        unique_index_code = curr_index_comp['index_code'].unique
        index_pettm = pd.DataFrame(columns=['index_code', 'pe_ttm'])
        iloc = 0
        for index_code in unique_index_code:
            index_comp_subset_flag = curr_index_comp['index_code'] == index_code
            index_comp_subset = curr_index_comp[index_comp_subset_flag]
            if not index_comp_subset:
                continue
            pe_ttm = self._index_pe_ttm(index_comp_subset, curr_stock_pettm)
            index_pettm['index_code'].loc[iloc] = index_code
            index_pettm['pe_ttm'].loc[iloc] = pe_ttm
            iloc += 1
        index_pettm['index_code'].loc[iloc] = "market"
        index_pettm['pe_ttm'].loc[iloc] = self._market_pettm(curr_stock_pettm)
        return index_pettm

    def index_pe_ttm(self, index_codes, start_date, end_date):
        """
        给定index集合，计算从start_date至end_date的pe
        :param index_codes: list / str
        :param start_date: str
            起始日期，yyyymmdd
        :param end_date: str
            结束日期，yyyymmdd
        """
        if isinstance(index_codes, str):
            index_codes = [index_codes]
        curr_date = start_date
        last_stock_pettm = None
        last_index_comp = None
        hist_index_pettm = pd.DataFrame(columns=['index_code', 'pe_ttm', 'trade_date'])
        while(dtu.tsformat_compare(curr_date, end_date) <= 0):
            if self._market_info.is_trade_date(curr_date):
                curr_stock_pettm = self._daily_stock_pettm(last_stock_pettm, curr_date)
                curr_index_comp = self._daily_index_comp(index_codes, last_index_comp, curr_date)
                curr_index_pettm = self._daily_index_pettm(curr_index_comp, curr_stock_pettm)
                curr_index_pettm['trade_date'] = dtu.tsformat_to_dbformat(curr_date)
                hist_index_pettm = hist_index_pettm.append(curr_index_pettm, ignore_index=True)
                last_stock_pettm = curr_stock_pettm
                last_index_comp = curr_index_comp
            curr_date = dtu.get_next_day(curr_date)
        dbu.save_df(hist_index_pettm, 'index_pe', if_exists='replace')