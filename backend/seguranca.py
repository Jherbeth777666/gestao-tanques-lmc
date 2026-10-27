import base64
import hashlib
import hmac
import os
import secrets
import time

from fastapi import Header, HTTPException, status

VALIDADE_TOKEN_SEGUNDOS = 12 * 60 * 60

# Sem SECRET_KEY definida, gera uma chave por processo: os tokens deixam de valer ao reiniciar.
_CHAVE = (os.getenv("SECRET_KEY") or secrets.token_hex(32)).encode()


def _assinar(dados: str) -> str:
    return hmac.new(_CHAVE, dados.encode(), hashlib.sha256).hexdigest()


def gerar_token(usuario: str) -> str:
    expira = int(time.time()) + VALIDADE_TOKEN_SEGUNDOS
    dados = base64.urlsafe_b64encode(f"{usuario}|{expira}".encode()).decode()
    return f"{dados}.{_assinar(dados)}"


def validar_token(token: str) -> str | None:
    try:
        dados, assinatura = token.split(".", 1)
        if not hmac.compare_digest(assinatura, _assinar(dados)):
            return None
        usuario, expira = base64.urlsafe_b64decode(dados.encode()).decode().rsplit("|", 1)
        if int(expira) < time.time():
            return None
        return usuario
    except (ValueError, UnicodeDecodeError):
        return None


def credenciais_validas(usuario: str, senha: str) -> bool:
    senha_admin = os.getenv("ADMIN_PASSWORD")
    if not senha_admin:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Defina ADMIN_PASSWORD no ambiente para habilitar o login.",
        )
    usuario_admin = os.getenv("ADMIN_USER", "admin")
    return hmac.compare_digest(usuario, usuario_admin) & hmac.compare_digest(senha, senha_admin)


def exigir_token(authorization: str | None = Header(default=None)) -> str:
    if authorization and authorization.startswith("Bearer "):
        usuario = validar_token(authorization.removeprefix("Bearer "))
        if usuario:
            return usuario
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sessão inválida ou expirada. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
