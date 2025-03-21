from reservas.database.db import db
import uuid
from sqlalchemy import DateTime, func
import sqlalchemy as sa

class Reserva(db.Model):
    __tablename__ = 'RESERVA'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(sa.UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    update_date = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_date = db.Column(DateTime, nullable=False, server_default=func.now())

class PasajeroReserva(db.Model):
    __tablename__ = 'PASAJERO_RESERVA'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(sa.UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    pasajero_id = db.Column(sa.UUID(as_uuid=True), unique=True, nullable=False)
    reserva_id = db.Column(db.Integer, db.ForeignKey('RESERVA.id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    update_date = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_date = db.Column(DateTime, nullable=False, server_default=func.now())
