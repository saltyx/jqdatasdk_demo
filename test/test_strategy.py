import unittest
from strategy.strategy_bull_up import BullUpStrategy
from strategy.strategy_indicator import IndicatorStrategy
from config.config import *


class TestStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.strategy_bull_up = BullUpStrategy()
        self.indicator_strategy = IndicatorStrategy()

    def test_bull_up(self):
        log.info("===============================================")
        result = self.strategy_bull_up.list_bull_up_stock(count=4, up_thread_hold=0.03)[0]
        log.info("===============================================")
        # result = self.strategy_bull_up.list_bull_up_stock(7, 0.03, result)[0]
        # log.info("===============================================")
        # result = self.strategy_bull_up.list_bull_up_stock(8, 0.03, result)[0]
        # log.info("===============================================")

    # def test_stock_concept(self):
    #     self

    # def test_dmi_indicator(self):

if __name__ == "__main__":
    unittest.main()
