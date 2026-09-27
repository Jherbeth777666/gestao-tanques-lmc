from datetime import datetime
from pydantic import BaseModel

class TanqueBase(BaseModel):
    numero_tanque: int
    tipo_combustivel: str
    capacidade_maxima: float

class TanqueCreate(TanqueBase):
    pass

class TanqueResponse(TanqueBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
