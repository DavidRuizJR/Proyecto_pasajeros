from flask import request, jsonify
from flask_pydantic import validate
from pydantic import ValidationError
from src.pasajeros.database import db
from src.pasajeros.database.models import Pasajeros
from src.pasajeros.services.pasajeros_service import cargar_pasajeros_masivo
from src.pasajeros.utils.validadores import PasajeroSchema
from src.reservas.blueprints import pasajeros_bp



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


@pasajeros_bp.route('/<int:id>', methods=['PUT'])
@validate()
def actualizar(id: int, body: PasajeroSchema):
    pasajero = Pasajeros.query.get(id)
    if not pasajero:
        return jsonify({"error": "Pasajero no encontrado"}), 404
    try:
        pasajero.nombre = body.nombre
        pasajero.email = body.email
        db.session.commit()
        return jsonify({"message": "Pasajero actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pasajeros_bp.route('/load_massive', methods=['POST'])
def load_massive():
    data = request.get_json()
    try:
        cargar_pasajeros_masivo(data)
        return jsonify({"message": "Carga masiva completada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pasajeros_bp.errorhandler(ValidationError)
def validation_error(e):
    return jsonify({"error": e.errors()}), 400
