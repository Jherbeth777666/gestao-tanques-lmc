from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class LMCFechamentoCreate(BaseModel):
    tanque_id: int
    data_movimento: Optional[date] = None
    estoque_inicial: Optional[float] = None
    recebimentos: float = 0.0
    vendas: float
    estoque_fisico: Optional[float] = None
    altura_cm: Optional[float] = None

class LMCFechamentoResponse(BaseModel):
    id: int
    tanque_id: int
    data_movimento: date
    estoque_inicial: float
    recebimentos: float
    vendas: float
    estoque_escritural: float
    estoque_fisico: float
    perda_sobra: float
    percentual_variacao: float
    status_anp: str
    data_registro: datetime

    class Config:
        from_attributes = True
