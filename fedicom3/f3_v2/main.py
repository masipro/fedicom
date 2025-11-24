
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import API_VERSION
from database import Base, engine
from fedicom.auth_utils import AuthError
from fedicom.api import auth as auth_api
from fedicom.api import general as general_api
from fedicom.api import pedidos as pedidos_api
from fedicom.api import devoluciones as devoluciones_api
from fedicom.api import facturas as facturas_api
from fedicom.api import albaranes as albaranes_api

app = FastAPI(title="Fedicom 3.4.15 TEST Server", version=API_VERSION, openapi_url="/fedicom/api/v3.4.15/openapi.json", docs_url="/docs", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.exception_handler(AuthError)
async def auth_error_handler(request, exc: AuthError):
    return JSONResponse(
        status_code=exc.status_code,
        content=[{"codigo": exc.code, "descripcion": exc.description}],
        headers={"Content-Api-Version": API_VERSION},
    )


app.include_router(auth_api.router)
app.include_router(general_api.router)
app.include_router(pedidos_api.router)
app.include_router(devoluciones_api.router)
app.include_router(facturas_api.router)
app.include_router(albaranes_api.router)

@app.get("/",status_code=200,tags=["Status"])
@app.get("/status",status_code=200,tags=["Status"])
async def status():
    return {"message": "Servidor Fedicom3 activo"}