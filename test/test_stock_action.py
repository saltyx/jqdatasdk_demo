import unittest
import jqdemo


class TestStockAction(unittest.TestCase):

    def test_get_all_stock(self):
        stock_action = jqdemo.stock_action.StockAction()
        stock_action.refresh_locked_share()


if __name__ == "__main__":
    unittest.main()
