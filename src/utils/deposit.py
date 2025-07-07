def retorna_dados_transaction_deposit(cpf, value):
    return {
    "email": "email@teste.com",
    "action": "deposit",
    "cpf": cpf,
    "reference_id": "02",
    "enterprise_token": "sua-chave-api",
    "meta": {
                "amount": value,
                "status": "approved",
                "created_at": "2025-06-11T19:24:04.000000Z"
            }
    }
