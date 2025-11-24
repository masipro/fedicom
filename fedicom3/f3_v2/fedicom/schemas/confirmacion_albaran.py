
from typing import List, Optional

from .common import FedicomBase, ErrorItem


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
