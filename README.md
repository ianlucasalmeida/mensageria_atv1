Projeto: Sistema de Processamento de Pedidos com Comunicação AssíncronaNome da aplicação: mensageria_atv1

🌟 Objetivo:

Simular um sistema de e-commerce onde os pedidos são processados de forma assíncrona usando filas (RabbitMQ), com atualização em tempo real no front-end por WebSocket.

📂 Componentes:

1. Front-End (HTML + WebSocket)

Interface moderna com layout responsivo.

Lista de produtos.

❌ Sem envio de pedidos.

🔔 Recebe notificações em tempo real sempre que um novo pedido é feito.

Disponível em: http://localhost:8000

2. API FastAPI (main.py)

Endpoint POST /pedido: recebe pedidos do front.

Envia os pedidos para a fila RabbitMQ (pedidos).

Serve o front-end na raiz /.

WebSocket na rota /ws para transmitir notificações.

3. Fila de Mensagens (RabbitMQ)

Gerenciado via docker-compose.yml

Armazena os pedidos de forma persistente.

Interface de gerenciamento: http://localhost:15672

Usuário: guest

Senha: guest

4. Consumidor de Mensagens (consumer/worker.py)

Conecta na fila pedidos

Processa cada mensagem recebida

Simula etapas como:

Impressão de nota fiscal

Atualização de estoque

Logs exibidos no terminal

🚀 Como executar:

Suba o RabbitMQ com Docker:

docker-compose up -d

Instale as dependências Python (em um ambiente virtual ou global):

pip install -r requirements.txt

Rode a API principal com front embutido:

python main.py

Acesse no navegador:
http://localhost:8000

Em outro terminal, inicie o consumidor:

python consumer/worker.py

A cada novo pedido recebido via API:

A fila armazena a mensagem

O consumidor processa

O front é notificado ao vivo via WebSocket

📊 Arquitetura:

[ Navegador HTML ]
      ⇓
 [ FastAPI REST + WS ]
      ⇓
  [ RabbitMQ Queue ]
      ⇓
 [ Consumer (Worker) ]

🛡️ Tolerância a falhas:

Se o consumidor estiver offline, os pedidos ficam na fila.

Ao religar o consumidor, ele processa todos os pedidos pendentes.

As mensagens são persistentes (delivery_mode=2).

Falhas de conexão WebSocket são tratadas com reconexão automática.

⚙️ Tecnologias utilizadas:

Python + FastAPI

RabbitMQ + Docker Compose

Pika (client de fila)

HTML, CSS, JavaScript (WebSocket nativo)

FontAwesome para ícones