import unittest
from strategy.strategy_bull_up import BullUpStrategy
from strategy.strategy_indicator import IndicatorStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from config.config import *


class TestStrategy(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.strategy_bull_up = BullUpStrategy()
        self.indicator_strategy = IndicatorStrategy()
        self.offline_stock_action = OfflineStockAction()

    # def test_bull_up(self):
    # #     log.info("===============================================")
    #     result = self.strategy_bull_up.list_bull_up_stock(count=4, up_thread_hold=0.03)[0]
    #     log.info("===============================================")
        # result = self.strategy_bull_up.list_bull_up_stock(7, 0.03, result)[0]
        # log.info("===============================================")
        # result = self.strategy_bull_up.list_bull_up_stock(8, 0.03, result)[0]
        # log.info("===============================================")

    # def test_stock_concept(self):
    #     self

    # def test_dmi_indicator(self):

    # 找出放量突破布林线中轴
    # 高于昨日最高价3%以上
    # 当日K线实体部分至少占80%的
    # 认为有企稳信号
    def test_bollinger_band(self):
        stocks = self.offline_stock_action.query_all_stock()
        for index, stock in stocks.iterrows():
            all_prices = self.offline_stock_action.query_all_history_prices(stock['stock_code'])
            avg_vol = all_prices.tail(5)['volume'].mean() #5日均量
            newest_price = all_prices.tail(1)
            close_price = newest_price['close']
            newest_vol = newest_price['volume']
            newest_high = newest_price['high']
            newest_low = newest_price['low']
            newest_open = newest_price['open']

            last_high_price = all_prices.tail(2).head(1)['high']
            last_close_price = all_prices.tail(2).head(1)['close']
            if newest_high.item() > last_high_price.item()*1.03\
                and (close_price.item() - newest_open.item()) > 0.8*(newest_high.item() - newest_low.item())\
                and (newest_vol.item() > avg_vol.item()):
                upperband, middleband, lowerband = self.indicator_strategy.calculate_boll(all_prices['close'])
                if close_price.item() > middleband[len(middleband)-1] \
                        and last_close_price.item() < middleband[len(middleband)-2]:
                    log.info("stock_info: %s(%s) close_price:%.2f, +%.2f%%", stock['display_name'],stock['stock_code'],
                             close_price.item(), (close_price.item()-last_close_price.item())/last_close_price.item()*100)
                    log.info("upper :%.2f; middle: %.2f; lower: %.2f",
                             upperband[len(upperband)-1],
                             middleband[len(middleband)-1], lowerband[len(lowerband)-1])
                    log.info("======================================================")
            pass

if __name__ == "__main__":
    unittest.main()
