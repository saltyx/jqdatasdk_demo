import pandas as pd
from jqdatasdk import *
import jqdatasdk
from config.config import *
from jqdemo.util import *


class BaseJQData:

    def __init__(self):
        log.debug("init jqdata")
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
    def get_price(stock_list, end_day, start_day):
        return get_price(stock_list, start_date=start_day,
                         end_date=end_day, frequency='daily', fq='pre',
                         fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit', 'low_limit', 'avg',
                                 'pre_close', 'paused'])

    @staticmethod
    def get_concepts():
        return get_concepts()

    @staticmethod
    def get_concept_stocks(concept_code, date=None):
        return get_concept_stocks(concept_code=concept_code, date=date)

    @staticmethod
    def get_industry(stock_code, date):
        return get_industry(stock_code, date)

    @staticmethod
    def get_industries(name):
        return get_industries(name=name)

    @staticmethod
    def get_industry_stocks(industry_code, date=datetime.datetime.today()):
        return get_industry_stocks(industry_code, date)

    @staticmethod
    def get_valuations(date, stock_list):
        return get_fundamentals(date=date, query_object=query(valuation)
                                .filter(valuation.code.in_(stock_list)))
