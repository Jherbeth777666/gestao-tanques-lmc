from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base

class Tanque(Base):
    __tablename__ = 'tanques'

    id = Column(Integer, primary_key=True, index=True)
    numero_tanque = Column(Integer, unique=True, nullable=False)
    tipo_combustivel = Column(String(50), nullable=False)
    capacidade_maxima = Column(Float, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    medicoes = relationship('Medicao', back_populates='tanque', cascade='all, delete-orphan')
