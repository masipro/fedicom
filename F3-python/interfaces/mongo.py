from pymongo import MongoClient
from config import Config

class Mongo:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]

    async def consulta_tx_por_crc(self, crc):
        # Dummy implementation
        if crc == 'dummy-crc':
            return {'_id': 'dummy-id', 'clientResponse': {'body': {'numeroPedido': 'dummy-sap-order-number'}}}
        else:
            return None

mongo = Mongo()
