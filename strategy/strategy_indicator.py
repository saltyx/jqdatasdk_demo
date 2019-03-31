import talib
from strategy.base_strategy import BaseStrategy


class IndicatorStrategy(BaseStrategy):

    def __init__(self):
        BaseStrategy.__init__(self)

    @staticmethod
    def calculate_macd(stock_prices):
        return talib.MACD(stock_prices, fastperiod=12, slowperiod=26, signalperiod=9)

    @staticmethod
    def calculate_rsi(stock_close_prices):
        return talib.RSI(stock_close_prices, timeperiod=14)

    @staticmethod
    def calculate_cci(high, low, close):
        return talib.CCI(high, low, close, timeperiod=14)

    @staticmethod
    def calculate_dmi(high, low, close):
        return [talib.MINUS_DI(high, low, close, timeperiod=14),
                talib.PLUS_DI(high, low, close, timeperiod=14),
                talib.ADX(high, low, close, timeperiod=14)]
