from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.tanque import Tanque
from backend.schemas.tanque import TanqueCreate, TanqueResponse

router = APIRouter(prefix="/tanques", tags=["Tanques"])

@router.post("/", response_model=TanqueResponse, status_code=status.HTTP_201_CREATED)
def criar_tanque(tanque: TanqueCreate, db: Session = Depends(get_db)):
    tanque_existente = db.query(Tanque).filter(Tanque.numero_tanque == tanque.numero_tanque).first()
    if tanque_existente:
        raise HTTPException(status_code=400, detail="Já existe um tanque com esse número.")
    novo_tanque = Tanque(**tanque.model_dump())
    db.add(novo_tanque)
    db.commit()
    db.refresh(novo_tanque)
    return novo_tanque

@router.get("/", response_model=List[TanqueResponse])
def listar_tanques(db: Session = Depends(get_db)):
    return db.query(Tanque).all()

@router.get("/{tanque_id}", response_model=TanqueResponse)
def obter_tanque(tanque_id: int, db: Session = Depends(get_db)):
    tanque = db.query(Tanque).filter(Tanque.id == tanque_id).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque não encontrado.")
    return tanque
