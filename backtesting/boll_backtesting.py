from backtesting.base_backtesting import BaseBackTesing
from jqdemo.offline_stock_action import OfflineStockAction
from strategy.strategy_indicator import IndicatorStrategy
from strategy.strategy_bull_up import BullUpStrategy
from config.config import *
import datetime
import pandas as pd


class BollBacktesting(BaseBackTesing):

    def __init__(self):
        super().__init__()
        self.stock_code = None
        self.offline_stock_action = OfflineStockAction()
        self.indicator_strategy = IndicatorStrategy()
        self.boll = None
        self.stock = None
        self.buy_date = None

    def set_stock_code(self, stock_code):
        self.stock_code = stock_code

    def is_buy_position(self, history_prices, current_price):
        all_prices = history_prices
        avg_vol = all_prices.tail(5)['volume'].mean()  # 5日均量
        newest_price = all_prices.tail(1)
        close_price = newest_price['close']
        newest_vol =  newest_price['volume']
        newest_high = newest_price['high']
        newest_low =  newest_price['low']
        newest_open = newest_price['open']

        last_high_price = all_prices.tail(2).head(1)['high']
        last_close_price = all_prices.tail(2).head(1)['close']
        try:
            if newest_high.item() > last_high_price.item() * 1.03 \
                    and (close_price.item() - newest_open.item()) > 0.8 * (newest_high.item() - newest_low.item()) \
                    and (newest_vol.item() > avg_vol.item()):
                upperband = self.boll['upperband']
                middleband = self.boll['middleband']
                lowerband = self.boll['lowerband']
                if close_price.item() > middleband[len(middleband) - 1] \
                        and last_close_price.item() < middleband[len(middleband) - 2]:
                    log.info("stock_info: %s(%s) close_price:%.2f, +%.2f%%", self.stock['display_name'],
                             self.stock['stock_code'],
                             close_price.item(),
                             (close_price.item() - last_close_price.item()) / last_close_price.item() * 100)
                    log.info("upper :%.2f; middle: %.2f; lower: %.2f",
                             upperband[len(upperband) - 1],
                             middleband[len(middleband) - 1], lowerband[len(lowerband) - 1])
                    log.info("======================================================")
                    self.buy_date = datetime.datetime.strptime(str(current_price['trade_day']).split(" ")[0],
                                                               '%Y-%m-%d')
                    return True
        except ValueError:
            print(newest_high)
            return False
        return False

    def buy_action(self, history_prices, current_price):
        self.buy_position_percent_value(current_price, 1)

    def is_sell_position(self, history_prices, current_price):
        if self.buy_date is not None \
                and self.position > 0:
            cur_date = datetime.datetime.strptime(str(current_price['trade_day']).split(" ")[0],
                                                  '%Y-%m-%d')
            print((cur_date - self.buy_date).days)
            if (cur_date - self.buy_date).days > 3:
                self.buy_date = None
                log.info("持有超过2天，卖出")
                return True
        return False

    def sell_action(self, history_prices, current_price):
        self.sell_position_percent_value(current_price, 1)

    def is_add_position(self, history_prices, current_price):
        super().is_add_position(history_prices, current_price)

    def add_position_action(self, history_prices, current_price):
        super().add_position_action(history_prices, current_price)

    def is_reduce_position(self, history_prices, current_price):
        super().is_reduce_position(history_prices, current_price)

    def reduce_position_action(self, history_prices, current_price):
        super().reduce_position_action(history_prices, current_price)

    def is_clear_position(self, history_prices, current_price):
        if self.position > 0:
            profit = self.position*current_price['open'] - self.INIT_BALANCE
            print(profit)
            if profit < 0 and (-profit)/self.INIT_BALANCE > 0.08:
                log.info("触及止损，清仓")
                return True
        return False

    def clear_position_action(self, history_prices, current_price):
        super().sell_position_percent_value(current_price=current_price,
                                            percent=1)

    def buy_fee(self):
        return super().buy_fee()

    def sell_fee(self):
        return super().sell_fee()

    def end_backtesting(self, history_prices, current_price):
        if self.position > 0:
            self.sell_position_percent_value(current_price, 1)

    def buy_position_percent_value(self, current_price, percent):
        # 早盘就卖
        current_price['close'] = current_price['open']
        return super().buy_position_percent_value(current_price, percent)

    def sell_position_percent_value(self, current_price, percent):
        return super().sell_position_percent_value(current_price, percent)

    def run(self):
        if self.stock_code is None:
            raise Exception("stock code can not be None")
        self.stock = pd.DataFrame(self.offline_stock_action.query_by_stock_code(self.stock_code))
        total_history_prices = self.offline_stock_action.query_all_history_prices(
            self.stock_code)
        upperband, middleband, lowerband = self.indicator_strategy.calculate_boll(total_history_prices['close'])

        bollinger = {
            'upperband' : upperband,
            'middleband': middleband,
            'lowerband': lowerband,
            'trade_day': total_history_prices['trade_day']
        }

        self.boll = pd.DataFrame(bollinger)
        super().run_backtesting(total_history_prices=total_history_prices,
                                start_date=datetime.datetime(2018, 1, 1))
        return float(round((self.balance - self.INIT_BALANCE)/self.INIT_BALANCE*100, 2))