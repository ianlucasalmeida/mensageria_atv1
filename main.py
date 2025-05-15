from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pika
import json
import os

app = FastAPI()

# Serve a pasta 'frontend' como arquivos estáticos
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

class Pedido(BaseModel):
    cliente: str
    itens: list[str]
    quantidade: int
    valor_total: float

def send_to_queue(message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="pedidos", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="pedidos",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

@app.post("/pedido")
def criar_pedido(pedido: Pedido):
    try:
        send_to_queue(pedido.dict())
        return {"message": "Pedido recebido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Permite rodar com `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
