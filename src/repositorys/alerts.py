from src.config.settings import settings
from src.config.mongo import MongoEnterpriseClient
import uuid
from typing import List, Dict, Optional
from datetime import datetime

class WalletMongo:
    def __init__(self, enterprise_id: str):
        self.mongo = MongoEnterpriseClient(enterprise_id)
        self.collection = self.mongo.alerts  # Corrigido: "alerts" em vez de "alets"

    async def get_alerts(self, customer_id: str, limite: int = 10):
        """Busca todos os alerts de um customer_id específico"""
        try:
            safe_customer_id = str(customer_id)

            # find() retorna múltiplos documentos, find_one() retorna apenas um
            cursor = self.collection.find(
                {"customer_id": safe_customer_id},
                projection={"_id": False}  # Remove o _id do retorno
            ).sort("created_at", -1).limit(limite)  # Ordena por data (mais recente primeiro)

            alerts = []
            async for alert in cursor:
                alerts.append(alert)
            
            return alerts
        
        except Exception as e:
            print(f"Erro ao buscar alerts: {e}")
            return []

    async def get_all_alerts(self, limite: int = 50) :
        """Busca TODOS os alerts (sem filtro de customer_id)"""
        try:
            cursor = self.collection.find(
                {},  # Filtro vazio = todos os documentos
                projection={"_id": False}
            ).sort("created_at", -1).limit(limite)

            alerts = []
            async for alert in cursor:
                alerts.append(alert)
            
            return alerts
        
        except Exception as e:
            print(f"Erro ao buscar todos os alerts: {e}")
            return []

    async def get_alerts_recentes(self, limite: int = 10) :
        """Busca os alerts mais recentes (formatados para o frontend)"""
        try:
            cursor = self.collection.find(
                {},
                projection={"_id": False}
            ).sort("created_at", -1).limit(limite)

            alerts = []
            async for document in cursor:
                # Formata para o padrão esperado pelo frontend
                customer = document['customer']
                alert = {
                    "alert": document.get("alert_type", "Alert"),
                    "date": self._format_date(document.get("created_at")),
                    "customer_id": customer.get("id", ""),
                    "customer_name": customer.get("name", "")
                }
                print(alert)
                alerts.append(alert)
            
            return alerts
        
        except Exception as e:
            print(f"Erro ao buscar alerts recentes: {e}")
            return []

    def _format_date(self, date_obj) -> str:
        """Formata data para string"""
        if date_obj:
            if isinstance(date_obj, datetime):
                return date_obj.strftime("%d/%m/%Y - %H:%M")
            else:
                return str(date_obj)
        return datetime.now().strftime("%d/%m/%Y - %H:%M")

