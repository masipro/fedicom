from fastapi import APIRouter, Depends, Query
from db.models import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/stock")
def consultar_stock(codigo: str = Query(...), db: Session = Depends(get_db)):
    result = db.execute("SELECT stock FROM productos WHERE codigo = ?", (codigo,)).fetchone()
    return {"codigo": codigo, "stock": result[0] if result else 0}