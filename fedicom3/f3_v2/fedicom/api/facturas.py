
import json
from datetime import datetime
from typing import Dict, Optional, List

from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session

from config import API_VERSION
from database import get_db
from fedicom.models import User, FacturaDB
from fedicom.schemas.facturas import Factura
from fedicom.auth_utils import get_current_user
from fedicom.api.deps import common_headers, error_response

router = APIRouter(tags=["Facturas"])


@router.get("/facturas", response_model=List[Factura])
def consultar_facturas(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=50),
    numeroFactura: Optional[str] = None,
    numeroAlbaran: Optional[str] = None,
    fechaAlbaran: Optional[str] = None,
    fechaDesde: Optional[str] = None,
    fechaHasta: Optional[str] = None,
    codigoCliente: str = Query(...),
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> List[Factura]:
    if codigoCliente is None or codigoCliente == "":
        return error_response("FACT-ERR-002", "El parámetro “codigoCliente” es inválido")

    if offset < 0:
        return error_response("FACT-ERR-008", "El parámetro “offset” es inválido")
    if limit <= 0 or limit > 50:
        return error_response("FACT-ERR-009", "El parámetro “limit” es inválido")

    def parse_date(value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            return None

    d_desde = parse_date(fechaDesde)
    d_hasta = parse_date(fechaHasta)

    if fechaDesde and not d_desde:
        return error_response("FACT-ERR-006", "El parámetro “fechaDesde” es inválido")
    if fechaHasta and not d_hasta:
        return error_response("FACT-ERR-007", "El parámetro “fechaHasta” es inválido")

    if d_desde and d_hasta:
        delta = (d_hasta - d_desde).days
        if delta < 0 or delta > 366:
            return error_response(
                "FACT-ERR-010",
                "El intervalo entre “fechaDesde” y “fechaHasta” no puede ser superior a un año.",
            )

    q = db.query(FacturaDB).filter(FacturaDB.codigo_cliente == codigoCliente)
    if numeroFactura:
        q = q.filter(FacturaDB.numero_factura == numeroFactura)

    total = q.count()
    filas = q.offset(offset).limit(limit).all()

    resultado = [json.loads(f.raw_json) for f in filas]

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
        response.headers["X-Total-Count"] = str(total)

    return resultado


@router.get("/facturas/{numeroFactura}", response_model=Factura)
def obtener_factura(
    numeroFactura: str,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> Factura:
    factura_db = db.query(FacturaDB).filter(FacturaDB.numero_factura == numeroFactura).first()
    if not factura_db:
        return error_response("FACT-ERR-001", "La factura solicitada no existe.", status_code=404)
    data = json.loads(factura_db.raw_json)
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    return data
