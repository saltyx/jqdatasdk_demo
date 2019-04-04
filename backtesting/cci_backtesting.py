from backtesting.base_backtesting import BaseBackTesing
from jqdemo.offline_stock_action import OfflineStockAction
from strategy.strategy_indicator import IndicatorStrategy
from strategy.strategy_bull_up import BullUpStrategy
from config.config import *
import datetime
import pandas as pd


class CCIBacktesing(BaseBackTesing):

    def __init__(self):
        BaseBackTesing.__init__(self)
        self.stock_code = None
        self.offline_stock_action = OfflineStockAction()
        self.indicator_strategy = IndicatorStrategy()
        self.cci = None
        self.stock = None

    def set_stock_code(self, stock_code):
        self.stock_code = stock_code

    def is_buy_position(self, history_prices, current_price):
        pre_price = history_prices.tail(1)
        pre_price = pre_price.reset_index(drop=True)
        pre_cci = self.cci[self.cci['trade_day'] == pre_price['trade_day'][0]]
        cur_cci = self.cci[self.cci['trade_day'] == current_price['trade_day']]
        if float(pre_cci['cci']) < 100 < float(cur_cci['cci']):
            return True
        return False

    def buy_action(self, history_prices, current_price):
        cur_cci = self.cci[self.cci['trade_day'] == current_price['trade_day']]
        self.buy_position_percent_value(current_price=current_price,
                                        percent=float(cur_cci['cci'])/100-1)

    def is_sell_position(self, history_prices, current_price):
        pre_price = history_prices.tail(1)
        pre_price = pre_price.reset_index(drop=True)
        pre_cci = self.cci[self.cci['trade_day'] == pre_price['trade_day'][0]]
        cur_cci = self.cci[self.cci['trade_day'] == current_price['trade_day']]
        if float(pre_cci['cci']) > 100 > float(cur_cci['cci']):
            return True
        return False

    def sell_action(self, history_prices, current_price):
        if self.position > 0:
            self.sell_position_percent_value(current_price=current_price,
                                             percent=1)

    def is_add_position(self, history_prices, current_price):
        super().is_add_position(history_prices=history_prices, current_price=current_price)

    def add_position_action(self, history_prices, current_price):
        super().add_position_action(history_prices=history_prices, current_price=current_price)

    def is_reduce_position(self, history_prices, current_price):
        super().is_reduce_position(history_prices=history_prices, current_price=current_price)

    def reduce_position_action(self, history_prices, current_price):
        super().reduce_position_action(history_prices=history_prices, current_price=current_price)

    def is_clear_position(self, history_prices, current_price):
        if self.position > 0:
            profit = self.balance - self.INIT_BALANCE
            if profit < 0 and (-profit)/self.INIT_BALANCE > 0.08:
                return True
        return False

    def clear_position_action(self, history_prices, current_price):
        super().sell_position_percent_value(current_price=current_price,
                                            percent=1)

    def buy_fee(self):
        return 5

    def sell_fee(self):
        return 5

    def end_backtesting(self, history_prices, current_price):
        if self.position > 0:
            self.sell_position_percent_value(current_price=current_price,
                                             percent=1)

    def buy_position_percent_value(self, current_price, percent):
        super().buy_position_percent_value(current_price, percent)

    def sell_position_percent_value(self, current_price, percent):
        super().sell_position_percent_value(current_price, percent)

    def run(self):
        if self.stock_code is None:
            raise Exception("stock code can not be None")
        self.stock = pd.DataFrame(self.offline_stock_action.query_by_stock_code(self.stock_code))
        total_history_prices = self.offline_stock_action.query_all_history_prices(
            self.stock_code)
        ccis = self.indicator_strategy.calculate_cci(total_history_prices['high'],
                                                     total_history_prices['low'],
                                                     total_history_prices['close'])
        cci = {
            'cci': ccis,
            'trade_day': total_history_prices['trade_day']
        }

        self.cci = pd.DataFrame(cci)
        super().run_backtesting(total_history_prices=total_history_prices,
                                start_date=datetime.datetime(2018, 1, 1))
        return float(round((self.balance - self.INIT_BALANCE)/self.INIT_BALANCE*100, 2))
