# src/rabbitmq_config.py
import pika
import os
import json
import requests
import threading
from src.pasajeros.database.models import Pasajeros
from src.pasajeros.database.db import db


rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host,5672))
channel = connection.channel()


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        if message.get("event") == "pasajeros_validados":
            pasajeros_data = message.get("pasajeros", [])

            # Llamar a la API de validación del microservicio
            response = requests.post("http://localhost:5001/validar_pasajeros", json={"pasajeros": pasajeros_data})
            response_data = response.json()

            # Publicar resultado en RabbitMQ
            channel.queue_declare(queue='p', durable=True)
            channel.basic_publish(exchange='', routing_key='pasajeros_validados', body=json.dumps({
                "event": "pasajeros_validados",
                "pasajeros_validos": response_data.get("validos", []),
                "pasajeros_invalidos": response_data.get("invalidos", [])
            }),properties=pika.BasicProperties(delivery_mode=2))

            close_connection()

            print(f"✅ Pasajeros válidos: {response_data.get('pasajeros_validados')} | ❌ Pasajeros inválidos: {response_data.get('invalid_passengers')}")
    except json.JSONDecodeError:
        print("⚠️ Error: JSON inválido")
    except requests.RequestException as e:
        print(f"⚠️ Error llamando a la API de validación: {e}")


def setup_rabbitmq():
    channel.queue_declare(queue='validar_pasajeros', durable=True)
    channel.basic_consume(queue='validar_pasajeros', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    
def close_connection():
    connection.close()