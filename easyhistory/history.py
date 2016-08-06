# coding:utf-8
import os

import pandas as pd
import talib


class Indicator(object):
    def __init__(self, stock_code, history):
        self.stock_code = stock_code
        self.history = history

    def load_csv_files(self, path):
        file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
        for stock_csv in file_list:
            csv_ext_index_start = -4
            stock_code = stock_csv[:csv_ext_index_start]
            self.market[stock_code] = pd.read_csv(stock_csv, index_col='date')

    def __getattr__(self, item):
        def talib_func(*args, **kwargs):
            str_args = ''.join(map(str, args))
            if self.history.get(item + str_args) is not None:
                return self.history
            print(item)
            func = getattr(talib, item)
            """
            print(args)
            print(kwargs)
            res_arr = func(self.history['close'].values, *args, **kwargs)
            print(item + str_args)
            print(res_arr)
            #self.history[item + str_args] = res_arr
            """
            if item in ['MA','MAX','MIN']:
                res_arr = func(self.history['close'].values, *args, **kwargs)
                self.history[item + str_args] = res_arr
            if item == 'CCI':
                res_arr = func(self.history['high'].values,self.history['low'].values,
                               self.history['close'].values, *args, **kwargs)
                self.history[item + str_args] = res_arr
            if item == 'MACD':
                res_arr = func(self.history['close'].values, *args, **kwargs)
                self.history['macd'] = res_arr[0]       #DIF
                self.history['macdsignal'] = res_arr[1] #DEA
                self.history['macdhist'] = res_arr[2]  #MACD
                
            if item == 'BBANDS':
                res_arr = func(self.history['close'].values, *args, **kwargs)
                self.history['u_band'] = res_arr[0]
                self.history['m_band'] = res_arr[1]
                self.history['l_band'] = res_arr[2]
            if item =='STOCH':
                res_arr = func(self.history['high'].values,self.history['low'].values,
                               self.history['close'].values, *args, **kwargs)
                self.history['fastK'] = res_arr[0]
                self.history['slowD'] = res_arr[1]
                self.history['fastJ'] = 3 * self.history['fastK'] - 2 * self.history['slowD']
            if item =='MFI':
                res_arr = func(self.history['high'].values,self.history['low'].values,
                               self.history['close'].values, self.history['volume'].values,*args, **kwargs)
                self.history['MFI'] = res_arr
            if item =='ATR':
                res_arr = func(self.history['high'].values,self.history['low'].values,
                               self.history['close'].values,*args, **kwargs)
                self.history['ATR'] = res_arr
            if item =='NATR':
                res_arr = func(self.history['high'].values,self.history['low'].values,
                               self.history['close'].values,*args, **kwargs)
                self.history['NATR'] = res_arr
            return self.history

        return talib_func


class History(object):
    def __init__(self, dtype='D', path='history', codes=[]):
        self.market = dict()
        data_path = os.path.join(path, 'day', 'data')
        self.stock_codes = codes
        self.load_csv_files(data_path)

    def load_csv_files(self, path):
        if self.stock_codes:
            for stock_code in self.stock_codes:
                stock_csv = '%s.csv' % stock_code
                csv_path = os.path.join(path, stock_csv)
                self.market[stock_code] = Indicator(stock_code, pd.read_csv(csv_path, index_col='date'))
        else:
            file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
            for stock_csv in file_list:
                csv_ext_index_start = -4
                stock_code = stock_csv[:csv_ext_index_start]
    
                csv_path = os.path.join(path, stock_csv)
                self.market[stock_code] = Indicator(stock_code, pd.read_csv(csv_path, index_col='date'))

    def __getitem__(self, item):
        return self.market[item]
