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

    @staticmethod
    def is_good_dmi(m_di, p_di, adx):
        if float(p_di) > float(m_di) and float(adx) > 30:
            return True
        return False

    @staticmethod
    def calculate_boll(close):
        upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        return upperband, middleband, lowerband
