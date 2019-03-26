import datetime
import unittest
from strategy.strategy_macd import MACDStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from jqdemo.stock_action import StockAction


class TestMACDStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.macd_strategy = MACDStrategy()
        self.offline_stock_action = OfflineStockAction()
        self.stock_action = StockAction()

    def test_macd_calculate(self):
        stocks = []
        stock = self.offline_stock_action.query_by_stock_code('600031.XSHG')
        stocks.append(stock)
        print(stocks[0]['start_date'])
        stock_prices = self.stock_action.refresh_total_stock_price(stocks)

        self.stock_action.refresh_total_stock_price(stock)



        # print(stock_prices['close'])
        # macd, macdsignal, macdhist = self.macd_strategy.calculate(stock_prices['close'])
        # print(macd[len(macd)-1])
        # print(macdsignal[len(macdsignal)-1])
        # print(macdhist[len(macdhist)-1])


if __name__ == '__main__':
    unittest.main()
