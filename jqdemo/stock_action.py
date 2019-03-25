import pandas as pd
import datetime
from jqdemo.mongo_base import MongoBase
from jqdemo.jqdatasdk_base import JQDataBase
import jqdemo.config
import numpy as np


class StockAction(MongoBase, JQDataBase):

    def __init__(self):
        MongoBase.__init__(self)
        JQDataBase.__init__(self)

    def refresh_base_stock_info(self):
        self.db.base_stock.delete_many({})
        self.db.base_stock.insert_many(self.get_all_stocks().to_dict('record'))
        self.db.stock_config.delete_many({})
        self.db.stock_config.insert_one({"updated_time": datetime.datetime.today()})

    def refresh_trade_days(self):
        self.db.trade_days.delete_many({})
        self.db.trade_days.insert_many(self.get_all_trade_days().to_dict('record'))
        self.db.trade_day_config.delete_many({})
        self.db.trade_day_config.insert_one({"updated_time": datetime.datetime.today()})

    def refresh_locked_share(self):
        stocks = pd.DataFrame(list(self.db.base_stock.find({"type": "stock"})))
        locked_share = self.get_locked_share(list(stocks["stock_code"]),
                                             start_day=datetime.datetime.today())
        self.db.locked_share.delete_many({})
        self.db.locked_share.insert_many(locked_share.to_dict('record'))
        self.db.locked_share_config.delete_many({})
        self.db.locked_share_config.insert_one({"updated_time": datetime.datetime.today()})

    def refresh_all_stock_price(self):
        self.db.price.delete_many({})

        stock_codes = list(self.get_all_stock()['stock_code'])
        stock_code_cut = np.array_split(stock_codes, 50)
        for i in range(len(stock_code_cut)):
            jqdemo.config.view_bar(i+1, 50)
            prices = self.get_price(list(stock_code_cut[i]), end_day=datetime.datetime.today())
            self.db.price.insert_many(prices.to_dict('record'))

        self.db.price_config.delete_many({})
        self.db.price_config.insert_one({"updated_time": datetime.datetime.today()})

    def get_all_stock(self):
        return pd.DataFrame(list(self.db.base_stock.find({"type": "stock"})))

    def query_by_stock_code(self, stock_code):
        return self.db.base_stock.find_one({"stock_code": {"$regex": stock_code + ".*"}})

    def query_n_trade_days_before_today(self, n):
        today = datetime.datetime.today()
        result = self.db.trade_days.find({"trade_day": {"$lte": today}}) \
            .sort([("trade_day", -1)]).limit(n)
        return result

    def get_last_updated_time_of_stock(self):
        return self.db.stock_config.find_one()['updated_time']

    def get_last_updated_time_of_trade_day(self):
        return self.db.trade_day_config.find_one()['updated_time']

    def get_last_updated_time_of_locked_share(self):
        return self.db.locked_share_config.find_one()['updated_time']

    def __del__(self):
        MongoBase.__del__(self)
