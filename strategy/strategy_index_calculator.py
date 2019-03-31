import pandas as pd
from strategy.base_strategy import BaseStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from config.config import *
from strategy.error import StrategyError


class IndexCalculatorStategy(BaseStrategy):

    def __init__(self):
        self.offline_stock_action = OfflineStockAction()
        BaseStrategy.__init__(self)

    def calculate_concept_index(self, concept_code):
        concept_stocks = self.offline_stock_action.query_stocks_by_concept(concept_code)
        stock_code_list = list(concept_stocks['stock_code'])
        stock_valuations = self.offline_stock_action.query_valuations(stock_code_list)
        stock_last_prices = self.offline_stock_action.query_last_prices(stock_code_list)
        stock_first_prices = self.offline_stock_action.query_first_prices(stock_code_list)
        stock_valuations.sort_values(by='code')
        stock_last_prices.sort_values(by='stock_code')

        temp = pd.merge(stock_last_prices, stock_valuations, left_on='stock_code',
                        right_on='code')
        total_cap = 0
        market_capital = 0
        for index, item in temp.iterrows():
            market_capital += item['market_cap'] #*10000*item['close']
            total_cap += item['capitalization']

        log.info('%s指数 -> %.2f',concept_stocks['concept_name'][0]
                 ,market_capital*100000000/(total_cap*10000))
        pass
