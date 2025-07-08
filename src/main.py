from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import json
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from src.utils.dados_login import retornar_dados_login
from src.utils.dados_wallet import retornar_dados_wallet

from src.utils.deposit import retorna_dados_transaction_deposit
from src.utils.saque import retorna_dados_transaction_saque

from src.utils.start_game import retorna_start_game
from src.utils.dados_transaction_game import retorna_dados_transaction_game

from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Dict
from src.repositorys.alerts import WalletMongo
import random

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
# URL fixa
URL_FIXA = "http://127.0.0.1:8001/fraud/betshield/external_analyse/"

# Função para gerar dados específicos para cada ação
def gerar_dados_acao(action, numero_requisicao, data):
    """Gera dados específicos para cada tipo de ação"""
    
    dados_base = {
        "timestamp": asyncio.get_event_loop().time(),
        "request_id": f"{action}_{numero_requisicao}",
        "user_agent": "API-Tester/1.0"
    }
    
    if action == "login":
        return retornar_dados_login(data.get('cpf'), data.get('ip_variavel'))
    
    elif action == "wallet":
        return retornar_dados_wallet(data.get("cpf"), data.get("credit"))

    
    elif action == "deposito":
        response =  retorna_dados_transaction_deposit(data.get("cpf"), data.get("deposit"))
        if data.get('valor_aleatorio'):
            response['meta']['amount'] = random.randint(1000, 99999)

        return response
    

    elif action == "saque":
        response = retorna_dados_transaction_saque(data.get("cpf"), data.get("saque"))
        if data.get('valor_aleatorio'):
            response['meta']['value'] = random.randint(1000, 99999)

        return response
    
    elif action == "startgame":
        response = retorna_start_game(data.get("cpf"), data.get("game_id"))
        return response
    
    elif action == "game_transaction":
        print(data)
        response = retorna_dados_transaction_game(
            cpf = data.get("cpf"),           # ← argumento nomeado
            game_id = data.get("game_id"),   # ← argumento nomeado
            value = data.get("transaction_value"),   # ← argumento posicional (ERRO!)
            type = data.get("transaction_type")     # ← argumento posicional (ERRO!)
        )
        if data['valor_aleatorio_game_transaction']:
            response['meta']['amount'] = random.randint(100, 9999)
        if data['jogo_aleatorio_game_transaction']:
            response['meta']['casino_transaction']['game_id'] = random.randint(1, 999)
        return response
    
    else:
        return dados_base

async def enviar_requisicao(client, url, action, numero, data, delay=0): 
    try:
        if delay > 0:
            await asyncio.sleep(delay / 1000)  # Converte ms para segundos
        
        # Gera os dados para esta ação
        dados = gerar_dados_acao(action, numero,data = data)
        # Log do body que será enviado
        print(f"\n🔍 REQUISIÇÃO {numero} - ACTION: {action}")
        print(f"📤 URL: {url}")
        print(f"📋 BODY: {json.dumps(dados, indent=2, ensure_ascii=False)}")
        print("-" * 50)
        
        # Envia requisição POST com os dados
        r = await client.post(url, json=dados)
        
        return {
            "numero": numero,
            "status": r.status_code,
            "action": action,
            "dados_enviados": dados,
            "response_text": r.text[:200] if r.text else None  # Primeiros 200 chars da resposta
        }
    except Exception as e:
        print(f"❌ ERRO na requisição {numero}: {str(e)}")
        return {
            "numero": numero,
            "error": str(e),
            "action": action
        }

from fastapi.responses import RedirectResponse
from fastapi import Query

@app.get("/", response_class=HTMLResponse)
async def form_get(
    request: Request,
    quantidade: int = Query(10),
    action: str = Query(None),
):
    form_data = await request.form()
    # form_data é um MultiDict, pode ser convertido para dict
    data = dict(form_data)
    alerts = await WalletMongo('550e8400-e29b-41d4-a716-446655440000').get_alerts_recentes(limite=10)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "quantidade": quantidade,
        "action_testada": action,
        "cpf": data.get('cpf'),
        "ip_variado" : data.get('ip_variado'),
        "resultados": None,
        "alerts":alerts
    })

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request):
    form_data = await request.form()
    # form_data é um MultiDict, pode ser convertido para dict
    data = dict(form_data)
    action = data.get("action")
    quantidade = int(data.get("quantidade", 10))
    delay = int(data.get("delay", 100))
    cpf = data.get("cpf")

    print(f"\n🚀 INICIANDO TESTE")
    print(f"📊 Action: {action}")
    print(f"📊 Quantidade: {quantidade}")
    print(f"📊 Delay: {delay}ms")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        tarefas = [
            enviar_requisicao(client, URL_FIXA, action, i+1, data, delay)
            for i in range(quantidade)
        ]
        resultados = await asyncio.gather(*tarefas)
    
    print(f"\n✅ TESTE CONCLUÍDO - {len(resultados)} requisições enviadas")
    print("=" * 60)
    
    # Redireciona para GET passando parâmetros para preencher o formulário (sem resultados)
    redirect_url = app.url_path_for("form_get")
    redirect_url += f"?quantidade={quantidade}&action={action}"
    if cpf:
        redirect_url += f"&cpf={cpf}"
    return RedirectResponse(url=redirect_url, status_code=303)



# Endpoint da API
@app.get("/alerts")
async def get_alerts_api():
    """Endpoint API para buscar apenas os alerts (JSON)"""
    try:
        alerts = await WalletMongo('550e8400-e29b-41d4-a716-446655440000').get_alerts_recentes(limite=10)
        return JSONResponse(content={
            "alerts": alerts, 
            "success": True
        })
    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e), 
                "success": False
            }, 
            status_code=500
        )