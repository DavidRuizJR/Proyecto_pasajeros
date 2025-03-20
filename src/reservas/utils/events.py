# src/rabbitmq_config.py
import pika
import os
import json
import requests

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



def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        if message.get("event") == "validate_passengers":
            pasajeros_data = message.get("pasajeros", [])

            # Llamar a la API de validación del microservicio
            response = requests.post("http://localhost:5001/validar_pasajeros", json={"pasajeros": pasajeros_data})
            response_data = response.json()

            # Publicar resultado en RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='validated_passengers', durable=True)
            channel.basic_publish(exchange='', routing_key='validated_passengers', body=json.dumps({
                "event": "validated_passengers",
                "valid_passengers": response_data.get("valid_passengers", []),
                "invalid_passengers": response_data.get("invalid_passengers", [])
            }))
            connection.close()

            print(f"✅ Pasajeros válidos: {response_data.get('valid_passengers')} | ❌ Pasajeros inválidos: {response_data.get('invalid_passengers')}")

    except json.JSONDecodeError:
        print("⚠️ Error: JSON inválido")
    except requests.RequestException as e:
        print(f"⚠️ Error llamando a la API de validación: {e}")

# Iniciar el consumidor
def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='validate_passengers', durable=True)
    channel.basic_consume(queue='validate_passengers', on_message_callback=callback, auto_ack=True)

    print(" [*] Esperando mensajes de validación de pasajeros...")
    channel.start_consuming()