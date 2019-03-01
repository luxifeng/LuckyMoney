#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: common.py
@time: 2018/01/31
"""

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

const = _const()
const.TS_TOKEN = ''
const.DIR_STOCK_LIST = '../data/stock_list/'