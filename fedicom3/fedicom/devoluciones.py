from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db.crud import insert_devolucion, validate_farmacia, validate_articulo
from db.models import get_db, User
from .auth import get_current_user

router = APIRouter()

class LineaDevolucion(BaseModel):
    codigoArticulo: str
    cantidad: int

class Devolucion(BaseModel):
    numeroPedidoOrigen: str
    num_farmacia: str
    lineas: list[LineaDevolucion]

@router.post("/devoluciones")
def crear_devolucion(devolucion: Devolucion, user: User = Depends(get_current_user), db=Depends(get_db)):
    validate_farmacia(devolucion.num_farmacia, db)
    for linea in devolucion.lineas:
        validate_articulo(linea.codigoArticulo, db)
    id_interno = insert_devolucion(devolucion, db)
    return {"id_interno": id_interno, "status": "recibido"}