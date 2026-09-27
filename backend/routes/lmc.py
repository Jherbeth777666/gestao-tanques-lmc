from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from backend.database import get_db
from backend.models.tanque import Tanque
from backend.models.medicao import Medicao
from backend.models.lmc import LMCFechamento
from backend.schemas.lmc import LMCFechamentoCreate, LMCFechamentoResponse
from backend.services.lmc_service import calcular_lmc
from backend.services.arqueacao import calcular_volume_por_regua

router = APIRouter(prefix="/lmc", tags=["LMC - Fechamento"])

@router.get("/ultimo-estoque/{tanque_id}")
def obter_ultimo_estoque(tanque_id: int, db: Session = Depends(get_db)):
    ultimo_lmc = db.query(LMCFechamento).filter(LMCFechamento.tanque_id == tanque_id).order_by(LMCFechamento.data_movimento.desc()).first()
    if ultimo_lmc:
        return {"estoque_inicial_sugerido": ultimo_lmc.estoque_fisico}
    
    ultima_medicao = db.query(Medicao).filter(Medicao.tanque_id == tanque_id).order_by(Medicao.data_medicao.desc()).first()
    if ultima_medicao:
        return {"estoque_inicial_sugerido": ultima_medicao.volume_medido}
        
    return {"estoque_inicial_sugerido": 0.0}

@router.post("/fechamento", response_model=LMCFechamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_fechamento_lmc(fechamento: LMCFechamentoCreate, db: Session = Depends(get_db)):
    tanque = db.query(Tanque).filter(Tanque.id == fechamento.tanque_id).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque não encontrado.")

    data_fechamento = fechamento.data_movimento or date.today()

    # Estoque inicial (se nao informado, usa o sugerido)
    estoque_ini = fechamento.estoque_inicial
    if estoque_ini is None:
        sugestao = obter_ultimo_estoque(fechamento.tanque_id, db)
        estoque_ini = sugestao["estoque_inicial_sugerido"]

    # Estoque fisico: por regua ou valor direto
    estoque_fis = fechamento.estoque_fisico
    if estoque_fis is None and fechamento.altura_cm is not None:
        estoque_fis = calcular_volume_por_regua(tanque.capacidade_maxima, fechamento.altura_cm)

    if estoque_fis is None:
        raise HTTPException(status_code=400, detail="Informe a altura da régua (altura_cm) ou o estoque físico (estoque_fisico).")

    # Calculo oficial LMC
    resultado = calcular_lmc(
        estoque_inicial=estoque_ini,
        recebimentos=fechamento.recebimentos,
        vendas=fechamento.vendas,
        estoque_fisico=estoque_fis
    )

    novo_lmc = LMCFechamento(
        tanque_id=fechamento.tanque_id,
        data_movimento=data_fechamento,
        estoque_inicial=estoque_ini,
        recebimentos=fechamento.recebimentos,
        vendas=fechamento.vendas,
        estoque_escritural=resultado["estoque_escritural"],
        estoque_fisico=estoque_fis,
        perda_sobra=resultado["perda_sobra"],
        percentual_variacao=resultado["percentual_variacao"],
        status_anp=resultado["status_anp"]
    )
    db.add(novo_lmc)
    db.commit()
    db.refresh(novo_lmc)
    return novo_lmc

@router.get("/fechamentos", response_model=List[LMCFechamentoResponse])
def listar_fechamentos(db: Session = Depends(get_db)):
    return db.query(LMCFechamento).order_by(LMCFechamento.data_movimento.desc(), LMCFechamento.id.desc()).all()
