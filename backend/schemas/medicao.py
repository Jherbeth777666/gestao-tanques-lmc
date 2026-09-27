from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MedicaoBase(BaseModel):
    tanque_id: int
    altura_cm: Optional[float] = None
    volume_medido: Optional[float] = None

class MedicaoCreate(MedicaoBase):
    pass

class MedicaoResponse(MedicaoBase):
    id: int
    data_medicao: datetime

    class Config:
        from_attributes = True
