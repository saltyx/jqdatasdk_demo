from jqdemo import stock_action

# logging.basicConfig(level=logging.INFO,
                    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log = logging.getLogger(__name__)
# log.info("starting")
stock_action = stock_action.StockAction()

stock_action.refresh_locked_share()

# get all stocks
# today = datetime.datetime.today()
# all_stocks = get_all_securities(types=['stock', 'index', 'etf'], date=today)
# all_stocks['stock_code'] = all_stocks.index
# db.refresh_base_stock_info(all_stocks)
# stock = pd.DataFrame(db.query_by_stock_code('600031'), index=[0])

# stock_action.refresh_base_stock_info()

# get all trade days
# all_trade_days = get_all_trade_days()
# all_trade_days = util.convert_date_to_datetime(all_trade_days)
# all_trade_days = pd.DataFrame(all_trade_days, columns=['trade_day'])
# stock_action.refresh_trade_days()

# print(pd.DataFrame(list(db.query_n_trade_days_before_today(n=5)), columns=['trade_day']))

# db.close()
