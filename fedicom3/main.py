from fastapi import FastAPI
from fedicom import pedidos, devoluciones, stock, auth, albaranes, facturas
from db.database import init_db

app = FastAPI(title="Servidor Fedicom3", version="3.4.15")

# app.include_router(auth.router, tags=["auth"])
# app.include_router(pedidos.router, tags=["pedidos"])
# app.include_router(devoluciones.router, tags=["devoluciones"])
# app.include_router(albaranes.router, tags=["albaranes"])
# app.include_router(facturas.router, tags=["facturas"])
# app.include_router(stock.router, tags=["stock"])

app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(devoluciones.router)
app.include_router(albaranes.router)
app.include_router(facturas.router)
app.include_router(stock.router)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Servidor Fedicom3 activo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=50505, reload=True)