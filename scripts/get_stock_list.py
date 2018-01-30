#-*- coding:utf-8 -*-
"""
@author: Lucy
@file: get_stock_list.py
@time: 2018/01/28
"""

import datetime
from lxml import etree
from urllib import request
from scripts import constants

url = 'http://quote.eastmoney.com/stocklist.html'
reg = '//div[@id="quotesearch"]/ul/li/a/text()'
path = constants.STOCK_LIST_FILE_DIR + datetime.date.today().strftime('%Y-%m-%d') + constants.STOCK_LIST_FILE_TYPE


# 获取网页内容
def getHtml(url):
    page = request.urlopen(url)
    html = page.read().decode('gbk')
    return html

# xpath解析路径
def parseHtml(reg, html):
    selector = etree.HTML(html.lower())
    result = selector.xpath(reg)
    return result

# 获取A股股票代码
def getCode(stock_list):
    codes = []
    for stock in stock_list:
        code_1 = stock.split('(')[1]
        code_2 = str.replace(code_1, ')', '')
        code_3 = code_2.strip()
        if code_3.startswith(('6', '3', '0')):
            codes.append(code_3)
    return codes

# 写入文件
def write(stock_a_codes, path):
    try:
        f = open(path, 'w')
        for code in stock_a_codes:
            f.writelines(code + '\n')
        f.close()
    except FileNotFoundError:
        print("文件不存在")
    except PermissionError:
        print("无权操作该文件")


html = getHtml(url)
stock_list = parseHtml(reg, html)
stock_a_codes = getCode(stock_list)
write(stock_a_codes, path)