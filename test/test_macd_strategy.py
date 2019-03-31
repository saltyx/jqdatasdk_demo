import datetime
import unittest
from strategy.strategy_indicator import IndicatorStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from jqdemo.stock_action import StockAction
from config.config import *


class TestMACDStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.indicator_strategy = IndicatorStrategy()
        self.offline_stock_action = OfflineStockAction()
        self.stock_action = StockAction()

    # def test_list_macd_gold(self):
    #     stocks = self.offline_stock_action.get_all_stock()
    #     log.info("======================================")
    #     for index, stock in stocks.iterrows():
    #         price = self.offline_stock_action.query_all_history_prices(stock['stock_code'])
    #         real = self.indicator_strategy.calculate_rsi(price['close'])
    #         cci = self.indicator_strategy.calculate_cci(price['high'], price['low'], price['close'])
    #         if float(price['paused'].tail(1)) <= 0:
    #             if int(cci.tail(1)) > 100 > int(cci.tail(2).head(1)):
    #                 log.info("NOTICE ==> %s CCI今日超过100", stock['stock_code'])
    #                 macd, macdsignal, macdhist = self.indicator_strategy.calculate_macd(price['close'])
    #                 if float(macdhist.tail(1)) > 0 > float(macdhist.tail(2).head(1)) and float(macd.tail(1)) > 0:
    #                     log.info("\t\tNOTICE ==> %s MACD金叉行情",stock['stock_code'])
    #                 if float(macd.tail(1)) > 0 > float(macd.tail(2).head(1)):
    #                     log.info("\t\tNOTICE ==> %s DIF>0行情", stock['stock_code'])

    def test_valuations(self):
        print(self.stock_action.refresh_valuations())

    # def test_concept(self):
    #     print(self.stock_action.refresh_concepts())

    # def test_concept_stocks(self):
    #     # print(self.stock_action.refresh_concept_stocks())
    #     print(self.offline_stock_action.query_stock_concept('000027.XSHE'))
    # # def test_all_stock_history_price(self):
    #     stocks = self.offline_stock_action.get_all_stock()
    #     stock_codes = list(stocks['stock_code'])
    #     print(stock_codes)
    #     for i in range(len(stock_codes)):
    #         view_bar(i, len(stock_codes))
    #         self.stock_action.append_stock_price(stock_codes[i])

if __name__ == '__main__':
    unittest.main()
