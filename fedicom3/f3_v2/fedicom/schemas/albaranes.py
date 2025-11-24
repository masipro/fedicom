
from typing import List, Optional

from .common import (
    FedicomBase,
    InformacionLote,
    InformacionCubeta,
    Impuesto,
    Descuento,
    Cargo,
    Incidencia,
)


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
