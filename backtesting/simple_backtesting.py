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

        if bull_up_list[0].empty is False :
            current_dmi = self.total_dmi[self.total_dmi['trade_day'] == current_price['trade_day']]
            print(current_price['trade_day'])
            if float(current_dmi['pdi'].tail(1)) > float(current_dmi['mdi'].tail(1)) \
                    and float(current_dmi['adx'].tail(1)) > 30:
                return True
        return False

    def buy_action(self, history_prices, current_price):
        # 以close价格买入60%仓
        close_price = current_price['close']
        # 计算余额可以买入的最大数量
        max_stock_num = (self.balance-self.buy_fee())//(close_price*100) * 100
        buy_num = max_stock_num*0.6//100 * 100
        if buy_num <= 0:
            log.warning("[%s]无法买入，余额不足，当前余额 : %.2f， 当前close：%.2f", current_price['trade_day'], self.balance, close_price)
        else:
            current_spend = close_price*buy_num+self.buy_fee()
            log.info("[%s]当前余额：%.2f\t买入后余额：%.2f\t能够买入最大数量 %d\t买入数量 %d\t买入单价%.2f",
                     current_price['trade_day'], self.balance,
                     self.balance - current_spend,
                     max_stock_num, buy_num, close_price)
            total_spend = current_spend + self.position*self.cost_price

            self.balance -= current_spend
            self.position += buy_num
            self.buy_fees += self.buy_fee()  # TODO
            self.buy_times += 1
            self.cost_price = total_spend / self.position
            log.info("买入成功，当前余额：%.2f\t仓位 %d\t成本价: %.2f", self.balance,
                     self.position, self.cost_price)

    def is_sell_position(self, history_prices, current_price):
        return super().is_sell_position(history_prices, current_price)

    def sell_action(self, history_prices, current_price):
        super().sell_action(history_prices, current_price)

    def is_add_position(self, history_prices, current_price):
        return super().is_add_position(history_prices, current_price)

    #放量突破压力位，加仓20%
    def add_position_action(self, history_prices, current_price):
        super().add_position_action(history_prices, current_price)

    def is_reduce_position(self, history_prices, current_price):
        return super().is_reduce_position(history_prices, current_price)

    #遇到压力位如果当天最高价超过，但是收盘没有超过则减仓50%
    def reduce_position_action(self, history_prices, current_price):
        super().reduce_position_action(history_prices, current_price)

    def is_clear_position(self, history_prices, current_price):
        return super().is_clear_position(history_prices, current_price)

    # 到达止损位，清仓出局
    def clear_position_action(self, history_prices, current_price):
        super().clear_position_action(history_prices, current_price)

    def buy_fee(self):
        return 5 #TODO 暂时固定按5元

    def sell_fee(self):
        return 5 #TODO 暂时固定按5元

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
                                start_date=datetime.datetime(2019, 1, 1))

        pass
