import json
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Depends, Header, Response, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import API_VERSION
from database import Base, engine, get_db
from models import (
    User,
    Cliente,
    Articulo,
    Pedido as PedidoDB,
    Devolucion as DevolucionDB,
    Factura as FacturaDB,
    Albaran as AlbaranDB,
    ConfirmacionAlbaranDB,
)
from schemas import (
    AuthRequest,
    TokenResponse,
    Pedido,
    PedidoResponse,
    PedidoModificacion,
    Devolucion,
    Factura,
    Albaran,
    ConfirmacionAlbaran,
    EndpointVersion,
)
from auth_utils import (
    verify_password,
    create_jwt,
    get_current_user,
    AuthError,
)

app = FastAPI(title="Fedicom 3.4.15 Mock Server", version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def common_headers(
    software_id: str = Header(..., alias="Software-ID"),
    content_api_version: str = Header(..., alias="Content-Api-Version"),
) -> Dict[str, str]:
    return {"software_id": software_id, "content_api_version": content_api_version}


def error_response(code: str, description: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=[{"codigo": code, "descripcion": description}],
        headers={"Content-Api-Version": API_VERSION},
    )


@app.exception_handler(AuthError)
async def auth_error_handler(request, exc: AuthError):
    return JSONResponse(
        status_code=exc.status_code,
        content=[{"codigo": exc.code, "descripcion": exc.description}],
        headers={"Content-Api-Version": API_VERSION},
    )


# -----------------------
#   AUTENTICACIÓN
# -----------------------
@app.post("/authenticate", response_model=TokenResponse, status_code=201, tags=["Autenticación"])
def authenticate(
    auth: AuthRequest,
    db: Session = Depends(get_db),
    headers: Dict[str, str] = Depends(common_headers),
    response: Response = None,
) -> TokenResponse:
    user = db.query(User).filter(User.username == auth.user).first()
    if not user:
        raise AuthError("AUTH-005", "Usuario o contraseña inválidos", status_code=401)
    if not verify_password(auth.password, user.password_hash, user.salt):
        raise AuthError("AUTH-005", "Usuario o contraseña inválidos", status_code=401)
    token = create_jwt(
        sub=user.username,
        extra_claims={"nombre": "Usuario Fedicom", "admin": str(user.is_admin).lower()},
    )
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    return TokenResponse(auth_token=token)


# -----------------------
#   GENERAL
# -----------------------
@app.get(
    "/endpoint-fedicom-protocol-versions",
    response_model=List[EndpointVersion],
    tags=["General"],
)
def get_endpoint_versions(
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    response: Response = None,
) -> List[EndpointVersion]:
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION
    endpoints = [
        EndpointVersion(
            url="/authenticate",
            method="POST",
            description="Autenticación",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/endpoint-fedicom-protocol-versions",
            method="GET",
            description="Consulta versiones del protocolo",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos",
            method="POST",
            description="Creación de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos/{numeroPedido}",
            method="GET",
            description="Consulta de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos/{numeroPedido}",
            method="PUT",
            description="Modificación de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/devoluciones",
            method="POST",
            description="Creación de devoluciones",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/devoluciones/{numeroDevolucion}",
            method="GET",
            description="Consulta de una devolución",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/facturas",
            method="GET",
            description="Consulta de facturas",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/facturas/{numeroFactura}",
            method="GET",
            description="Obtención de una factura",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes",
            method="GET",
            description="Consulta de albaranes",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes/{numeroAlbaran}",
            method="GET",
            description="Obtención de un albarán",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes/confirmacion",
            method="POST",
            description="Confirmación de recepción de albarán",
            version=API_VERSION,
        ),
    ]
    return endpoints


# -----------------------
#   PEDIDOS
# -----------------------
@app.post("/pedidos", response_model=PedidoResponse, status_code=201, tags=["Pedidos"])
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


@app.get("/pedidos/{numeroPedido}", response_model=PedidoResponse, tags=["Pedidos"])
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


@app.put("/pedidos/{numeroPedido}", response_model=PedidoResponse, tags=["Pedidos"])
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


# -----------------------
#   DEVOLUCIONES
# -----------------------
@app.post("/devoluciones", response_model=List[Devolucion], status_code=201, tags=["Devoluciones"])
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

    from collections import defaultdict

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


@app.get("/devoluciones/{numeroDevolucion}", response_model=Devolucion, tags=["Devoluciones"])
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


# -----------------------
#   FACTURAS
# -----------------------
@app.get("/facturas", response_model=List[Factura], tags=["Facturas"])
def consultar_facturas(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=50),
    numeroFactura: Optional[str] = None,
    numeroAlbaran: Optional[str] = None,   # no usado en este mock
    fechaAlbaran: Optional[str] = None,    # no usado en este mock
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


@app.get("/facturas/{numeroFactura}", response_model=Factura, tags=["Facturas"])
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


# -----------------------
#   ALBARANES
# -----------------------
@app.get("/albaranes", response_model=List[Albaran], tags=["Albaranes"])
def consultar_albaranes(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=50),
    numeroAlbaran: Optional[str] = None,
    fechaAlbaran: Optional[str] = None,  # no usado en este mock
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


@app.get("/albaranes/{numeroAlbaran}", response_model=Albaran, tags=["Albaranes"])
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


@app.post("/albaranes/confirmacion", response_model=ConfirmacionAlbaran, tags=["Albaranes"])
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
