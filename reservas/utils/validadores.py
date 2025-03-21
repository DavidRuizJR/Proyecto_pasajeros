from datetime import date, time
from typing import Optional
from pydantic import Field, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class PasajeroData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    uuid: str = Field(...)
    nombre: str = Field(..., min_length=3)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class ReservaSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    pasajero_data: Optional[PasajeroData] = Field(None)
    fecha: date = Field(...)
    hora: time = Field(...)
    is_active: Optional[int] = Field(...)

class ReservaUpdateSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    pasajero_data: Optional[PasajeroData] = Field(None)
    is_active: Optional[int] = Field(...)
