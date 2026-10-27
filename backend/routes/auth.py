from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.seguranca import credenciais_validas, gerar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginRequest(BaseModel):
    usuario: str
    senha: str

@router.post("/login")
def login(dados: LoginRequest):
    if credenciais_validas(dados.usuario, dados.senha):
        return {"status": "sucesso", "token": gerar_token(dados.usuario)}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Utilizador ou senha incorretos."
    )
