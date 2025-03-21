from flask import request, jsonify
from flask_pydantic import validate
from pydantic import ValidationError
from database import db
from database.models import Pasajeros
# from pasajeros.services.pasajeros_service import cargar_pasajeros_masivo
from utils.validadores import PasajeroSchema
from blueprints import pasajeros_bp
from services.pasajeros_service import validar_actualizar_pasajero



@pasajeros_bp.route('/', methods=['POST'])
@validate()
def crear(body: PasajeroSchema):
    try:
        nuevo_pasajero = Pasajeros(nombre=body.nombre, email=body.email)
        db.session.add(nuevo_pasajero)
        db.session.commit()
        return jsonify({"message": "Pasajero creado", "id": nuevo_pasajero.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pasajeros_bp.route('/validar_pasajeros', methods=['POST'])
@validate()
def validar_pasajeros():
    try:
        data = request.get_json()
        pasajeros_data = data.get("pasajeros",[])
        pasajeros_validos, pasajeros_invalidos = validar_actualizar_pasajero(pasajeros_data)
    
        return jsonify({
            "valid_passengers": pasajeros_validos,
            "invalid_passengers": pasajeros_invalidos
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @pasajeros_bp.route('/load_massive', methods=['POST'])
# def load_massive():
#     data = request.get_json()
#     try:
#         cargar_pasajeros_masivo(data)
#         return jsonify({"message": "Carga masiva completada"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@pasajeros_bp.errorhandler(ValidationError)
def validation_error(e):
    return jsonify({"error": e.errors()}), 400
