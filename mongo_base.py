import pymongo as mongo
import json
import datetime


class MongoBase:

    def __init__(self):
        self.db_client = mongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client.jqdata

    def refresh_base_stock_info(self, df):
        self.db.base_stock.remove({})
        self.db.base_stock.insert(df.to_dict('record'))

    def query_by_stock_code(self, stock_code):
        return self.db.base_stock.find_one({"stock_code" : {"$regex" : stock_code+".*"}})

    def refresh_trade_days(self, trade_days):
        self.db.trade_days.remove({})
        self.db.trade_days.insert(trade_days.to_dict('record'))

    def query_n_trade_days_before_today(self, n):
        today = datetime.datetime.today()
        result = self.db.trade_days.find({"trade_day" : { "$lte" : today } }) \
            .sort([("trade_day", -1)]).limit(n)
        return result

    def close(self):
        self.db_client.close()