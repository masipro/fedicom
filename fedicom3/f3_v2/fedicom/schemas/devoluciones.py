
from typing import List, Optional

from .common import FedicomBase, ErrorItem


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
