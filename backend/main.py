import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.routes.tanques import router as tanques_router
from backend.routes.medicoes import router as medicoes_router
from backend.routes.lmc import router as lmc_router
from backend.routes.ia import router as ia_router
from backend.routes.auth import router as auth_router
from backend.seguranca import exigir_token

app = FastAPI(title="PostoControl AI • Produção", version="2.1.0")

# O frontend é servido pela própria API; outras origens só se listadas em ALLOWED_ORIGINS.
origens = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if origens:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origens,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

protegido = [Depends(exigir_token)]

app.include_router(auth_router)
app.include_router(tanques_router, dependencies=protegido)
app.include_router(medicoes_router, dependencies=protegido)
app.include_router(lmc_router, dependencies=protegido)
app.include_router(ia_router, dependencies=protegido)

@app.get("/")
def pagina_inicial():
    return FileResponse("frontend/index.html")
