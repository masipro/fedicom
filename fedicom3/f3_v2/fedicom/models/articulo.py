
from sqlalchemy import Column, Integer, String
from database import Base


class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_articulo = Column(String(20), unique=True, index=True, nullable=False)
    descripcion = Column(String(200), nullable=False)
