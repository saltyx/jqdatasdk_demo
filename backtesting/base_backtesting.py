from abc import ABCMeta, abstractmethod
from config.config import *


class BaseBackTesing:

    def __init__(self):
        self.position = 0
        self.profit_times = 0
        self.loss_time = 0
        self.profit_money = 0
        self.loss_money = 0
        self.cost_price = 0
        self.balance = 30*1000 #默认30,000
        self.buy_fees = 0
        self.sell_fees = 0
        self.sell_times = 0
        self.buy_times = 0

    @abstractmethod
    def is_buy_position(self, history_prices, current_price):
        return True

    @abstractmethod
    def buy_action(self, history_prices, current_price):
        pass

    @abstractmethod
    def is_sell_position(self, history_prices, current_price):
        return False

    @abstractmethod
    def sell_action(self, history_prices, current_price):
        pass

    @abstractmethod
    def is_add_position(self, history_prices, current_price):
        return False

    @abstractmethod
    def add_position_action(self, history_prices, current_price):
        pass

    @abstractmethod
    def is_reduce_position(self, history_prices, current_price):
        return False

    @abstractmethod
    def reduce_position_action(self, history_prices, current_price):
        pass

    @abstractmethod
    def is_clear_position(self, history_prices, current_price):
        return False

    @abstractmethod
    def clear_position_action(self, history_prices, current_price):
        pass

    @abstractmethod
    def buy_fee(self):
        pass

    @abstractmethod
    def sell_fee(self):
        pass

    def run_backtesting(self, total_history_prices, start_date):
        trade_prices = total_history_prices[total_history_prices['trade_day'] >= start_date]\
            .sort_values(by='trade_day', ascending=True)
        his_prices = total_history_prices[total_history_prices['trade_day'] < start_date]\
            .sort_values(by='trade_day', ascending=True)

        for index, day in trade_prices.iterrows():
            if self.is_buy_position(his_prices, day):
                self.buy_action(his_prices, day)

            elif self.is_add_position(his_prices, day):
                self.add_position_action(his_prices, day)

            elif self.is_reduce_position(his_prices, day):
                self.reduce_position_action(his_prices, day)

            elif self.is_sell_position(his_prices, day):
                self.sell_action(his_prices, day)

            elif self.is_clear_position(his_prices, day):
                self.clear_position_action(his_prices, day)

            his_prices = his_prices.append(day)
            # view(str(his_prices['trade_day'].tail(1)))
            # print(day['trade_day'])
        last_day = trade_prices.tail(1)
        # 如果当前持仓全部尾盘卖掉，计算盈利
        log.info("回测结束，尾盘%.2f卖掉全部持仓，实现盈利为 %.2f", last_day['close'],
                 (last_day['close']-self.cost_price)*self.position)
