
from sqlalchemy import Column, Integer, String
from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    codigo_cliente = Column(String(20), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
