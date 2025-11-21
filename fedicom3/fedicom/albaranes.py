# fedicom/albaranes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, database
from fedicom.auth import requiere_jwt

router = APIRouter(prefix="/albaranes", dependencies=[Depends(requiere_jwt)])

@router.get("/{numero_albaran}")
def obtener_albaran(numero_albaran: str, db: Session = Depends(database.get_db)):
    alb = crud.obtener_albaran(db, numero_albaran)
    if not alb:
        raise HTTPException(status_code=404, detail="Albarán no encontrado")
    return alb