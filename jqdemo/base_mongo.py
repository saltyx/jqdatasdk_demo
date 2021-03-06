import pymongo as mongo
from config.config import *


class BaseMongo:

    def __init__(self):
        self.db_client = mongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client.jqdata

    def close(self):
        self.db_client.close()

    def __del__(self):
        log.debug("close connection")
        self.close()
