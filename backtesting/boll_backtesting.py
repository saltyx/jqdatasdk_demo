from backtesting.base_backtesting import BaseBackTesing
from jqdemo.offline_stock_action import OfflineStockAction
from strategy.strategy_indicator import IndicatorStrategy
from strategy.strategy_bull_up import BullUpStrategy
from config.config import *
import datetime
import pandas as pd


class BollBacktesting(BaseBackTesing):

    def __init__(self):
        self.stock_code = None
        self.offline_stock_action = OfflineStockAction()
        self.indicator_strategy = IndicatorStrategy()
        self.boll = None
        self.stock = None

    def is_buy_position(self, history_prices, current_price):
        pass

    def buy_action(self, history_prices, current_price):
        pass

    def is_sell_position(self, history_prices, current_price):
        pass

    def sell_action(self, history_prices, current_price):
        pass

    def is_add_position(self, history_prices, current_price):
        pass

    def add_position_action(self, history_prices, current_price):
        pass

    def is_reduce_position(self, history_prices, current_price):
        pass

    def reduce_position_action(self, history_prices, current_price):
        pass

    def is_clear_position(self, history_prices, current_price):
        pass

    def clear_position_action(self, history_prices, current_price):
        pass

    def buy_fee(self):
        pass

    def sell_fee(self):
        pass

    def end_backtesting(self, history_prices, current_price):
        pass

    def buy_position_percent_value(self, current_price, percent):
        return super().buy_position_percent_value(current_price, percent)

    def sell_position_percent_value(self, current_price, percent):
        return super().sell_position_percent_value(current_price, percent)

    def run(self):
        pass
