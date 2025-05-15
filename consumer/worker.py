import pika
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def processar_pedido(ch, method, properties, body):
    pedido = json.loads(body)
    logging.info(f"📦 Processando pedido de {pedido['cliente']}")
    logging.info("🧾 Gerando nota fiscal...")
    time.sleep(2)
    logging.info("📦 Atualizando estoque...")
    time.sleep(1)
    logging.info("✅ Pedido finalizado!\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="pedidos", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="pedidos", on_message_callback=processar_pedido)
    logging.info("🛠️ Aguardando pedidos para processar...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
