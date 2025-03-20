from flask import jsonify
from flask_pydantic import validate, ValidationError
from src.reservas.services.reservas_service import crear_reserva, actualizar_reserva, eliminar_reserva, obtener_reserva
from src.reservas.blueprints import reserva_bp
from src.reservas.utils.validadores import ReservaSchema, ReservaUpdateSchema



@reserva_bp.route("/", methods=["POST"])
@validate()
def crear(body: ReservaSchema):
    return crear_reserva(body)

@reserva_bp.route("/<string:id>", methods=["GET"])
def obtener(id: str):
    return obtener_reserva(id)

@reserva_bp.route("/<string:id>", methods=["PUT"])
@validate()
def actualizar(id: str, body: ReservaUpdateSchema):
    return actualizar_reserva(id, body)

@reserva_bp.route("/<string:id>", methods=["DELETE"])
def eliminar(id: str):
    return eliminar_reserva(id)

@reserva_bp.errorhandler(ValidationError)
def validation_error(e):
    return jsonify({"error": e.errors()}), 400