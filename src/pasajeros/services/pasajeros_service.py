from src.pasajeros.database.db import db
from src.pasajeros.database.models import Pasajeros
import json
import threading
# import psycopg2
from src.pasajeros.utils.events import consume_messages, start_consuming
from flask import jsonify
from src.pasajeros.utils.validadores import PasajeroSchema,PasajerosListSchema
from pydantic import ValidationError


# def cargar_pasajeros_masivo(data):
#     conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
#     cur = conn.cursor()
#     psycopg2.extras.execute_batch(cur, "INSERT INTO pasajero (nombre, email) VALUES (%s, %s)", data)
#     conn.commit()
#     cur.close()
#     conn.close()

def validar_actualizar_pasajero(pasajeros):
    pasajeros_validos = []
    pasajeros_invalidos = []
    for pasajero in pasajeros:
        try:
            pasajero_obj = PasajeroSchema(**pasajero)
            pasajero_db = Pasajeros.query.filter_by(uuid=pasajero_obj.uuid).first()
            if pasajero_db:
                cambios = False
                if pasajero_db.nombre != pasajero_obj.nombre:
                    pasajero_db.nombre = pasajero_obj.nombre
                    cambios = True
                if pasajero_db.email != pasajero_obj.email:
                    pasajero_db.email = pasajero_obj.email
                    cambios = True
                if cambios:
                    db.session.commit()
                
                pasajeros_validos.append(pasajero_obj.uuid)
            else:
                pasajeros_invalidos.append(pasajero_obj.uuid)
                return jsonify({"error": "Pasajero no encontrado"}), 404
            
        except ValidationError as e:
            pasajeros_invalidos.append(pasajero.get("id", "desconocido"))

    return pasajeros_validos, pasajeros_invalidos


def callback(ch, method, properties, body):
    message = json.loads(body)
    pasajero = Pasajeros.query.get(message['pasajero_id'])
    if pasajero:
        pasajero.nombre = message['nombre']
        pasajero.email = message['email']
        db.session.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)

def iniciar_consumidor():
    consume_messages(queue='pasajero_updates', callback=callback)
    start_consuming()

def iniciar_consumidor_en_hilo():
    thread = threading.Thread(target=iniciar_consumidor)
    thread.daemon = True
    thread.start()