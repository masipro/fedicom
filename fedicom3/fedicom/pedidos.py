# fedicom/pedidos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import crud, database
from fedicom.auth import requiere_jwt

router = APIRouter(prefix="/pedidos", dependencies=[Depends(requiere_jwt)])

class LineaPedidoIn(BaseModel):
    codigo_articulo: str
    cantidad: float

class PedidoIn(BaseModel):
    numero_pedido_origen: str
    num_farmacia: str
    user_id: str
    lineas: list[LineaPedidoIn]

@router.post("")
def crear_pedido(pedido: PedidoIn, db: Session = Depends(database.get_db)):
    if not pedido.num_farmacia.strip():
        raise HTTPException(status_code=400, detail="num_farmacia inválido")
    for linea in pedido.lineas:
        if not linea.codigo_articulo.strip():
            raise HTTPException(status_code=400, detail="codigo_articulo inválido")
    nuevo = crud.crear_pedido(db, pedido.numero_pedido_origen, pedido.num_farmacia, pedido.user_id, [l.dict() for l in pedido.lineas])
    return {"id_interno": nuevo.id, "numero_pedido_origen": pedido.numero_pedido_origen}