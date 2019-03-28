import pandas as pd
from strategy.base_strategy import BaseStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from config.config import *
from strategy.error import StrategyError


class BullUpStrategy(BaseStrategy):

    def __init__(self):
        self.stock_action = OfflineStockAction()
        BaseStrategy.__init__(self)

    # def list_bull_up_stock(self, count, up_thread_hold):
    #     log.info("当前条件为, %s日下跌之后进行放量反弹，并且超过前日最高价%s%%", str(count-1),
    #              str(up_thread_hold*100))
    #     stocks = self.stock_action.get_all_stock()
    #     stock_codes = stocks['stock_code']
    #     result = []
    #     i = 1
    #     for stock_code in stock_codes:
    #         view_bar(i, len(stock_codes))
    #         i = i+1
    #         prices = self.stock_action.get_prices_by_stock_code_time(stock_code, count=count)
    #
    #         if prices is None:
    #             raise StrategyError(str(count) + "日价格为空")
    #
    #         if self.is_bull_up(prices, up_thread_hold):
    #             result.append(stock_code)
    #             log.info("NOTICE ==> %s", str(stock_code))
    #     return result

    def list_bull_up_stock(self, count, up_thread_hold, stock_list=None):
        log.info("当前条件为, %s日下跌之后进行放量反弹，并且超过前日最高价%s%%", str(count - 1),
                 str(up_thread_hold * 100))
        if stock_list is None:
            stock_list = self.stock_action.get_all_stock()
            # stock_code_list = stocks['stock_code']

        result = pd.DataFrame()
        i = 1
        for index, stock in stock_list.iterrows():
            view_bar(i, len(stock_list.index))
            i = i+1
            prices = self.stock_action.get_prices_by_stock_code_time(stock['stock_code'], count=count)

            if prices is None:
                raise StrategyError(str(count) + "日价格为空")
            ratio = self.is_bull_up(prices, up_thread_hold)
            if ratio is not None:
                log.info("NOTICE ==> %s[%s 当前收盘 %s 涨幅 %.2f%%]", str(stock['stock_code']), str(stock['display_name']),
                         str(ratio[0]), ratio[1]*100)
                result.append(stock)
        return result

    def is_bull_up(self, prices, thread_hold):
        if len(prices) < 4:
            log.warning("%s时间太短", str(prices['stock_code'][0]))
            return None

        prices.sort_values(by="trade_day", ascending=False)
        close_price = prices['close'][0]
        last_high = prices['high'][1]

        i = 1
        while i < len(prices)-1:
            i = i + 1
            if last_high < prices['high'][i]:
                last_high = prices['high'][i]
            else:
                return None

        if prices['volume'][0] > self.calculate_avg_vol(prices) \
                and close_price > prices['high'][1] * (1+thread_hold):
            return [close_price, close_price/prices['close'][1]-1]

        return None

    @staticmethod
    def calculate_avg_vol(prices):
        avg_volume = prices['volume'].mean()
        return avg_volume






