
import json
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from config import API_VERSION
from database import get_db
from fedicom.models import User, Cliente, Articulo, PedidoDB
from fedicom.schemas.pedidos import Pedido, PedidoResponse, PedidoModificacion
from fedicom.auth_utils import get_current_user
from fedicom.api.deps import common_headers, error_response

router = APIRouter(tags=["Pedidos"])


@router.post("/pedidos", response_model=PedidoResponse, status_code=201)
def crear_pedido(
    pedido: Pedido,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> PedidoResponse:
    cliente = db.query(Cliente).filter(Cliente.codigo_cliente == pedido.codigoCliente).first()
    if not cliente:
        return error_response("PED-ERR-002", "El parámetro “codigoCliente” es inválido")

    if not pedido.numeroPedidoOrigen or len(pedido.numeroPedidoOrigen) > 10:
        return error_response("PED-ERR-006", "El parámetro “numeroPedidoOrigen” es inválido")

    if not pedido.lineas or len(pedido.lineas) == 0:
        return error_response("PED-ERR-004", "El parámetro “lineas” es inválido")

    for linea in pedido.lineas:
        art = db.query(Articulo).filter(Articulo.codigo_articulo == linea.codigoArticulo).first()
        if not art:
            return error_response("LIN-PED-ERR-001", "El parámetro “codigoArticulo” es inválido")
        if linea.cantidad is not None and linea.cantidad <= 0:
            return error_response("LIN-PED-ERR-002", "El parámetro “cantidad” es inválido")

    now = datetime.now()
    fecha_pedido_str = now.strftime("%d/%m/%Y %H:%M:%S")
    fecha_servicio_str = pedido.fechaServicio or fecha_pedido_str

    pedido_dict = pedido.dict()
    pedido_dict["fechaPedido"] = fecha_pedido_str

    pedido_db = PedidoDB(
        numero_pedido="TEMP",
        codigo_cliente=pedido.codigoCliente,
        numero_pedido_origen=pedido.numeroPedidoOrigen,
        fecha_pedido=fecha_pedido_str,
        fecha_servicio=fecha_servicio_str,
        tipo_pedido=pedido.tipoPedido,
        aplazamiento=pedido.aplazamiento,
        raw_json="{}",
    )
    db.add(pedido_db)
    db.flush()

    numero_pedido_generado = f"{pedido_db.id:08d}"
    pedido_db.numero_pedido = numero_pedido_generado
    pedido_dict["numeroPedido"] = numero_pedido_generado

    for idx, linea in enumerate(pedido_dict["lineas"]):
        if linea.get("orden") is None:
            linea["orden"] = idx
        art = db.query(Articulo).filter(Articulo.codigo_articulo == linea["codigoArticulo"]).first()
        if art and not linea.get("descripcionArticulo"):
            linea["descripcionArticulo"] = art.descripcion

    pedido_db.raw_json = json.dumps(pedido_dict, ensure_ascii=False)
    db.commit()
    db.refresh(pedido_db)

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    return PedidoResponse(**pedido_dict)


@router.get("/pedidos/{numeroPedido}", response_model=PedidoResponse)
def obtener_pedido(
    numeroPedido: str,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> PedidoResponse:
    pedido_db = db.query(PedidoDB).filter(PedidoDB.numero_pedido == numeroPedido).first()
    if not pedido_db:
        return error_response("PED-ERR-001", "El pedido solicitado no existe.", status_code=404)
    data = json.loads(pedido_db.raw_json)
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    return data


@router.put("/pedidos/{numeroPedido}", response_model=PedidoResponse)
def modificar_pedido(
    numeroPedido: str,
    modificacion: PedidoModificacion,
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    db: Session = Depends(get_db),
    response: Response = None,
) -> PedidoResponse:
    if modificacion.numeroPedido != numeroPedido:
        return error_response("PED-ERR-005", "El parámetro “numeroPedido” es inválido")

    cliente = db.query(Cliente).filter(Cliente.codigo_cliente == modificacion.codigoCliente).first()
    if not cliente:
        return error_response("PED-ERR-002", "El parámetro “codigoCliente” es inválido")

    pedido_db = db.query(PedidoDB).filter(PedidoDB.numero_pedido == numeroPedido).first()
    if not pedido_db:
        return error_response("PED-ERR-001", "El pedido solicitado no existe.", status_code=404)

    pedido_json = json.loads(pedido_db.raw_json)
    lineas = pedido_json.get("lineas", [])

    lineas_por_clave: Dict[str, Dict[str, Any]] = {}
    for linea in lineas:
        clave = f"{linea.get('orden')}|{linea.get('codigoArticulo')}"
        lineas_por_clave[clave] = linea

    for linea_mod in modificacion.lineas:
        clave = f"{linea_mod.orden}|{linea_mod.codigoArticulo}"
        if clave not in lineas_por_clave:
            return error_response("LIN-PED-ERR-003", "El parámetro “orden” es inválido")
        if linea_mod.estadoServicio not in ("PA", "PR"):
            return error_response("LIN-PED-ERR-004", "El parámetro “estadoServicio” es inválido")
        linea = lineas_por_clave[clave]
        if linea_mod.estadoServicio == "PA":
            linea["estadoServicio"] = "SC"
        elif linea_mod.estadoServicio == "PR":
            linea["estadoServicio"] = "SR"

    pedido_db.raw_json = json.dumps(pedido_json, ensure_ascii=False)
    db.commit()
    db.refresh(pedido_db)

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    return PedidoResponse(**pedido_json)
