from mongo_base import MongoBase
import datetime


class StockMongo(MongoBase):

    def refresh_base_stock_info(self, df):
        self.db.base_stock.remove({})
        self.db.base_stock.insert(df.to_dict('record'))
        self.db.stock_config.remove({})
        self.db.stock_config.insert({"updated_time" : datetime.datetime.today()})

    def query_by_stock_code(self, stock_code):
        return self.db.base_stock.find_one({"stock_code" : {"$regex" : stock_code+".*"}})

    def refresh_trade_days(self, trade_days):
        self.db.trade_days.remove({})
        self.db.trade_days.insert(trade_days.to_dict('record'))
        self.db.trade_day_config.insert({"updated_time": datetime.datetime.today()})

    def query_n_trade_days_before_today(self, n):
        today = datetime.datetime.today()
        result = self.db.trade_days.find({"trade_day" : { "$lte" : today } }) \
            .sort([("trade_day", -1)]).limit(n)
        return result

    def get_last_updated_time_of_stock(self):
        return self.db.stock_config.find_one()['updated_time']

    def get_last_updated_time_of_trade_day(self):
        return self.db.trade_day_config.find_one()['updated_time']