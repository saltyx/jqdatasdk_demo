import pymongo as mongo


class MongoBase:

    def __init__(self):
        self.db_client = mongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client.jqdata

    def close(self):
        self.db_client.close()