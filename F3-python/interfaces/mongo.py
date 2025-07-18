from pymongo import MongoClient
from config import Config

class Mongo:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]

mongo = Mongo()
