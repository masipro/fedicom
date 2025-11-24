from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models import get_db, User
from .auth import get_current_user

router = APIRouter()

@router.get("/stock")
def consultar_stock(codigo: str = Query(...),db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    result = db.execute("SELECT stock FROM productos WHERE codigo = ?", (codigo,)).fetchone()
    return {"codigo": codigo, "stock": result[0] if result else 0}
