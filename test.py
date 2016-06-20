import easyhistory
easyhistory.init('D', export='csv', path="C:/hist",stock_codes=['002789'])
#easyhistory.update(path="C:/hist",stock_codes=['000042','000060'])
#easyhistory.update_single_code(dtype='D', stock_code='002789', path="C:/hist")

def update_hist(codes=[]):
    this_day = Day(path="C:/hist")
    stock_codes_need_to_init = this_day.store.init_stock_codes
    actual_init_codes = list(set(stock_codes_need_to_init).intersection(set(codes)))
    if actual_init_codes:
        easyhistory.init('D', export='csv', path="C:/hist",stock_codes=actual_init_codes)
    if len(codes)==1:
        easyhistory.update_single_code(dtype='D', stock_code=codes[0], path="C:/hist")
    elif len(codes)>=2:
        for code in codes:
            easyhistory.update_single_code(dtype='D', stock_code=codes[0], path="C:/hist")
    else:
        pass

