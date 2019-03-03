#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: main.py
@time: 2019/03/01
"""

from core.market_info import MarketInfo
from common.constant import const
from datetime import datetime
import os
import logging


handler = logging.FileHandler(const.FILE_LOG)
fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter) #设置输出内容的格式
logger = logging.getLogger()
logger.setLevel('INFO')
logger.addHandler(handler)

file_suffix = datetime.now().strftime(const.DATE_FORMAT_ONE) + const.CSV_EXTENSION
current_stock_list_file = const.DIR_STOCK_LIST + file_suffix
current_trade_date_file = const.DIR_TRADE_DATE + file_suffix
current_index_list_file = const.DIR_INDEX_LIST + file_suffix

def hist():
    # 加载一遍股票基本信息
    if not os.path.exists(current_stock_list_file):
        load_stock_list = mi.save_stock_list(current_stock_list_file)
        if not load_stock_list:
            raise("Failed to load stock list: %s" % current_stock_list_file)
    logger.info("Successfully load stock list: %s" % current_stock_list_file)

    # 加载一遍交易日
    if not os.path.exists(current_trade_date_file):
        load_trade_date = mi.save_all_trade_date(current_trade_date_file)
        if not load_trade_date:
            raise("Failed to load trade date: %s" % current_trade_date_file)
    logger.info("Successfully load trade date: %s" % current_trade_date_file)

def real():
    pass


mi = MarketInfo()
hist()


