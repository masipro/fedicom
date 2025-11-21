# fedicom/facturas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, database
from fedicom.auth import requiere_jwt

router = APIRouter(prefix="/facturas", dependencies=[Depends(requiere_jwt)])

@router.get("/{numero_factura}")
def obtener_factura(numero_factura: str, db: Session = Depends(database.get_db)):
    fact = crud.obtener_factura(db, numero_factura)
    if not fact:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return fact