# -*- coding:utf-8 -*-
"""
指数层面信息

@author: Lucy
@file: index_info.py
@time: 2019/03/02
"""

import logging
import os
import tushare as ts
import pandas as pd
import time
import math
from datetime import datetime
from common.constant import const
import util.date_util as du


class IndexInfo:

    def __init__(self):
        # pro token
        ts.set_token(const.TS_TOKEN)
        # init api
        self._pro = ts.pro_api()

    def save_index_list(self, file_path):
        """
        保存中证、上交所、深交所指数列表
        与已存在的数据合并，保持一份最新
        :param file_path: str
            path to save index list
        :return bool
        """
        try:
            index_list_csi = self._pro.query('index_basic', market='CSI')
            index_list_sse = self._pro.query('index_basic', market='SSE')
            index_list_szse = self._pro.query('index_basic', market='SZSE')
            index_list = index_list_csi.append([index_list_sse, index_list_szse])
            if os.path.exists(file_path):
                exist_index_list = pd.read_csv(file_path, encoding='utf-8')
                index_list = index_list.append(exist_index_list)
                index_list.drop_duplicates()
            index_list.to_csv(file_path, header=True, index=False, encoding='utf-8')
            print("Successfully load index list")
        except Exception as e:
            print("Failed to load index list")
            raise e

    def _append_index_component(self, index_code, start_date, end_date, file_path):
        """
        保存或追加某只指数的成分股
        每分钟最多访问该接口70次
        :param index_code: str
            example: 399300.SZ
        :param start_date: str
            example: 20190101
        :param end_date: str
            example: 20190101
        :param file_path: str
            example: ../data/index/component/111.dz.csv
        :return: bool
        """
        try:
            index_comp = self._pro.query('index_weight', index_code=index_code, start_date=start_date,
                                         end_date=end_date)
            if os.path.exists(file_path):
                index_comp.to_csv(file_path, header=False, index=False, mode='a', encoding='utf-8')
            else:
                index_comp.to_csv(file_path, header=True, index=False, encoding='utf-8')
            print("Successfully load index component: %s" % index_code)
            time.sleep(10)
        except Exception as e:
            print("Failed to load index componenet: %s, start: %s, end: %s" % (index_code, start_date, end_date))
            raise e

    def save_index_stock_component(self, from_file_path, to_dir_path):
        """
        保存指数成分，按指数代码保存一份最新，月更
        若无存在的数据，则从20000101开始获取至今的数据
        若有存在的数据，则从最后数据的下个月第一天开始获取
        :param from_file_path: str
            path to read index list
        :param to_dir_path: str
            path to save index component info
        :param start_date: str
            start date
        :param end_date: str
            end date
        """
        start_date = const.DATE_START
        end_date = du.datetime_to_yyyymmdd(datetime.now())
        try:
            index_list = pd.read_csv(from_file_path, encoding='utf-8')
            index_code = index_list['ts_code']
            for item in index_code:
                file_path = to_dir_path + item + const.CSV_EXTENSION
                if os.path.exists(file_path):
                    index_comp_series = pd.read_csv(file_path, encoding='utf-8')
                    last_trade_date = str(index_comp_series['trade_date'].max())
                    if last_trade_date.lower() == 'nan':
                        start_date = const.DATE_START
                    elif end_date[0:6] != last_trade_date[0:6]:
                        start_date_tmp = du.yyyymmdd_to_datetime(last_trade_date)
                        first_day_of_next_month = du.get_first_day_of_next_month(start_date_tmp)
                        start_date = du.datetime_to_yyyymmdd(first_day_of_next_month)
                    else:
                        continue
                self._append_index_component(item, start_date=start_date, end_date=end_date, file_path=file_path)
        except Exception as e:
            raise e


ii = IndexInfo()
# ii.save_index_list(const.FILE_INDEX_LIST)
ii.save_index_stock_component(const.FILE_INDEX_LIST, const.DIR_INDEX_COMP)
