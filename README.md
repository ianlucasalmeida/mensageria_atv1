#  mensageria_atv1
### Sistema de Processamento de Pedidos com Comunicação Assíncrona

---

##  Objetivo

Simular um sistema de e-commerce distribuído onde **pedidos são processados de forma assíncrona** usando **RabbitMQ** como fila de mensagens e **WebSocket** para notificações em tempo real no front-end.

---

##  Componentes da Aplicação

###  Front-End (HTML + WebSocket)
- Interface moderna, responsiva e baseada em HTML, CSS e JS.
- **Lista de produtos** exibida para simulação.
-  **Não realiza envio de pedidos**.
-  **Recebe notificações em tempo real** via WebSocket sempre que um novo pedido é feito.
-  Disponível em: [http://localhost:8000](http://localhost:8000)

---

###  API - FastAPI (`main.py`)
- Endpoint **POST `/pedido`**: Recebe pedidos via HTTP.
- Publica os pedidos na fila **RabbitMQ (`pedidos`)**.
- Serve o front-end na raiz `/`.
- WebSocket em `/ws`: Transmite notificações em tempo real para o front-end.

---

###  Fila de Mensagens - RabbitMQ
- Orquestrado com **Docker Compose**.
- Armazena pedidos de forma **persistente** (modo de entrega 2).
- Interface de gerenciamento:
  - [http://localhost:15672](http://localhost:15672)
  - Usuário: `guest` | Senha: `guest`

---

###  Consumidor de Mensagens (`consumer/worker.py`)
- Conecta à fila `pedidos`.
- Processa mensagens recebidas simulando etapas:
  - Geração de nota fiscal
  - Atualização de estoque
- Emite logs no terminal durante o processamento.

---

##  Arquitetura Geral

[ Navegador HTML ]
⇓ WebSocket
[ FastAPI REST + WS ]
⇓ RabbitMQ (Fila de pedidos)
[ Consumer (Worker) ]


---

##  Fluxo de Funcionamento

1. Cliente acessa o site e observa os produtos.
2. Um pedido é feito via API (simulação).
3. Pedido é enfileirado no RabbitMQ.
4. Consumidor processa o pedido assincronamente.
5. Front-end é notificado em tempo real por WebSocket.

---

##  Tolerância a Falhas

- **Pedidos não são perdidos** caso o consumidor esteja offline.
- **Mensagens persistentes**: `delivery_mode=2`.
- O **consumidor pode ser reiniciado** sem perder dados.
- WebSocket com **reconexão automática** para garantir notificações.

---

##  Tecnologias Utilizadas

| Tecnologia       | Função                                   |
|------------------|-------------------------------------------|
| Python 3         | Linguagem principal                       |
| FastAPI          | API REST e WebSocket                      |
| RabbitMQ         | Fila de mensagens                         |
| Docker Compose   | Orquestração do RabbitMQ                  |
| Pika             | Cliente Python para RabbitMQ              |
| HTML, CSS, JS    | Interface do usuário                      |
| WebSocket nativo | Notificações em tempo real                |
| FontAwesome      | Ícones visuais                            |

---

##  Como Executar

### 1. Suba o RabbitMQ com Docker

```bash
docker-compose up -d

2. Instale dependências Python
bash
Copiar
Editar
pip install -r requirements.txt
3. Rode a API principal (com o front embutido)
bash
Copiar
Editar
python main.py
Acesse no navegador: http://localhost:8000

4. Em outro terminal, inicie o consumidor
bash
Copiar
Editar
python consumer/worker.py
Resultado Esperado
A cada novo pedido:

A fila armazena a mensagem.

O consumidor processa.

O navegador recebe a notificação via WebSocket em tempo real.