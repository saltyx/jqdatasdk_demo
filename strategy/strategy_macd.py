import talib
from strategy.base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):

    def __init__(self):
        BaseStrategy.__init__(self)

    @staticmethod
    def calculate(stock_prices):
        return talib.MACD(stock_prices, fastperiod=12, slowperiod=26, signalperiod=9)
