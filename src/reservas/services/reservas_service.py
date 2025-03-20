from sqlalchemy import func, text
from src.reservas.database.db import db
from src.reservas.database.models import Reserva, PasajeroReserva
from src.reservas.utils.validadores import PasajeroData
from src.reservas.utils.events import publish_message
from flask import jsonify

def crear_reserva(body):
    try:
        pasajero_data = body.pasajero_data
    
        reserva = Reserva()
        db.session.add(reserva)
        db.session.commit()

        for pasajero in pasajero_data:
            
            pasajero_reserva = PasajeroReserva(pasajero_id=pasajero["id"], reserva_id=reserva.id)
            db.session.add(pasajero_reserva)
            db.session.commit()

        message = {
            'action': 'update',
            #'pasajero_id': pasajero_id,
            'nombre': pasajero_data['nombre'],
            'email': pasajero_data['email']
        }
        publish_message(queue='pasajero_updates', message=message)
        return jsonify(reserva), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
   
def obtener_reserva(reserva_id):
    reserva = db.session.query(Reserva).filter(Reserva.uuid == reserva_id).first()
    if reserva:
        return jsonify(reserva), 200
    return jsonify({"error": "Reserva no encontrada"}), 404

def actualizar_reserva(uuid: str, body: PasajeroData):
    try:
        reserva = db.session.query(Reserva).filter(Reserva.uuid == uuid).first()
        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404

        message = {
            'event': 'actualizar_pasajero',
            'id': body.uuid,
            'nombre': body.pasajero_data['nombre'],
            'email': body.pasajero_data['email']
        }
        publish_message(queue='pasajero_updates', message=message)
        reserva.pasajero_id = body.pasajero_id

        db.session.commit()
        return jsonify(reserva), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def eliminar_reserva(uuid: str):
    try:
        reserva = db.session.query(Reserva).filter(Reserva.uuid == uuid).first()
        reserva.is_active = False
        db.session.commit()
        #actualizar pasajero_reserva
        return jsonify({"message": "Reserva eliminada"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500