import unittest
from strategy.strategy_bull_up import BullUpStrategy


class TestStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.strategy_bull_up = BullUpStrategy()

    def test_bull_up(self):
        self.strategy_bull_up.list_bull_up_stock(self.strategy_bull_up.n5, 0.03)


if __name__ == "__main__":
    unittest.main()
