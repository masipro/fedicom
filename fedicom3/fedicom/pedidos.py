from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db.crud import insert_pedido, validate_farmacia, validate_articulo
from db.models import get_db, User
from .auth import get_current_user

router = APIRouter()

class LineaPedido(BaseModel):
    codigoArticulo: str
    cantidad: int

class Pedido(BaseModel):
    numeroPedidoOrigen: str
    num_farmacia: str
    lineas: list[LineaPedido]

@router.post("/pedidos")
def crear_pedido(pedido: Pedido, user: User = Depends(get_current_user), db=Depends(get_db)):
    validate_farmacia(pedido.num_farmacia, db)
    for linea in pedido.lineas:
        validate_articulo(linea.codigoArticulo, db)
    id_interno = insert_pedido(pedido, db)
    return {"id_interno": id_interno, "status": "recibido"}