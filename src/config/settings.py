import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()  # Carrega o .env



class Settings(BaseSettings):
    JANELA_TEMPO_MULTILOGIN: int = 300
    QUANTIDADE_LOGINS_MULTILOGIN: int = 5
    QUANTIDADE_LOGINS_MESMO_IP: int = 2

    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_CLUSTER: str
    MONGO_APPNAME: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()




