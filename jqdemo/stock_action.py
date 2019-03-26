import pandas as pd
import datetime
from jqdemo.base_mongo import BaseMongo
from jqdemo.base_jqdatasdk import BaseJQData
from jqdemo.offline_stock_action import OfflineStockAction
import config.config


class StockAction(OfflineStockAction, BaseJQData):

    def __init__(self):
        OfflineStockAction.__init__(self)
        BaseJQData.__init__(self)

    def refresh_base_stock_info(self):
        self.db.base_stock.delete_many({})
        self.db.base_stock.insert_many(self.get_all_stocks().to_dict('record'))
        self.db.stock_config.delete_many({})
        self.db.stock_config.insert_one({"updated_time": config.get_today()})

    def refresh_trade_days(self):
        self.db.trade_days.delete_many({})
        self.db.trade_days.insert_many(self.get_all_trade_days().to_dict('record'))
        self.db.trade_day_config.delete_many({})
        self.db.trade_day_config.insert_one({"updated_time": config.get_today()})

    def refresh_locked_share(self):
        stocks = pd.DataFrame(list(self.db.base_stock.find({"type": "stock"})))
        locked_share = self.get_locked_share(list(stocks["stock_code"]),
                                             start_day=config.get_today())
        self.db.locked_share.delete_many({})
        self.db.locked_share.insert_many(locked_share.to_dict('record'))
        self.db.locked_share_config.delete_many({})
        self.db.locked_share_config.insert_one({"updated_time": config.get_today()})

    def refresh_all_stock_price(self):
        stock_codes = list(self.get_all_stocks()['stock_code'])
        start_day = self.db.price_config.find_one()
        if start_day is None:
            self.db.price.delete_many({})
            start_day = datetime.datetime(2019, 1, 1)
        else:
            start_day = start_day['updated_time']
        print('last updated time: ', start_day)
        for i in range(len(stock_codes)):
            config.config.view_bar(i + 1, len(stock_codes))
            prices = self.get_price(stock_codes[i], start_day=start_day, end_day=datetime.datetime.today())
            prices['stock_code'] = stock_codes[i]
            prices['time'] = prices.index
            self.db.price.insert_many(prices.to_dict('record'))

        self.db.price_config.delete_many({})
        self.db.price_config.insert_one({"updated_time": config.get_today()})

    # 由于数据量巨大，需要单个获取，每次更新
    def refresh_total_price(self, stock_code, start_day):
        all_price = self.get_price(stock_code, start_day=start_day,
                                   end_day=datetime.datetime.utcnow())
        self.db.all_price.insert_many(all_price.to_dict('record'))
        return all_price

    def refresh_total_stock_price(self, stocks):
        self.db.total_stock_price.delete_many({})
        for i in range(len(stocks)):
            all_price = self.get_price(stocks[i]['stock_code'], start_day=stocks[i]['start_date'],
                                       end_day=datetime.datetime.utcnow())
            all_price['stock_code'] = stocks[i]['stock_code']
            all_price['trade_day'] = all_price.index
            all_price['created_time'] = datetime.datetime.utcnow()
            all_price['updated_time'] = datetime.datetime.utcnow()
            self.db.total_stock_price.insert_many(all_price.to_dict('record'))
            config.view_bar(i+1, len(stocks))

    def append_stock_price(self, stock_code):
        newest_record = self.db.total_stock_price.find_one({"stock_code": stock_code})\
                                    .sort([("trade_day", -1)]).limit(1)
        print('last updated time : ', newest_record['updated_time'])
        prices = self.get_price(stock_code, end_day=datetime.datetime.today(),
                                start_day=newest_record['updated_time'])
        prices['stock_code'] = stock_code
        prices['trade_day'] = prices.index
        prices['updated_time'] = datetime.datetime.utcnow()
        self.db.total_stock_price.insert_many(prices.to_dict('record'))

    def __del__(self):
        BaseMongo.__del__(self)
