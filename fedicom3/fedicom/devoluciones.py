# fedicom/devoluciones.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import crud, database
from fedicom.auth import requiere_jwt

router = APIRouter(prefix="/devoluciones", dependencies=[Depends(requiere_jwt)])

class LineaDevolucionIn(BaseModel):
    codigo_articulo: str
    cantidad: float

class DevolucionIn(BaseModel):
    num_farmacia: str
    user_id: str
    lineas: list[LineaDevolucionIn]

@router.post("")
def crear_devolucion(dev: DevolucionIn, db: Session = Depends(database.get_db)):
    if not dev.num_farmacia.strip():
        raise HTTPException(status_code=400, detail="num_farmacia inválido")
    for linea in dev.lineas:
        if not linea.codigo_articulo.strip():
            raise HTTPException(status_code=400, detail="codigo_articulo inválido")
    nueva = crud.crear_devolucion(db, dev.num_farmacia, dev.user_id, [l.dict() for l in dev.lineas])
    return {"id_interno": nueva.id}