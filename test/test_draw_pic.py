import datetime
import unittest
from strategy.strategy_indicator import IndicatorStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from jqdemo.stock_action import StockAction
from config.config import *


class TestDrawPic(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

    def test_draw_wave_buy_and_sell_point(self):
        print(datetime.datetime.today().strftime('%Y-%m-%d'))
        pass


if __name__ == '__main__':
    unittest.main()
