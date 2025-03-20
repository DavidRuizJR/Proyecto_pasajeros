# src/rabbitmq_config.py
import pika
import os
import json

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

def setup_rabbitmq():
    channel.queue_declare(queue='pasajero_updates',durable=True)

def publish_message(queue, message):
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=2))

def consume_messages(queue, callback):
    channel.basic_consume(queue=queue, on_message_callback=callback)

def start_consuming():
    channel.start_consuming()

def close_connection():
    connection.close()