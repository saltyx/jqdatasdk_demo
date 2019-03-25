import unittest
import jqdemo


class TestStockAction(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.stock_action = jqdemo.stock_action.StockAction()

    # def test_get_all_stock(self):
    #     self.stock_action.refresh_base_stock_info()
    #
    # def test_fresh_trade_day(self):
    #     self.stock_action.refresh_trade_days()
    #
    # def test_locked_share(self):
    #     self.stock_action.refresh_locked_share()

    def test_refresh_all_stock_price(self):
        self.stock_action.refresh_all_stock_price()


if __name__ == "__main__":
    unittest.main()
