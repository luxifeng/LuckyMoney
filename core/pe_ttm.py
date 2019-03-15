# -*- coding:utf-8 -*-
"""
最后的目标！
计算指数pe ttm！

@author: Lucy
@file: pe_ttm.py
@time: 2019/03/15
"""

import pandas as pd
from datetime import datetime
from core.market import MarketInfo
from util.dateutil import dateutil
from util.dbutil import dbutil
from util.tsutil import tsutil


class PEInfo:

    def _cal_index_pe_ttm(self, trade_date, ):
        """
        计算指数pe-ttm
        :return:
        """
