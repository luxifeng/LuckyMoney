#-*- coding:utf-8 -*-
"""
constants

@author: Lucy
@file: const.py
@time: 2019/03/01
"""

class _Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const(%s) value" % name)
        if not name.isupper():
            raise self.ConstCaseError("Const name %s is not all uppercase" % name)
        self.__dict__[name] = value

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise self.ConstError("Can't return const %s, No Existing Key!" % item)

    def __delattr__(self, item):
        if item in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)" % item)
        raise NameError(item)

const = _Const()
const.TS_TOKEN = ''

const.DIR_TRADE_DATE = '../data/trade_date/'
const.DIR_INDEX_COMP = '../data/index/component/'
const.DIR_STOCK_INFO = '../data/stock/info/'
const.FILE_LOG = '../logs/lm.log'
const.FILE_STOCK_LIST = '../data/stock/stock_list.csv'
const.FILE_INDEX_LIST = '../data/index/index_list.csv'
const.CSV_EXTENSION = '.csv'
const.DATE_FORMAT_ONE = '%Y-%m-%d'
const.DATE_FORMAT_TWO = '%Y%m%d'
const.DATE_START = '20000101'