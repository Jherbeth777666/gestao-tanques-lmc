import os
import tempfile

os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "teste.db")
os.environ["ADMIN_USER"] = "admin"
os.environ["ADMIN_PASSWORD"] = "senha-de-teste"

import pytest
from fastapi.testclient import TestClient

import backend.models  # noqa: F401  (registra as tabelas)
from backend.database import Base, engine
from backend.main import app
from backend.seguranca import gerar_token, validar_token

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def token_valido():
    res = client.post("/auth/login", json={"usuario": "admin", "senha": "senha-de-teste"})
    assert res.status_code == 200
    return res.json()["token"]


def test_login_com_senha_errada_e_recusado():
    res = client.post("/auth/login", json={"usuario": "admin", "senha": "posto2026"})
    assert res.status_code == 401


def test_login_sem_senha_configurada_fica_bloqueado(monkeypatch):
    monkeypatch.delenv("ADMIN_PASSWORD")
    res = client.post("/auth/login", json={"usuario": "admin", "senha": ""})
    assert res.status_code == 503


@pytest.mark.parametrize("rota", ["/tanques/", "/medicoes/", "/lmc/fechamentos"])
def test_rotas_de_dados_exigem_token(rota):
    assert client.get(rota).status_code == 401
    assert client.get(rota, headers={"Authorization": "Bearer session_posto_token_valid"}).status_code == 401


def test_rota_aceita_token_do_login():
    res = client.get("/tanques/", headers={"Authorization": f"Bearer {token_valido()}"})
    assert res.status_code == 200


def test_token_adulterado_e_invalido():
    token = gerar_token("admin")
    dados, assinatura = token.split(".")
    assert validar_token(f"{dados}.{'0' * len(assinatura)}") is None
    assert validar_token(token) == "admin"
