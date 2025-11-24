
from pydantic import BaseModel
from typing import Optional


class FedicomBase(BaseModel):
    class Config:
        extra = "allow"


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


class InformacionLote(FedicomBase):
    lote: str
    fechaCaducidad: str


class InformacionCubeta(FedicomBase):
    codigo: str
    unidades: int
