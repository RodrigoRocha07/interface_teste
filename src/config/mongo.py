# src/config/mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from src.config.settings import settings


class MongoEnterpriseClient:
    def __init__(self, enterprise_id: str):
        self.enterprise_id = enterprise_id

        # Monta a URI com segurança
        username = quote_plus(settings.MONGO_USERNAME)
        password = quote_plus(settings.MONGO_PASSWORD)

        mongo_uri = (
            f"mongodb+srv://{username}:{password}@{settings.MONGO_CLUSTER}/"
            f"?retryWrites=true&w=majority&appName={settings.MONGO_APPNAME}"
        )

        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client["fraud_detection"]

    def get_collection(self, name: str):
        """Retorna a collection com prefixo da empresa"""
        return self.db[f"{self.enterprise_id}_{name}"]

    @property
    def alerts(self):
        return self.get_collection("alerts")

    @property
    def shared_ips(self):
        return self.get_collection("shared_ips")

 
    @property
    def start_game(self):
        return self.get_collection("start_game")
 
    @property
    def game_cash_transaction(self):
        return self.get_collection("game_cash_transaction")

 
    @property
    def account_cash_transaction(self):
        return self.get_collection("account_cash_transaction")


    @property
    def wallet(self):
        return self.get_collection("wallet")

 