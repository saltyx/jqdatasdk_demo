import pandas as pd
from strategy.base_strategy import BaseStrategy
from jqdemo.offline_stock_action import OfflineStockAction
from config.config import *
from strategy.error import StrategyError
from strategy.strategy_indicator import IndicatorStrategy


class BullUpStrategy(BaseStrategy):

    def __init__(self):
        self.stock_action = OfflineStockAction()
        self.indicator_strategy = IndicatorStrategy()
        BaseStrategy.__init__(self)

    def list_bull_up_stock(self, count, up_thread_hold, stock_list=None, end_day=get_today(),
                           prices=None, safe_flag=False):
        log.debug("当前条件为, %s日下跌之后进行放量反弹，并且超过前日最高价%s%%", str(count - 1),
                  str(up_thread_hold * 100))
        if stock_list is None:
            stock_list = self.stock_action.query_all_stock()
            # stock_code_list = stocks['stock_code']

        result = pd.DataFrame()
        result_price = pd.DataFrame()
        i = 1
        for index, stock in stock_list.iterrows():
            i = i+1
            if prices is None:
                prices = self.stock_action.query_prices_by_stock_code_time(stock['stock_code'],
                                                                           count=count,
                                                                           end_date=end_day)
            else:
                pass
            if prices is None:
                raise StrategyError(str(count) + "日价格为空")
            ratio = self.is_bull_up(prices, up_thread_hold, count)
            if ratio is not None:
                is_clash_the_top = False
                str_f = "NOTICE ==> %s\n[%s 当前收盘 %s(最高价 %s) 涨幅 %.2f%%(最高涨幅 %.2f%%) " \
                        "建议止损位 %s 压力位 %s"
                if ratio[3]*100 > 9.6 and ratio[1]*100 < ratio[3]*100:
                    is_clash_the_top = True
                    if safe_flag is False:
                        # 忽略掉开板股票
                        log.info(str_f + " 警惕开板风险]", str(stock['stock_code']),
                                 str(stock['display_name']),
                                 str(ratio[0]), str(ratio[2]), ratio[1] * 100, ratio[3] * 100, ratio[4], ratio[5])

                elif ratio[0] == ratio[2]:
                    log.info(str_f + " 强势光头阳，值得关注]", str(stock['stock_code']),
                             str(stock['display_name']),
                             str(ratio[0]), str(ratio[2]), ratio[1] * 100, ratio[3] * 100, ratio[4], ratio[5])
                else:
                    log.info(str_f + "]", str(stock['stock_code']),
                             str(stock['display_name']),
                             str(ratio[0]), str(ratio[2]), ratio[1] * 100, ratio[3] * 100, ratio[4], ratio[5])

                stock['stop_loss_price'] = ratio[4]
                stock['pressure_price'] = ratio[5]
                if safe_flag is False or is_clash_the_top is False:
                    result = result.append(stock)
                result_price = result_price.append(prices)
        return [result, result_price]

    def is_bull_up(self, prices, thread_hold, count):
        if len(prices) < 4:
            log.warning("%s时间太短", str(prices['stock_code'][0]))
            return None
        prices.sort_values(by="trade_day", ascending=False, inplace=True)
        prices = prices.reset_index(drop=True)
        close_price = prices['close'][0]
        high_price = prices['high'][0]
        last_high = prices['high'][1]
        last_close = prices['close'][1]

        take_profit_price = 0

        i = 1
        while i < len(prices)-1:
            i = i + 1
            if last_high < prices['high'][i]:
                last_high = prices['high'][i]
            else:
                take_profit_price = last_high
                break

        if i > (count - 1) and prices['volume'][0] > self.calculate_avg_vol(prices) \
                and close_price > prices['high'][1] * (1+thread_hold):
            # TODO 找出来近期高位
            return [close_price, close_price/prices['close'][1]-1, high_price,
                    high_price/prices['close'][1]-1, last_close, take_profit_price]

        return None

    @staticmethod
    def calculate_avg_vol(prices):
        avg_volume = prices['volume'].mean()
        return avg_volume






