def retorna_dados_transaction_saque(cpf, value):
    return{
    "email": "email@teste.com",
    "action": "withdraw",
    "cpf": cpf,
    "reference_id": "02",
    "enterprise_token": "sua-chave-api",
    "meta": {
                "id": 7178442,
                "value": value,
                "external_id": "AC9066XNOD",
                "status": "APPROVED",
                "status_detail": "Saque aprovado automaticamente.",
                "receipt_img_url": None,
                "type": "PIX",
                "user_id": 487186,
                "pix_key_id": 792976,
                "processor_name": "anspacepay",
                "bank_account_id": None,
                "created_at": "2025-06-06T20:19:31.000000Z",
                "updated_at": "2025-06-06T20:19:36.000000Z",
                "updated_by": None,
                "currency": None,
                "payment_method": "pix",
                "total_approved": 2,
                "total_denied": 0,
                "status_message": "Saque aprovado.",
                "user": {
                    "id": 487186,
                    "name": "ITALO RAMON MATOS SILVEIRA",
                    "document": {
                        "id": 486674,
                        "number": "05888483362",
                        "user_id": 487186
                    }
                }}}
