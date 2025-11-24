
from typing import List, Optional

from .common import FedicomBase, Notificacion, Condicion, ServicioAplazado, ErrorItem


class LineaPedido(FedicomBase):
    orden: Optional[int] = None
    codigoArticulo: str
    descripcionArticulo: Optional[str] = None
    codigoUbicacion: Optional[str] = None
    cantidad: Optional[int] = None
    cantidadFalta: Optional[int] = None
    cantidadBonificacion: Optional[int] = None
    cantidadBonificacionFalta: Optional[int] = None
    precio: Optional[float] = None
    codigoAlmacenServicio: Optional[str] = None
    condicion: Optional[Condicion] = None
    servicioDemorado: Optional[bool] = None
    estadoServicio: Optional[str] = None
    fechaLimiteServicio: Optional[str] = None
    servicioAplazado: Optional[ServicioAplazado] = None
    observaciones: Optional[str] = None
    incidencias: Optional[List[ErrorItem]] = None


class Pedido(FedicomBase):
    numeroPedido: Optional[str] = None
    codigoCliente: str
    notificaciones: Optional[List[Notificacion]] = None
    direccionEnvio: Optional[str] = None
    codigoAlmacenServicio: Optional[str] = None
    numeroPedidoOrigen: str
    tipoPedido: Optional[str] = None
    fechaPedido: Optional[str] = None
    fechaServicio: Optional[str] = None
    aplazamiento: Optional[int] = None
    empresaFacturadora: Optional[str] = None
    observaciones: Optional[str] = None
    lineas: List[LineaPedido]
    incidencias: Optional[List[ErrorItem]] = None
    alertas: Optional[List[str]] = None


class PedidoResponse(Pedido):
    numeroPedido: str
    fechaPedido: str


class PedidoModificacionLinea(FedicomBase):
    orden: int
    codigoArticulo: str
    estadoServicio: str


class PedidoModificacion(FedicomBase):
    numeroPedido: str
    codigoCliente: str
    numeroPedidoOrigen: Optional[str] = None
    lineas: List[PedidoModificacionLinea]
