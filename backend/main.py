from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.routes.tanques import router as tanques_router
from backend.routes.medicoes import router as medicoes_router
from backend.routes.lmc import router as lmc_router
from backend.routes.ia import router as ia_router
from backend.routes.auth import router as auth_router

app = FastAPI(title="PostoControl AI • Produção", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tanques_router)
app.include_router(medicoes_router)
app.include_router(lmc_router)
app.include_router(ia_router)

@app.get("/")
def pagina_inicial():
    return FileResponse("frontend/index.html")
