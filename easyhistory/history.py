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
            func = getattr(talib, item)
            """
            print(args)
            print(kwargs)
            res_arr = func(self.history['close'].values, *args, **kwargs)
            print(item + str_args)
            print(res_arr)
            #self.history[item + str_args] = res_arr
            """
            if item in ['MA','MOM','MAX','MIN','RSI','LINEARREG','LINEARREG_ANGLE','LINEARREG_INTERCEPT','LINEARREG_SLOPE']:
                column='close'
                column_key = item + str_args
                """
                print('column_key=',column_key)
                print(args)
                print(len(args))
                print(kwargs)
                """
                if len(args)==2:
                    column = args[1]
                    args = tuple([args[0]])
                res_arr = func(self.history[column].values, *args, **kwargs)
                self.history[column_key] = res_arr
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
            if item in [ 'CDLMORNINGDOJISTAR',#morning Doji Star (Pattern Recognition)  十字启明星, penetration: 0.3
                        'CDLEVENINGDOJISTAR',#Evening Doji Star (Pattern Recognition),penetration: 0.3
                        'CDLPIERCING', #Piercing Pattern (Pattern Recognition) 穿刺模型
                        'CDLABANDONEDBABY', #Abandoned Baby (Pattern Recognition)
                        'CDL3WHITESOLDIERS', #Three Advancing White Soldiers (Pattern Recognition) 红三兵
                        'CDLABANDONEDBABY',#Abandoned Baby (Pattern Recognition),penetration: 0.3
                        'CDLBELTHOLD',#Belt-hold (Pattern Recognition)
                        'CDLBREAKAWAY',#Breakaway (Pattern Recognition)  破茧而出
                        'CDLCONCEALBABYSWALL',#Concealing Baby Swallow (Pattern Recognition)
                        'CDLDARKCLOUDCOVER',#Dark Cloud Cover (Pattern Recognition)
                        'CDLDRAGONFLYDOJI',#Dragonfly Doji (Pattern Recognition)
                        ]:
                res_arr = func(self.history['open'].values, self.history['high'].values, self.history['low'].values, 
                               self.history['close'].values,*args, **kwargs)
                self.history[item] = res_arr
            if item== 'SAR':
                #acceleration: 0.02,maximum: 0.2
                res_arr = func(self.history['high'].values, self.history['low'].values, *args, **kwargs)
                self.history[item] = res_arr
            return self.history

        return talib_func


class History(object):
    def __init__(self, dtype='D', path='history', codes=[],type='csv',stock_sql=None):
        self.market = dict()
        self.indicator_result = dict()
        self.except_codes = list()
        data_path = os.path.join(path, 'day', 'data')
        self.stock_codes = codes
        if type=='csv':
            self.load_csv_files(data_path)
        elif type=='mysql':
            self.get_sql_data(stock_sql)
            pass
        else:
            pass
            

    def load_csv_files(self, path):
        if self.stock_codes:
            for stock_code in self.stock_codes:
                stock_csv = '%s.csv' % stock_code
                csv_path = os.path.join(path, stock_csv)
                try:
                    hist_data = pd.read_csv(csv_path)#, index_col='date')
                    self.market[stock_code] = Indicator(stock_code, hist_data)
                except:
                    self.except_codes.append(stock_csv)
        else:
            file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
            for stock_csv in file_list:
                csv_ext_index_start = -4
                stock_code = stock_csv[:csv_ext_index_start]
                csv_path = os.path.join(path, stock_csv)
                try:
                    hist_data = pd.read_csv(csv_path)#, index_col='date')
                    self.market[stock_code] = Indicator(stock_code, hist_data)
                except:
                    self.except_codes.append(stock_csv)
        #print('except_codes=',self.except_codes)
    
    def get_sql_data(self,stock_sql): #index_col='date'
        for stock_code in self.stock_codes:
            data_df = stock_sql.get_table_df(table=stock_code,columns=None)
            #data_df = data_df.set_index('date')
            self.market[stock_code] = Indicator(stock_code, data_df)
        return
    
    def __getitem__(self, item):
        return self.market[item]

    def get_hist_indicator(self,code_str):
        #http://www.stock-trading-infocentre.com/hanging-man.html
        res = self[code_str].MAX(20)
        res = self[code_str].MAX(20,'high')
        res = self[code_str].MIN(20)
        res = self[code_str].MIN(20,'low')
        res = self[code_str].MAX(3)
        res = self[code_str].MIN(3,'low')
        res = self[code_str].MA(5)
        res = self[code_str].MA(10)
        res = self[code_str].MA(20)
        res = self[code_str].MA(30)
        res = self[code_str].MA(60)
        res = self[code_str].MA(120)
        res = self[code_str].MA(250)
        res = self[code_str].CCI(timeperiod=14)
        res = self[code_str].MACD(fastperiod=12, slowperiod=26, signalperiod=9)
        res = self[code_str].BBANDS(timeperiod=10,nbdevup=2, nbdevdn=2)#(20,2,2)  #boll
        res = self[code_str].STOCH(fastk_period=9, slowk_period=3, slowd_period=3)  #KDJ
        res = self[code_str].MFI(timeperiod=14)  #MFI
        res = self[code_str].ATR(timeperiod=14)  #Average True Range 
        res = self[code_str].NATR(timeperiod=14)  #Normalized Average True Range 
        res = self[code_str].MOM(timeperiod=12)  #Momentum Indicators
        res = self[code_str].CDLMORNINGDOJISTAR()  #Momentum Indicators
        res = self[code_str].CDLABANDONEDBABY()
        res = self[code_str].CDLBELTHOLD()
        res = self[code_str].CDLBREAKAWAY()
        res = self[code_str].CDL3WHITESOLDIERS()
        res = self[code_str].CDLPIERCING()
        res = self[code_str].SAR()
        res = self[code_str].RSI()
        #'LINEARREG','LINEARREG_ANGLE','LINEARREG_INTERCEPT','LINEARREG_SLOPE'
        res = self[code_str].LINEARREG(14) #timeperiod: 14
        res = self[code_str].LINEARREG(30) #timeperiod: 30
        res = self[code_str].LINEARREG_ANGLE(14)
        res = self[code_str].LINEARREG_INTERCEPT(14)
        res = self[code_str].LINEARREG_SLOPE(14)
        res = self[code_str].LINEARREG_SLOPE(30)
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'MA30') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14MA30'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'MA60') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14MA60'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'MA120') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14MA120'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'MA250') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14MA250'] = -100.0
            
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'CCI') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14CCI'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'SAR') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14SAR'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'RSI') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14RSI'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'macdhist') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14macdhist'] = -100.0
        try:
            res = self[code_str].LINEARREG_ANGLE(14,'MOM') #timeperiod: 14
        except:
            res['LINEARREG_SLOPE14MOM'] = -100.0
        #res = self[code_str].RSI()
        #res = self[code_str].RSI()
        res['MTM'] = 100*res['MOM']/(res['close'].shift(12))
        self.indicator_result[code_str] = res
        return res
    
    def update_indicator_results(self):
        for code_str in self.stock_codes:
            self.get_hist_indicator(code_str)
        return