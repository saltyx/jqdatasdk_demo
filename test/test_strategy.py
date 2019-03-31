import unittest
from strategy.strategy_bull_up import BullUpStrategy


class TestStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.strategy_bull_up = BullUpStrategy()

    # def test_bull_up(self):
    #     print("===============================================")
    #     result = self.strategy_bull_up.list_bull_up_stock(count=6, up_thread_hold=0.03)[0]
    #     print("===============================================")
    #     result = self.strategy_bull_up.list_bull_up_stock(7, 0.03, result)[0]
    #     print("===============================================")
    #     result = self.strategy_bull_up.list_bull_up_stock(8, 0.03, result)[0]
    #     print("===============================================")

    # def test_stock_concept(self):
    #     self


if __name__ == "__main__":
    unittest.main()
