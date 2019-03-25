import pandas as pd
import datetime
from jqdatasdk import *
from jqdemo.config import *
from jqdemo.util import *


class JQDataBase:

    def __init__(self):
        log.info("init jqdata")
        auth(get_user_name(), get_pwd())

    @staticmethod
    def get_all_stocks():
        today = datetime.datetime.today()
        all_stocks = get_all_securities(types=['stock', 'index', 'etf'], date=today)
        all_stocks['stock_code'] = all_stocks.index
        return all_stocks

    @staticmethod
    def get_all_trade_days():
        all_trade_days = get_all_trade_days()
        all_trade_days = convert_date_to_datetime(all_trade_days)
        all_trade_days = pd.DataFrame(all_trade_days, columns=['trade_day'])
        return all_trade_days

    @staticmethod
    def get_locked_share(stock_list, start_day, count=500):
        locked_shares = get_locked_shares(stock_list=stock_list,
                                          start_date=start_day, forward_count=count)
        return locked_shares

    @staticmethod
    def get_price(stock_list, end_day):
        return get_price(stock_list, start_date=datetime.datetime(2019, 1, 1),
                         end_date=end_day, frequency='daily', fq='pre',
                         fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit', 'low_limit', 'avg',
                                 'pre_close', 'paused'])
