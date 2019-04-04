from backtesting.cci_backtesting import CCIBacktesing
from backtesting.simple_backtesting import SimpleBackTesting
from jqdemo.offline_stock_action import OfflineStockAction
import pandas as pd
import datetime
import unittest


class TestBacktesing(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.offline_stock_action = OfflineStockAction()

    # def test_simple_backtesting(self):
    #     stocks = self.offline_stock_action.get_all_stock()
    #     sample_stocks = stocks.sample(100)
    #     stock_codes = []
    #     profits = []
    #     for index, stock in sample_stocks.iterrows():
    #         simple_backtesting = SimpleBackTesting()
    #         simple_backtesting.set_stock_code(stock['stock_code'])
    #         profit = simple_backtesting.run()
    #         stock_codes.append(stock['stock_code'])
    #         profits.append(profit)
    #     sample = {
    #         'stock_code': stock_codes,
    #         'profit': profits
    #     }
    #     sample_result = pd.DataFrame(sample)
    #     sample_result.to_excel('./result/simple_backtesting-' +
    #                            str(datetime.datetime.strftime(
    #                                datetime.datetime.now(), '%Y%m%d%H%M%S'
    #                            )) +'.xlsx')

    def test_cci_backtesting(self):
        stocks = self.offline_stock_action.get_all_stock()
        sample_stocks = stocks.sample(20)
        stock_codes = []
        profits = []
        for index, stock in sample_stocks.iterrows():
            cci_backtesting = CCIBacktesing()
            cci_backtesting.set_stock_code(stock['stock_code'])
            profit = cci_backtesting.run()
            stock_codes.append(stock['stock_code'])
            profits.append(profit)
        sample = {
            'stock_code': stock_codes,
            'profit': profits
        }
        sample_result = pd.DataFrame(sample)
        sample_result.to_excel('./result/cci_backtesting-' +
                               str(datetime.datetime.strftime(
                                   datetime.datetime.now(), '%Y%m%d%H%M%S'
                               )) +'.xlsx')

if __name__ == '__main__':
    unittest.main()
