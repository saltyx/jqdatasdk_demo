from backtesting.base_backtesting import BaseBackTesing
from jqdemo.offline_stock_action import OfflineStockAction
from strategy.strategy_indicator import IndicatorStrategy
from strategy.strategy_bull_up import BullUpStrategy
from config.config import *
import datetime
import pandas as pd


class SimpleBackTesting(BaseBackTesing):

    def __init__(self, stock_code):
        BaseBackTesing.__init__(self)
        self.stock_code = stock_code
        self.offline_stock_action = OfflineStockAction()
        self.bull_up_strategy = BullUpStrategy()
        self.indicator_strategy = IndicatorStrategy()
        self.total_dmi = None
        self.stock = None
        self.pressure_level = self.MAX_VALUE
        self.stop_loss_level = 0
        pass

    def is_buy_position(self, history_prices, current_price):
        history_prices = history_prices.append(current_price)
        # 判断是否是反弹时间点
        bull_up_list = self.bull_up_strategy\
            .list_bull_up_stock(count=4, up_thread_hold=0.03,
                                stock_list=self.stock,
                                end_day=current_price['trade_day'],
                                prices=history_prices[history_prices['trade_day']
                                                      <= current_price['trade_day']])

        if bull_up_list[0].empty is False:
            self.stock = bull_up_list[0]
            self.pressure_level = self.stock['pressure_price']
            self.stop_loss_level = self.stock['stop_loss_price']
            current_dmi = self.total_dmi[self.total_dmi['trade_day'] == current_price['trade_day']]
            print(current_price['trade_day'])
            if float(current_dmi['pdi'].tail(1)) > float(current_dmi['mdi'].tail(1)) \
                    and float(current_dmi['adx'].tail(1)) > 30:
                return True
        return False

    def buy_action(self, history_prices, current_price):
        self.buy_position_percent_value(current_price=current_price,
                                        percent=0.8)

    def is_sell_position(self, history_prices, current_price):
        return super().is_sell_position(history_prices, current_price)

    def sell_action(self, history_prices, current_price):
        super().sell_action(history_prices, current_price)

    def is_add_position(self, history_prices, current_price):
        if float(current_price['close']) > float(self.pressure_level) \
                and current_price['volume'] > history_prices.tail(5)['volume'].mean():
            return True
        return super().is_add_position(history_prices, current_price)

    #放量突破压力位，加仓20%
    def add_position_action(self, history_prices, current_price):
        self.stop_loss_level = self.pressure_level
        self.pressure_level = self.pressure_level * 1.05
        self.buy_position_percent_value(current_price=current_price,
                                        percent=0.6)

    def is_reduce_position(self, history_prices, current_price):
        if self.position > 0 and float(current_price['close']) < float(self.pressure_level)\
                < float(current_price['high']):
            return True
        return super().is_reduce_position(history_prices, current_price)

    #遇到压力位如果当天最高价超过，但是收盘没有超过则减仓50%
    def reduce_position_action(self, history_prices, current_price):
        self.sell_position_percent_value(current_price=current_price, percent=1)

    def is_clear_position(self, history_prices, current_price):
        if self.position > 0 and float(current_price['close']) < float(self.stop_loss_level):
            return True
        return super().is_clear_position(history_prices, current_price)

    # 到达止损位，清仓出局
    def clear_position_action(self, history_prices, current_price):
        self.sell_position_percent_value(current_price=current_price,
                                         percent=1)

    def buy_fee(self):
        return 5 #TODO 暂时固定按5元

    def sell_fee(self):
        return 5 #TODO 暂时固定按5元

    def end_backtesting(self, history_prices, current_price):
        if self.position > 0:
            self.sell_position_percent_value(current_price=current_price,
                                             percent=1)

    def run(self):
        self.stock = pd.DataFrame(self.offline_stock_action.query_by_stock_code(self.stock_code))
        total_history_prices = self.offline_stock_action.query_all_history_prices(
            self.stock_code)
        mdi, pdi, adx = self.indicator_strategy.calculate_dmi(total_history_prices['high'],
                                                              total_history_prices['low'],
                                                              total_history_prices['close'])
        dmis = {
            'mdi': mdi,
            'pdi': pdi,
            'adx': adx,
            'trade_day': total_history_prices['trade_day']
        }
        self.total_dmi = pd.DataFrame(dmis)
        super().run_backtesting(total_history_prices=total_history_prices,
                                start_date=datetime.datetime(2017, 1, 1))

        pass
