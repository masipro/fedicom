
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), unique=True, index=True, nullable=False)
    codigo_cliente = Column(String(20), nullable=False, index=True)
    fecha_factura = Column(String(10), nullable=False)
    fecha_vencimiento = Column(String(10), nullable=True)
    codigo_almacen = Column(String(10), nullable=True)
    descripcion_almacen = Column(String(100), nullable=True)
    raw_json = Column(Text, nullable=False)
