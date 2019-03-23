from jqdatasdk import *
import datetime
import mongo_base as mongo
import pandas as pd
import util
import config


auth(config.get_user_name(), config.get_pwd())
db = mongo.MongoBase()

# get all stocks
today = datetime.datetime.today()
all_stocks = get_all_securities(types=['stock', 'index', 'etf'], date=today)
all_stocks['stock_code'] = all_stocks.index
db.refresh_base_stock_info(all_stocks)
# stock = pd.DataFrame(db.query_by_stock_code('600031'), index=[0])

# get all trade days
all_trade_days = get_all_trade_days()
all_trade_days = util.convert_date_to_datetime(all_trade_days)
all_trade_days = pd.DataFrame(all_trade_days, columns=['trade_day'])
db.refresh_trade_days(all_trade_days)
# print(pd.DataFrame(list(db.query_n_trade_days_before_today(n=5)), columns=['trade_day']))

db.close()
