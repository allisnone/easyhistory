# coding:utf-8
from .day import Day


def init(dtype='D', export='csv', path='history',stock_codes=[],set_stocks=[]):
    return Day(path=path, export=export,codes=stock_codes).init(set_stocks)


def update_single_code(dtype='D', stock_code=None, path='history', export='csv'):
    if stock_code is None:
        raise Exception('stock code is None')
    return Day(path=path, export=export).update_single_code(stock_code)


def update(dtype='D', export='csv', path='history',stock_codes=[]):
    return Day(path=path, export=export,codes=stock_codes).update()
