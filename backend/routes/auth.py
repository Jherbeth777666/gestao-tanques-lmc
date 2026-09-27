import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginRequest(BaseModel):
    usuario: str
    senha: str

@router.post("/login")
def login(dados: LoginRequest):
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "posto2026")

    if dados.usuario == admin_user and dados.senha == admin_pass:
        return {"status": "sucesso", "token": "session_posto_token_valid"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Utilizador ou senha incorretos."
    )
