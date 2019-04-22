import datetime
import unittest
import pandas as pd
from strategy.strategy_indicator import IndicatorStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from jqdemo.stock_action import StockAction
from strategy.strategy_bull_up import BullUpStrategy
import threading
from config.config import *


class TestMACDStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.indicator_strategy = IndicatorStrategy()
        self.offline_stock_action = OfflineStockAction()
        self.bull_up_strategy = BullUpStrategy()

    # def test_dmi(self):
    #     stocks = self.offline_stock_action.get_all_stock()
    #     i = 1
    #     for index, stock in stocks.iterrows():
    #         price = self.offline_stock_action.query_all_history_prices(stock['stock_code'])
    #         m_di, p_di, adx = self.indicator_strategy.calculate_dmi(price['high'], price['low'], price['close'])
    #         if float(p_di.tail(1)) > float(m_di.tail(2).head(1)) \
    #                 and float(adx.tail(1)) > 30:
    #             log.info("NOTICE => %s", stock['stock_code'])
    #             view_bar(i, len(stocks.index))
    #         i += 1

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

    # def test_valuations(self):
    #     print(self.stock_action.refresh_valuations())
    #
    def test_concept(self):
        stock_action = StockAction()
        print(stock_action.refresh_concepts())

    def test_refresh_concept_stock(self):
        stock_action = StockAction()
        stock_action.refresh_concept_stocks()

    # def test_concept_stocks(self):
    #     # print(self.stock_action.refresh_concept_stocks())
    #     print(self.offline_stock_action.query_stock_concept('000027.XSHE'))

    def test_all_stock_history_price(self):
        stocks = self.offline_stock_action.query_all_stock()
        stocks_0 = stocks[0:600]
        stocks_1 = stocks[600:1200]
        stocks_2 = stocks[1200:1800]
        stocks_3 = stocks[1800:2400]
        stocks_4 = stocks[2400:3000]
        stocks_5 = stocks[3000:len(stocks)]

        thread_0 = threading.Thread(target=self.append_stock_price, args=(stocks_0,))
        thread_1 = threading.Thread(target=self.append_stock_price, args=(stocks_1,))
        thread_2 = threading.Thread(target=self.append_stock_price, args=(stocks_2,))
        thread_3 = threading.Thread(target=self.append_stock_price1, args=(stocks_3,))
        thread_4 = threading.Thread(target=self.append_stock_price1, args=(stocks_4,))
        thread_5 = threading.Thread(target=self.append_stock_price1, args=(stocks_5,))

        thread_0.setDaemon(True)
        thread_1.setDaemon(True)
        thread_2.setDaemon(True)
        thread_3.setDaemon(True)
        thread_4.setDaemon(True)
        thread_5.setDaemon(True)

        thread_0.start()
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()
        thread_5.start()

        thread_0.join()
        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
        thread_5.join()


    def append_stock_price(self, stocks):
        log.info("%s running", threading.get_ident())
        stock_codes = list(stocks['stock_code'])
        for i in range(len(stock_codes)):
            #view_bar(i+1, len(stock_codes), '(' + str(threading.get_ident())+')')
            stock_action = StockAction()
            stock_action.append_stock_price(stock_codes[i])
        log.info("%s done", threading.get_ident())

    def append_stock_price1(self, stocks):
        log.info("%s running", threading.get_ident())
        stock_codes = list(stocks['stock_code'])
        for i in range(len(stock_codes)):
            #view_bar(i+1, len(stock_codes), '(' + str(threading.get_ident())+')')
            stock_action = StockAction(user_name= '****', pwd='****')
            stock_action.append_stock_price(stock_codes[i])
        log.info("%s done", threading.get_ident())

    # def test_swing_backtesting(self):
    #     start_date = datetime.datetime(2019, 1, 1)
    #     stock_code = '000027.XSHE'
    #     price = self.offline_stock_action.query_all_history_prices(stock_code)
    #     # self.bull_up_strategy.
    #     pass


if __name__ == '__main__':
    unittest.main()
