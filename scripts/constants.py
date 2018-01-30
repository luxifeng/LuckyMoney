#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: common.py
@time: 2018/01/31
"""

class _constants:
  class ConstantsError(TypeError): pass
  class ConstantsCaseError(ConstantsError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstantsError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstantCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

constant = _constants()
constant.STOCK_LIST_FILE_DIR = '../data/stock_list/'
constant.STOCK_LIST_FILE_TYPE = '.txt'
constant.STOCK_DATA_FILE_DIR = '../data/stock_data/'
constant.STOCK_DATA_FILE_TYPE = '.csv'
constant.STOCK_DATA_FIELDS = ['date', 'open', 'close', 'high', 'low', 'volume']