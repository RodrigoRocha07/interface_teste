from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import json
from pathlib import Path
from fastapi.staticfiles import StaticFiles
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
# URL fixa
URL_FIXA = "http://127.0.0.1:8001/fraud"

# Função para gerar dados específicos para cada ação
def gerar_dados_acao(action, numero_requisicao, cpf):
    """Gera dados específicos para cada tipo de ação"""
    
    dados_base = {
        "timestamp": asyncio.get_event_loop().time(),
        "request_id": f"{action}_{numero_requisicao}",
        "user_agent": "API-Tester/1.0"
    }
    
    if action == "login":
        return {
            **dados_base,
            "action": "login",
            "cpf": f"{cpf}",
            "password": "senha123",
            "ip_address": "127.0.0.1"
        }
    
    elif action == "wallet":
        return {
            **dados_base,
            "action": "wallet",
            "user_id": f"user_{numero_requisicao}",
            "wallet_type": "main"
        }
    
    elif action == "deposito":
        return {
            **dados_base,
            "action": "deposit",
            "user_id": f"user_{numero_requisicao}",
            "amount": 100.0,
            "currency": "BRL",
            "payment_method": "credit_card"
        }
    
    elif action == "saque":
        return {
            **dados_base,
            "action": "withdrawal",
            "user_id": f"user_{numero_requisicao}",
            "amount": 50.0,
            "currency": "BRL",
            "bank_account": "12345-6"
        }
    
    elif action == "startgame":
        return {
            **dados_base,
            "action": "start_game",
            "user_id": f"user_{numero_requisicao}",
            "game_id": "poker_texas",
            "bet_amount": 10.0
        }
    
    elif action == "game_transaction":
        return {
            **dados_base,
            "action": "game_transaction",
            "user_id": f"user_{numero_requisicao}",
            "game_id": "poker_texas",
            "transaction_type": "bet",
            "amount": 25.0
        }
    
    else:
        return dados_base

async def enviar_requisicao(client, url, action, numero, delay=0, cpf=None):
    try:
        if delay > 0:
            await asyncio.sleep(delay / 1000)  # Converte ms para segundos
        
        # Gera os dados para esta ação
        dados = gerar_dados_acao(action, numero, cpf = cpf)
        
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
    cpf: str = Query(None),
):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "quantidade": quantidade,
        "action_testada": action,
        "cpf": cpf,
        "resultados": None,
    })

@app.post("/", response_class=HTMLResponse)
async def form_post(
    request: Request,
    action: str = Form(...),
    quantidade: int = Form(...),
    delay: int = Form(default=100),
    cpf: str = Form(default=None),
):
    print(f"\n🚀 INICIANDO TESTE")
    print(f"📊 Action: {action}")
    print(f"📊 Quantidade: {quantidade}")
    print(f"📊 Delay: {delay}ms")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        tarefas = [
            enviar_requisicao(client, URL_FIXA, action, i+1, delay, cpf=cpf) 
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