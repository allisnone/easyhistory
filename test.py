import easyhistory
easyhistory.init('D', export='csv', path="C:/hist",stock_codes=['002789'])
easyhistory.update(path="C:/hist",stock_codes=['000042','000060'])
#easyhistory.update_single_code(dtype='D', stock_code='002789', path="C:/hist")
his = easyhistory.History(dtype='D', path='C:/hist',codes=['000042','000060'])

# MA 计算, 直接调用的 talib 的对应函数
res = his['000042'].MA(5)
describe_df = his['000042'].MA(1).tail(3).describe()
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
update_hist(push_stocks)