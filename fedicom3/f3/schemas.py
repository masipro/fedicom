from pydantic import BaseModel
from typing import List, Optional


class FedicomBase(BaseModel):
    class Config:
        extra = "allow"


class AuthRequest(BaseModel):
    user: str
    password: str


class TokenResponse(BaseModel):
    auth_token: str


class ErrorItem(FedicomBase):
    codigo: str
    descripcion: str


class Notificacion(FedicomBase):
    tipo: str
    valor: str


class Condicion(FedicomBase):
    codigo: str
    fechaInicio: Optional[str] = None
    fechaFin: Optional[str] = None


class ServicioAplazado(FedicomBase):
    fechaServicio: str
    cantidad: int


class Incidencia(FedicomBase):
    codigo: str
    descripcion: str


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


class LineaDevolucion(FedicomBase):
    orden: Optional[int] = None
    numeroAlbaran: str
    fechaAlbaran: str
    ordenLineaAlbaran: Optional[int] = None
    codigoArticulo: str
    descripcionArticulo: Optional[str] = None
    cantidad: int
    lote: Optional[str] = None
    fechaCaducidad: Optional[str] = None
    codigoMotivo: str
    descripcionMotivo: Optional[str] = None
    valeEstupefaciente: Optional[str] = None
    observaciones: Optional[str] = None
    incidencias: Optional[List[ErrorItem]] = None


class Devolucion(FedicomBase):
    numeroDevolucion: Optional[str] = None
    fechaDevolucion: Optional[str] = None
    codigoRecogida: Optional[str] = None
    codigoCliente: str
    numeroAlbaranAbono: Optional[str] = None
    fechaAlbaranAbono: Optional[str] = None
    empresaFacturadora: Optional[str] = None
    observaciones: Optional[str] = None
    lineas: List[LineaDevolucion]
    incidencias: Optional[List[ErrorItem]] = None


class Impuesto(FedicomBase):
    tipo: str
    base: float
    porcentaje: float
    importe: float
    porcentajeRecargo: Optional[float] = None
    importeRecargo: Optional[float] = None


class Descuento(FedicomBase):
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    porcentaje: Optional[float] = None
    importe: Optional[float] = None


class Cargo(FedicomBase):
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    base: Optional[float] = None
    porcentaje: Optional[float] = None
    importe: Optional[float] = None


class TotalFactura(FedicomBase):
    importeBruto: float
    importeIva: float
    importeRecargo: float
    importeTotal: float
    importeCargos: Optional[float] = None


class AlbaranFactura(FedicomBase):
    numeroAlbaran: str
    fechaAlbaran: str
    importeBruto: float
    importeNeto: Optional[float] = None
    codigoAlmacen: Optional[str] = None
    descipcionAlmacen: Optional[str] = None
    fechaVencimiento: Optional[str] = None


class Factura(FedicomBase):
    codigoCliente: str
    numeroFactura: str
    fechaFactura: str
    fechaVencimiento: Optional[str] = None
    codigoAlmacen: Optional[str] = None
    descipcionAlmacen: Optional[str] = None
    albaranes: List[AlbaranFactura]
    totales: TotalFactura
    impuestos: List[Impuesto]
    cargos: Optional[List[Cargo]] = None


class InformacionLote(FedicomBase):
    lote: str
    fechaCaducidad: str


class InformacionCubeta(FedicomBase):
    codigo: str
    unidades: int


class PedidoAlbaran(FedicomBase):
    numeroPedido: str
    numeroPedidoOrigen: Optional[str] = None
    tipoPedido: Optional[str] = None
    aplazamiento: Optional[int] = None
    canal: Optional[str] = None


class TotalAlbaran(FedicomBase):
    lineas: int
    lineasServidas: int
    lineasFalta: Optional[int] = None
    lineasBonificadas: Optional[int] = None
    cantidadPedida: Optional[int] = None
    cantidadServida: int
    cantidadBonificada: Optional[int] = None
    precioPvp: Optional[float] = None
    precioPvf: Optional[float] = None
    precioPvl: Optional[float] = None
    precioNeto: Optional[float] = None
    precioAlbaran: float
    impuestos: Optional[List[Impuesto]] = None
    descuentos: Optional[List[Descuento]] = None
    cargos: Optional[List[Cargo]] = None


class LineaAlbaran(FedicomBase):
    orden: int
    codigoArticulo: str
    descripcionArticulo: Optional[str] = None
    pedido: Optional[PedidoAlbaran] = None
    modelo: Optional[str] = None
    lotes: Optional[List[InformacionLote]] = None
    cubeta: Optional[List[InformacionCubeta]] = None
    cantidadPedida: Optional[int] = None
    cantidadServida: int
    cantidadBonificada: Optional[int] = None
    precioPvp: Optional[float] = None
    precioPvf: Optional[float] = None
    precioPvl: Optional[float] = None
    precioAlbaran: float
    precioNeto: float
    importeLineaBruto: Optional[float] = None
    importeLineaNeto: Optional[float] = None
    impuesto: Optional[Impuesto] = None
    descuento: Optional[List[Descuento]] = None
    cargo: Optional[List[Cargo]] = None
    observaciones: Optional[str] = None
    incidencias: Optional[List[Incidencia]] = None


class Albaran(FedicomBase):
    codigoCliente: str
    numeroAlbaran: str
    fechaAlbaran: str
    horaAlbaran: Optional[str] = None
    numeroFactura: Optional[str] = None
    fechaFactura: Optional[str] = None
    codigoAlmacen: Optional[str] = None
    descripcionAlmacen: Optional[str] = None
    reparto: Optional[str] = None
    operador: Optional[str] = None
    ruta: Optional[str] = None
    pedidos: Optional[List[PedidoAlbaran]] = None
    lineas: List[LineaAlbaran]
    totales: TotalAlbaran
    impuestos: Optional[List[Impuesto]] = None


class LineaConfirmacionAlbaran(FedicomBase):
    codigoArticulo: str
    lote: str
    fechaCaducidad: str
    unidades: int
    incidencias: Optional[List[ErrorItem]] = None


class ConfirmacionAlbaran(FedicomBase):
    numeroAlbaran: str
    fechaAlbaran: str
    lineas: List[LineaConfirmacionAlbaran]


class EndpointVersion(FedicomBase):
    url: str
    method: str
    description: str
    version: str
