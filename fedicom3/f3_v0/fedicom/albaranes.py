from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from db.models import get_db, User
from db.crud import search_albaranes, get_albaran_by_numero
from .auth import get_current_user

router = APIRouter()

@router.get("/albaran")
def listar_albaranes(
    codigoCliente: str | None = Query(None),
    numeroAlbaran: str | None = Query(None),
    numeroPedidoOrigen: str | None = Query(None),
    fechaDesde: str | None = Query(None, description="dd/MM/yyyy"),
    fechaHasta: str | None = Query(None, description="dd/MM/yyyy"),
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    fd = datetime.strptime(fechaDesde, "%d/%m/%Y").date() if fechaDesde else None
    fh = datetime.strptime(fechaHasta, "%d/%m/%Y").date() if fechaHasta else None
    total, rows = search_albaranes(db, codigoCliente, numeroAlbaran, numeroPedidoOrigen, fd, fh, offset, min(limit, 200))
    items = [{
        "numeroAlbaran": r.numeroAlbaran,
        "fechaAlbaran": r.fechaAlbaran.strftime("%d/%m/%Y"),
        "codigoCliente": r.codigoCliente,
        "numeroPedido": r.numeroPedido,
        "numeroPedidoOrigen": r.numeroPedidoOrigen,
        "almacen": r.almacen,
        "importeNeto": r.importeNeto,
        "importeBruto": r.importeBruto
    } for r in rows]
    return {"total": total, "items": items}

@router.get("/albaran/{numeroAlbaran}")
def obtener_albaran(
    numeroAlbaran: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alb = get_albaran_by_numero(db, numeroAlbaran)
    if not alb:
        raise HTTPException(status_code=404, detail="Albarán no encontrado")
    return {
        "numeroAlbaran": alb.numeroAlbaran,
        "fechaAlbaran": alb.fechaAlbaran.strftime("%d/%m/%Y"),
        "codigoCliente": alb.codigoCliente,
        "numeroPedido": alb.numeroPedido,
        "numeroPedidoOrigen": alb.numeroPedidoOrigen,
        "almacen": alb.almacen,
        "importeNeto": alb.importeNeto,
        "importeBruto": alb.importeBruto,
        "lineas": [{
            "orden": l.orden,
            "codigoArticulo": l.codigoArticulo,
            "descripcionArticulo": l.descripcionArticulo,
            "cantidad": l.cantidad,
            "precioUnitario": l.precioUnitario,
            "importeTotal": l.importeTotal
        } for l in alb.lineas]
    }
