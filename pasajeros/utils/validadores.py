from typing import List
from pydantic import Field, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class PasajeroSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    uuid: str = Field(...)
    nombre: str = Field(...,min_length=3)
    email: str = Field(...,pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class PasajerosListSchema(BaseModel):
    pasajeros: List[PasajeroSchema]

class PasajerosRequest(BaseModel):
    pasajeros: List[int]