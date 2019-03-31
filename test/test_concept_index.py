import unittest
import datetime
import unittest
from strategy.strategy_index_calculator import IndexCalculatorStategy
from jqdemo.offline_stock_action import OfflineStockAction
from jqdemo.stock_action import StockAction
from config.config import *


class TestConceptIndex(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.index_strategy = IndexCalculatorStategy()
        self.offline_stock_action = OfflineStockAction()

    def test_concept_index(self):
        self.index_strategy.calculate_concept_index('GN086')
        pass


if __name__ == '__main__':
    unittest.main()