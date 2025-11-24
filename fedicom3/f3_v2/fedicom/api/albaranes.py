
import json
from datetime import datetime
from typing import Dict, Optional, List

from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session

from config import API_VERSION
from database import get_db
from fedicom.models import User, AlbaranDB, ConfirmacionAlbaranDB
from fedicom.schemas.albaranes import Albaran
from fedicom.schemas.confirmacion_albaran import ConfirmacionAlbaran
from fedicom.auth_utils import get_current_user
from fedicom.api.deps import common_headers, error_response

router = APIRouter(tags=["Albaranes"])


@router.get("/albaranes", response_model=List[Albaran])
def consultar_albaranes(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=50),
    numeroAlbaran: Optional[str] = None,
    fechaAlbaran: Optional[str] = None,
    numeroPedido: Optional[str] = None,
    numeroPedidoOrigen: Optional[str] = None,
    fechaDesde: Optional[str] = None,
    fechaHasta: Optional[str] = None,
    codigoCliente: str = Query(...),
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> List[Albaran]:
    if codigoCliente is None or codigoCliente == "":
        return error_response("ALB-ERR-002", "El parámetro “codigoCliente” es inválido")

    if offset < 0:
        return error_response("ALB-ERR-007", "El parámetro “offset” es inválido")
    if limit <= 0 or limit > 50:
        return error_response("ALB-ERR-008", "El parámetro “limit” es inválido")

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
        return error_response("ALB-ERR-005", "El parámetro “fechaDesde” es inválido")
    if fechaHasta and not d_hasta:
        return error_response("ALB-ERR-006", "El parámetro “fechaHasta” es inválido")

    if d_desde and d_hasta:
        delta = (d_hasta - d_desde).days
        if delta < 0 or delta > 366:
            return error_response(
                "ALB-ERR-009",
                "El intervalo entre “fechaDesde” y “fechaHasta” no puede ser superior a un año.",
            )

    q = db.query(AlbaranDB).filter(AlbaranDB.codigo_cliente == codigoCliente)
    if numeroAlbaran:
        q = q.filter(AlbaranDB.numero_albaran == numeroAlbaran)
    if numeroPedido:
        q = q.filter(AlbaranDB.numero_pedido == numeroPedido)
    if numeroPedidoOrigen:
        q = q.filter(AlbaranDB.numero_pedido_origen == numeroPedidoOrigen)

    total = q.count()
    filas = q.offset(offset).limit(limit).all()
    resultado = [json.loads(a.raw_json) for a in filas]

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
        response.headers["X-Total-Count"] = str(total)

    return resultado


@router.get("/albaranes/{numeroAlbaran}", response_model=Albaran)
def obtener_albaran(
    numeroAlbaran: str,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> Albaran:
    albaran_db = db.query(AlbaranDB).filter(AlbaranDB.numero_albaran == numeroAlbaran).first()
    if not albaran_db:
        return error_response("ALB-ERR-001", "El albarán solicitado no existe", status_code=404)
    data = json.loads(albaran_db.raw_json)
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    return data


@router.post("/albaranes/confirmacion", response_model=ConfirmacionAlbaran)
def confirmar_albaran(
    confirmacion: ConfirmacionAlbaran,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> ConfirmacionAlbaran:
    albaran_db = db.query(AlbaranDB).filter(AlbaranDB.numero_albaran == confirmacion.numeroAlbaran).first()
    if not albaran_db:
        return error_response("CONF-ERR-001", "El albarán indicado no existe.", status_code=400)

    conf_db = ConfirmacionAlbaranDB(
        numero_albaran=confirmacion.numeroAlbaran,
        fecha_albaran=confirmacion.fechaAlbaran,
        raw_json=json.dumps(confirmacion.dict(), ensure_ascii=False),
    )
    db.add(conf_db)
    db.commit()

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    return confirmacion
