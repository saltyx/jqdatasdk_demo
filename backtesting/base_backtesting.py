from abc import ABCMeta, abstractmethod
from config.config import *



class BaseBackTesing:

    def __init__(self):
        self.INIT_BALANCE = 30 * 1000
        self.MAX_VALUE = 9999
        self.position = 0
        self.profit_times = 0
        self.loss_time = 0
        self.profit_money = 0
        self.loss_money = 0
        self.cost_price = 0
        self.balance = self.INIT_BALANCE #默认30,000
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
        return 5

    @abstractmethod
    def sell_fee(self):
        return 5

    @abstractmethod
    def end_backtesting(self, history_prices, current_price):
        pass

        # 计算买入 percent仓位之后的账户属性

    def buy_position_percent_value(self, current_price, percent):
        if float(percent) < 0:
            raise Exception("can not buy below 0")
        if float(percent) > 1:
            log.warning("percent is set 1")
            percent = 1
        # 以close价格买入percent 仓
        close_price = current_price['close']
        # 计算余额可以买入的最大数量
        max_stock_num = (self.balance - self.buy_fee()) // (close_price * 100) * 100
        buy_num = max_stock_num * percent // 100 * 100
        if buy_num <= 0:
            log.warning("[%s]无法买入，余额不足，当前余额 : %.2f， 当前close：%.2f",
                        current_price['trade_day'], self.balance, close_price)
            log.warning("最大可买%.2f， 买入 %.2f, percent %.2f", max_stock_num, buy_num, percent)
        else:
            current_spend = close_price * buy_num + self.buy_fee()
            log.info("[%s]当前余额：%.2f\t买入后余额：%.2f\t能够买入最大数量 %d\t买入数量 %d\t买入单价%.2f",
                     current_price['trade_day'], self.balance,
                     self.balance - current_spend,
                     max_stock_num, buy_num, close_price)
            self.balance -= current_spend
            self.position += buy_num
            self.buy_fees += self.buy_fee()  # TODO
            self.buy_times += 1
            self.cost_price = (self.INIT_BALANCE - self.balance) / self.position
            log.info("[%s]买入成功，当前余额：%.2f\t持仓 %d\t成本价: %.2f", current_price['trade_day'],
                     self.balance, self.position, self.cost_price)

    def sell_position_percent_value(self, current_price, percent):
        if percent < 0:
            raise Exception("can not sell below 0")
        if percent > 1:
            log.warning("percent is set 1")
            percent = 1
        close_price = current_price['close']
        # 计算卖出数量
        sell_position = self.position * percent
        if sell_position == 0:
            log.warning("[%s]无法卖出，持仓为 0 ", current_price['trade_day'])
        else:
            added_balance = close_price * sell_position - self.sell_fee()
            self.balance += added_balance
            self.position = self.position - sell_position
            if self.position == 0:
                self.cost_price = 0
            else:
                self.cost_price = (self.INIT_BALANCE - self.balance) / self.position
            self.sell_times += 1
            self.sell_fees += self.sell_fee()
            log.info("[%s]卖出(%.2f)成功, 当前余额: %.2f\t仓位 %d\t成本价 %.2f", current_price['trade_day'],
                     current_price['close'], self.balance, self.position, self.cost_price)

    def run_backtesting(self, total_history_prices, start_date):
        trade_prices = total_history_prices[total_history_prices['trade_day'] >= start_date]\
            .sort_values(by='trade_day', ascending=True)
        his_prices = total_history_prices[total_history_prices['trade_day'] < start_date]\
            .sort_values(by='trade_day', ascending=True)

        for index, day in trade_prices.iterrows():
            if self.is_clear_position(his_prices, day):
                self.clear_position_action(his_prices, day)
            elif self.position <= 0 and self.is_buy_position(his_prices, day):
                self.buy_action(his_prices, day)

            if self.position > 0 and self.is_add_position(his_prices, day):
                self.add_position_action(his_prices, day)

            if self.position > 0 and self.is_reduce_position(his_prices, day):
                self.reduce_position_action(his_prices, day)

            if self.position > 0 and self.is_sell_position(his_prices, day):
                self.sell_action(his_prices, day)

            his_prices = his_prices.append(day)
            # view(str(his_prices['trade_day'].tail(1)))
            # print(day['trade_day'])
        # last_day = trade_prices.tail(1)
        self.end_backtesting(history_prices=his_prices, current_price=trade_prices.tail(1))
        # 如果当前持仓全部尾盘卖掉，计算盈利
        # log.info("回测结束，尾盘%.2f卖掉全部持仓，实现盈利为 %.2f", last_day['close'],
        #          (last_day['close']-self.cost_price)*self.position)
        log.info("回测结束，收益%.2f(%.2f%%)，买入%d次，卖出%d次", self.balance-self.INIT_BALANCE,
                 (self.balance-self.INIT_BALANCE)/self.INIT_BALANCE*100, self.buy_times, self.sell_times)
