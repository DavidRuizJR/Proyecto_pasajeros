# src/rabbitmq_config.py
import pika
import os
import json
import requests

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()


import pika
import json

def enviar_validacion_pasajeros(pasajeros):
    channel.queue_declare(queue='validate_passengers', durable=True)

    mensaje = json.dumps({
        "event": "validate_passengers",
        "pasajeros": pasajeros
    })

    channel.basic_publish(exchange='', routing_key='validate_passengers', body=mensaje, properties=pika.BasicProperties(delivery_mode=2))
    close_connection()

    print("📤 Enviando pasajeros a validar...")



def callback(ch, method, properties, body):
    try:
        mensaje = json.loads(body)
        if mensaje.get("event") == "pasajeros_validos":
            validos = mensaje.get("valid_passengers", [])
            invalidos = mensaje.get("invalid_passengers", [])

            print(f"✅ Pasajeros válidos: {validos}")
            print(f"❌ Pasajeros inválidos: {invalidos}")

            if validos:
                procesar_reserva_con_pasajeros(validos)

    except json.JSONDecodeError:
        print("⚠️ Error: JSON inválido")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    

    print(" [*] Esperando validaciones de pasajeros...")
    channel.start_consuming()


def setup_rabbitmq():
    channel.queue_declare(queue='pasajeros_validos', durable=True)
    channel.basic_consume(queue='pasajeros_validos', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def close_connection():
    connection.close()

