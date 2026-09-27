from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Medicao(Base):
    __tablename__ = "medicoes"

    id = Column(Integer, primary_key=True, index=True)
    tanque_id = Column(Integer, ForeignKey("tanques.id"), nullable=False)
    altura_cm = Column(Float, nullable=True)
    volume_medido = Column(Float, nullable=False)
    data_medicao = Column(DateTime, default=datetime.utcnow)

    tanque = relationship("Tanque", back_populates="medicoes")
