from datetime import date, datetime
from sqlalchemy import Column, Integer, Float, Date, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class LMCFechamento(Base):
    __tablename__ = "lmc_fechamentos"

    id = Column(Integer, primary_key=True, index=True)
    tanque_id = Column(Integer, ForeignKey("tanques.id"), nullable=False)
    data_movimento = Column(Date, nullable=False, default=date.today)
    
    estoque_inicial = Column(Float, nullable=False)
    recebimentos = Column(Float, default=0.0)      # Litros de NF-e recebidas
    vendas = Column(Float, nullable=False)          # Litros vendidos (encerrantes)
    
    estoque_escritural = Column(Float, nullable=False)
    estoque_fisico = Column(Float, nullable=False)  # Medido pela regua
    
    perda_sobra = Column(Float, nullable=False)     # Fisico - Escritural
    percentual_variacao = Column(Float, nullable=False)
    status_anp = Column(String(50), nullable=False) # CONFORME, PERDA_EXCESSIVA, SOBRA_EXCESSIVA
    
    data_registro = Column(DateTime, default=datetime.utcnow)

    tanque = relationship("Tanque")
