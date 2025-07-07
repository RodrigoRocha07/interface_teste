import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()  # Carrega o .env

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chave-padrao-segura")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))


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




