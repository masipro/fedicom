
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Albaran(Base):
    __tablename__ = "albaranes"

    id = Column(Integer, primary_key=True, index=True)
    numero_albaran = Column(String(50), unique=True, index=True, nullable=False)
    codigo_cliente = Column(String(20), nullable=False, index=True)
    fecha_albaran = Column(String(10), nullable=False)
    numero_pedido = Column(String(50), nullable=True)
    numero_pedido_origen = Column(String(10), nullable=True)
    hora_albaran = Column(String(8), nullable=True)
    codigo_almacen = Column(String(10), nullable=True)
    descripcion_almacen = Column(String(100), nullable=True)
    raw_json = Column(Text, nullable=False)


class ConfirmacionAlbaranDB(Base):
    __tablename__ = "confirmaciones_albaran"

    id = Column(Integer, primary_key=True, index=True)
    numero_albaran = Column(String(50), nullable=False)
    fecha_albaran = Column(String(10), nullable=False)
    raw_json = Column(Text, nullable=False)
