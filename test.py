import easyhistory
#easyhistory.init('D', export='csv', path="C:/hist",stock_codes=['sh000001'])
#easyhistory.update(path="C:/hist",stock_codes=['000042','000060'])
#easyhistory.update_single_code(dtype='D', stock_code='002789', path="C:/hist")
s_sql = pds.StockSQL()
his = easyhistory.History(dtype='D', path='C:/hist',type='mysql',codes=['sh','cyb'],stock_sql=s_sql)
test_code = 'sh'
# MA 计算, 直接调用的 talib 的对应函数
res = his[test_code].MAX(20)
res = his[test_code].MIN(20)
res = his[test_code].MA(5)
res = his[test_code].MA(10)
res = his[test_code].MA(20)
res = his[test_code].MA(30)
res = his[test_code].MA(60)
res = his[test_code].MA(120)
res = his[test_code].MA(250)
res = his[test_code].CCI(timeperiod=14)
res = his[test_code].MACD(fastperiod=12, slowperiod=26, signalperiod=9)
res = his[test_code].BBANDS(timeperiod=10,nbdevup=2, nbdevdn=2)#(20,2,2)  #boll
res = his[test_code].STOCH(fastk_period=9, slowk_period=3, slowd_period=3)  #KDJ
res = his[test_code].MFI(timeperiod=14)  #MFI
res = his[test_code].ATR(timeperiod=14)  #Average True Range 
res = his[test_code].NATR(timeperiod=14)  #Normalized Average True Range 
res = his[test_code].MOM(12)  #Momentum Indicators
print( res)
res.to_csv('%s.csv' % test_code)
describe_df = his[test_code].MA(1).tail(3).describe()
min_low = describe_df.loc['min'].low
min_close = describe_df.loc['min'].close
max_close = describe_df.loc['max'].close
max_high = describe_df.loc['max'].high

print(describe_df)
print(min_low,min_close,max_close)


def update_hist(codes=[]):
    this_day = easyhistory.Day(path="C:/hist")
    stock_codes_need_to_init = this_day.store.init_stock_codes
    actual_init_codes = list(set(stock_codes_need_to_init).intersection(set(codes)))
    if actual_init_codes:
        easyhistory.init('D', export='csv', path="C:/hist",stock_codes=actual_init_codes)
    else:
        pass
    if len(codes)>=1:
        for code in codes:
            easyhistory.update_single_code(dtype='D', stock_code=code, path="C:/hist")
    else:
        pass


push_stocks=['000932', '002191', '002521', '002766', '601009', '000002', '300162']
#update_hist(push_stocks)