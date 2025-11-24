
import json
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from config import API_VERSION
from database import get_db
from fedicom.models import User, Cliente, Articulo, DevolucionDB
from fedicom.schemas.devoluciones import Devolucion
from fedicom.auth_utils import get_current_user
from fedicom.api.deps import common_headers, error_response

router = APIRouter(tags=["Devoluciones"])


@router.post("/devoluciones", response_model=List[Devolucion], status_code=201)
def crear_devolucion(
    devolucion: Devolucion,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> List[Devolucion]:
    cliente = db.query(Cliente).filter(Cliente.codigo_cliente == devolucion.codigoCliente).first()
    if not cliente:
        return error_response("DEV-ERR-002", "El parámetro “codigoCliente” es inválido")

    if not devolucion.lineas or len(devolucion.lineas) == 0:
        return error_response("DEV-ERR-003", "El parámetro “lineas” es inválido")

    agrupadas: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for idx, linea in enumerate(devolucion.lineas):
        if not linea.numeroAlbaran:
            return error_response("LIN-DEV-ERR-001", "El parámetro “numeroAlbaran” es inválido")
        if not linea.fechaAlbaran:
            return error_response("LIN-DEV-ERR-002", "El parámetro “fechaAlbaran” es inválido")
        if linea.cantidad <= 0:
            return error_response("LIN-DEV-ERR-004", "El parámetro “cantidad” es inválido")

        art = db.query(Articulo).filter(Articulo.codigo_articulo == linea.codigoArticulo).first()
        linea_dict = linea.dict()
        if not art:
            incidencias = linea_dict.get("incidencias") or []
            incidencias.append(
                {"codigo": "LIN-DEV-ERR-003", "descripcion": "El parámetro codigoArticulo es inválido"}
            )
            linea_dict["incidencias"] = incidencias

        if linea_dict.get("orden") is None:
            linea_dict["orden"] = idx

        clave = f"{linea.numeroAlbaran}|{linea.fechaAlbaran}"
        agrupadas[clave].append(linea_dict)

    respuestas: List[Devolucion] = []

    for clave, lineas in agrupadas.items():
        now = datetime.now()
        fecha_devolucion_str = now.strftime("%d/%m/%Y %H:%M:%S")

        devol_db = DevolucionDB(
            numero_devolucion="TEMP",
            codigo_cliente=devolucion.codigoCliente,
            fecha_devolucion=fecha_devolucion_str,
            raw_json="{}",
        )
        db.add(devol_db)
        db.flush()
        numero_dev = f"D{devol_db.id:08d}"

        devol_dict = {
            "numeroDevolucion": numero_dev,
            "fechaDevolucion": fecha_devolucion_str,
            "codigoCliente": devolucion.codigoCliente,
            "numeroAlbaranAbono": f"ABV{numero_dev}",
            "fechaAlbaranAbono": now.strftime("%d/%m/%Y"),
            "lineas": lineas,
            "observaciones": devolucion.observaciones,
            "incidencias": [],
        }

        devol_db.numero_devolucion = numero_dev
        devol_db.raw_json = json.dumps(devol_dict, ensure_ascii=False)
        db.flush()

        respuestas.append(Devolucion(**devol_dict))

    db.commit()

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    return respuestas


@router.get("/devoluciones/{numeroDevolucion}", response_model=Devolucion)
def obtener_devolucion(
    numeroDevolucion: str,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> Devolucion:
    devol_db = db.query(DevolucionDB).filter(DevolucionDB.numero_devolucion == numeroDevolucion).first()
    if not devol_db:
        return error_response("DEV-ERR-001", "La devolución solicitada no existe.", status_code=404)
    data = json.loads(devol_db.raw_json)
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    return data
