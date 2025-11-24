
from typing import List, Optional

from .common import FedicomBase, Impuesto, Cargo


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
