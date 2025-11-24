
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    numero_pedido = Column(String(50), unique=True, index=True, nullable=False)
    codigo_cliente = Column(String(20), nullable=False, index=True)
    numero_pedido_origen = Column(String(10), nullable=False)
    fecha_pedido = Column(String(19), nullable=False)  # dd/mm/yyyy HH:MM:SS
    fecha_servicio = Column(String(19), nullable=True)
    tipo_pedido = Column(String(20), nullable=True)
    aplazamiento = Column(Integer, nullable=True)
    raw_json = Column(Text, nullable=False)
