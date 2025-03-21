import uuid
from database.db import db
from sqlalchemy import DateTime, func
import sqlalchemy as sa

class Pasajeros(db.Model):
    __tablename__ = 'PASAJERO'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(sa.UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    update_date = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_date = db.Column(DateTime, nullable=False, server_default=func.now())
    