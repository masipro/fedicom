# main.py
from fastapi import FastAPI
from db import models, database
from fedicom import auth, pedidos, devoluciones, albaranes, facturas, stock

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Servidor Fedicom3", version="3.4.15")

app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(devoluciones.router)
app.include_router(albaranes.router)
app.include_router(facturas.router)
app.include_router(stock.router)

@app.get("/")
async def root():
    return {"message": "Servidor Fedicom3 activo"}