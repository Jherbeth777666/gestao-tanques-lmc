from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.tanque import Tanque
from backend.models.medicao import Medicao
from backend.schemas.medicao import MedicaoCreate, MedicaoResponse
from backend.services.arqueacao import calcular_volume_por_regua

router = APIRouter(prefix="/medicoes", tags=["Medições"])

@router.post("/", response_model=MedicaoResponse, status_code=status.HTTP_201_CREATED)
def registar_medicao(medicao: MedicaoCreate, db: Session = Depends(get_db)):
    tanque = db.query(Tanque).filter(Tanque.id == medicao.tanque_id).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque informado não existe.")

    volume_final = medicao.volume_medido
    if medicao.altura_cm is not None and volume_final is None:
        volume_final = calcular_volume_por_regua(tanque.capacidade_maxima, medicao.altura_cm)

    if volume_final is None:
        raise HTTPException(status_code=400, detail="Informe a altura da régua (altura_cm) ou o volume em litros (volume_medido).")

    if volume_final > (tanque.capacidade_maxima * 1.05):
        raise HTTPException(status_code=400, detail=f"Volume ({volume_final}L) excede a capacidade máxima do tanque ({tanque.capacidade_maxima}L).")

    nova_medicao = Medicao(
        tanque_id=medicao.tanque_id,
        altura_cm=medicao.altura_cm,
        volume_medido=volume_final
    )
    db.add(nova_medicao)
    db.commit()
    db.refresh(nova_medicao)
    return nova_medicao

@router.get("/", response_model=List[MedicaoResponse])
def listar_medicoes(db: Session = Depends(get_db)):
    return db.query(Medicao).order_by(Medicao.data_medicao.desc()).all()

@router.get("/tanque/{tanque_id}", response_model=List[MedicaoResponse])
def listar_medicoes_por_tanque(tanque_id: int, db: Session = Depends(get_db)):
    return db.query(Medicao).filter(Medicao.tanque_id == tanque_id).order_by(Medicao.data_medicao.desc()).all()
