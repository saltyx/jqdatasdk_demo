from jqdemo.base_mongo import BaseMongo
import datetime
import pandas as pd
from config.config import *


class OfflineStockAction(BaseMongo):

    def __init__(self):
        BaseMongo.__init__(self)

    def get_prices_by_stock_code_time(self, stock_code, count, end_date=get_today()):
        return pd.DataFrame(list(self.db.total_stock_price.find({"stock_code": stock_code, "trade_day": {"$lte": end_date}})
                            .sort([("trade_day", -1)]).limit(count)))

    def get_all_stock(self):
        return pd.DataFrame(list(self.db.base_stock.find({"type": "stock"})))

    def query_by_stock_code(self, stock_code):
        return self.db.base_stock.find_one({"stock_code": {"$regex": stock_code + ".*"}})

    def query_price_by_stock_code(self, stock_code):
        return self.db.price.find({"stock_code": {"$regex": stock_code+".*"}})

    def query_n_trade_days_before_today(self, count):
        today = datetime.datetime.today()
        result = self.db.trade_days.find({"trade_day": {"$lte": today}}) \
            .sort([("trade_day", -1)]).limit(count)
        return result

    def query_all_history_prices(self, stock_code):
        return pd.DataFrame(list(self.db.total_stock_price.find({"stock_code": stock_code})))

    def query_all_concepts(self):
        return pd.DataFrame(list(self.db.concepts.find({})))

    def query_stock_concept(self, stock_code):
        return list(self.db.concept_stock_code.find({'stock_code': stock_code}))

    def query_stocks_by_concept(self, concept_code):
        return pd.DataFrame(list(self.db.concept_stock_code.find({'concept_code': concept_code})))

    def query_valuations(self, stock_code_list):
        return pd.DataFrame(list(self.db.stock_valuations.find({'code' : {'$in': stock_code_list}})))

    def query_last_prices(self, stock_list):
        trade_day = pd.DataFrame(list(self.query_n_trade_days_before_today(1)))['trade_day'][0]
        return pd.DataFrame(list(self.db.total_stock_price
                                 .find({'$and': [{'stock_code': {'$in': stock_list}},
                                                  {'trade_day': trade_day}]})))

    def query_first_prices(self, stock_code_list):
        result = pd.DataFrame()
        for stock_code in stock_code_list:
            result.append(pd.DataFrame(list(self.db.total_stock_price.find({'stock_code': stock_code}).sort([('stock_code', 1)])\
                    .limit(1))))
        return result

    def get_last_updated_time_of_stock(self):
        return self.db.stock_config.find_one()['updated_time']

    def get_last_updated_time_of_trade_day(self):
        return self.db.trade_day_config.find_one()['updated_time']

    def get_last_updated_time_of_locked_share(self):
        return self.db.locked_share_config.find_one()['updated_time']
