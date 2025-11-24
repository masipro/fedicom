
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Devolucion(Base):
    __tablename__ = "devoluciones"

    id = Column(Integer, primary_key=True, index=True)
    numero_devolucion = Column(String(50), unique=True, index=True, nullable=False)
    codigo_cliente = Column(String(20), nullable=False, index=True)
    fecha_devolucion = Column(String(19), nullable=False)
    raw_json = Column(Text, nullable=False)
