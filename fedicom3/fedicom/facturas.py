from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from db.models import get_db, User
from db.crud import search_facturas, get_factura_by_numero
from .auth import get_current_user

router = APIRouter()

@router.get("/facturas")
def listar_facturas(
    codigoCliente: str | None = Query(None),
    numeroFactura: str | None = Query(None),
    fechaDesde: str | None = Query(None, description="dd/MM/yyyy"),
    fechaHasta: str | None = Query(None, description="dd/MM/yyyy"),
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    fd = datetime.strptime(fechaDesde, "%d/%m/%Y").date() if fechaDesde else None
    fh = datetime.strptime(fechaHasta, "%d/%m/%Y").date() if fechaHasta else None
    total, rows = search_facturas(db, codigoCliente, numeroFactura, fd, fh, offset, min(limit, 200))
    items = [{
        "numeroFactura": r.numeroFactura,
        "fechaFactura": r.fechaFactura.strftime("%d/%m/%Y"),
        "codigoCliente": r.codigoCliente,
        "almacen": r.almacen,
        "importeNeto": r.importeNeto,
        "importeBruto": r.importeBruto,
        "vencimiento": r.vencimiento.strftime("%d/%m/%Y") if r.vencimiento else None
    } for r in rows]
    return {"total": total, "items": items}

@router.get("/facturas/{numeroFactura}")
def obtener_factura(
    numeroFactura: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    fac = get_factura_by_numero(db, numeroFactura)
    if not fac:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return {
        "numeroFactura": fac.numeroFactura,
        "fechaFactura": fac.fechaFactura.strftime("%d/%m/%Y"),
        "codigoCliente": fac.codigoCliente,
        "almacen": fac.almacen,
        "importeNeto": fac.importeNeto,
        "importeBruto": fac.importeBruto,
        "vencimiento": fac.vencimiento.strftime("%d/%m/%Y") if fac.vencimiento else None
    }
