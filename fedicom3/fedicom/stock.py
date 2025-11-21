# fedicom/stock.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, database
from fedicom.auth import requiere_jwt

router = APIRouter(prefix="/stock", dependencies=[Depends(requiere_jwt)])

@router.get("")
def obtener_stock(codigo_articulo: str, db: Session = Depends(database.get_db)):
    st = crud.obtener_stock(db, codigo_articulo)
    if not st:
        raise HTTPException(status_code=404, detail="Artículo sin stock")
    return st