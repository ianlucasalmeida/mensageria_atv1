from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pika
import json
import os

app = FastAPI()

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexões WebSocket ativas
active_connections: list[WebSocket] = []

# Modelos
class ItemPedido(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int

class PedidoCompleto(BaseModel):
    cliente: str
    itens: list[ItemPedido]
    valorTotal: str
    data: str

# Função para enviar à fila RabbitMQ
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

# Notificar WebSockets conectados
async def notificar_todos_ws(mensagem: str):
    for ws in active_connections:
        try:
            await ws.send_text(mensagem)
        except:
            pass

# POST /pedido
@app.post("/pedido")
async def criar_pedido(pedido: PedidoCompleto):
    try:
        print(f"📥 Pedido recebido: {pedido.cliente}")
        send_to_queue(pedido.dict())
        await notificar_todos_ws(f"Novo pedido de {pedido.cliente} recebido!")
        return {"message": "Pedido recebido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket /ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Serve HTML manualmente
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("frontend/index.html")

# Serve arquivos estáticos (ex: CSS, JS separados)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Execução local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
