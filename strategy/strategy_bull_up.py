from strategy.base_strategy import BaseStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from config.config import *
from strategy.error import StrategyError


class BullUpStrategy(BaseStrategy):

    def __init__(self):
        self.stock_action = OfflineStockAction()
        BaseStrategy.__init__(self)

    def list_bull_up_stock(self, count, up_thread_hold):
        log.info("当前条件为, %s日下跌之后进行放量反弹，并且超过前日最高价%s%%", str(count-1),
                 str(up_thread_hold))
        stocks = self.stock_action.get_all_stock()
        stock_codes = stocks['stock_code']

        i = 1
        for stock_code in stock_codes:
            view_bar(i, len(stock_codes))
            i = i+1
            prices = self.stock_action.get_prices_by_stock_code_time(stock_code, count=count)

            if prices is None:
                raise StrategyError(str(count) + "日价格为空")

            if self.is_bull_up(prices, up_thread_hold):
                log.info("NOTICE ==> %s", str(stock_code))

    def is_bull_up(self, prices, thread_hold):
        if len(prices) < 4:
            raise StrategyError("时间太短")

        prices.sort_values(by="time", ascending=False)
        close_price = prices['close'][0]
        last_high = prices['high'][1]

        i = 1
        while i < len(prices)-1:
            i = i + 1
            if last_high < prices['high'][i]:
                last_high = prices['high'][i]
            else:
                return False

        if prices['volume'][0] > self.calculate_avg_vol(prices) \
                and close_price > prices['high'][1] * (1+thread_hold):
            return True

        return False

    @staticmethod
    def calculate_avg_vol(prices):
        avg_volume = prices['volume'].mean()
        return avg_volume






