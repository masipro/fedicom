# db/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from .database import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    numero_pedido_origen = Column(String, index=True)
    num_farmacia = Column(String, index=True)
    user_id = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

class LineaPedido(Base):
    __tablename__ = "lineas_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    codigo_articulo = Column(String, index=True)
    cantidad = Column(Float)

class Devolucion(Base):
    __tablename__ = "devoluciones"
    id = Column(Integer, primary_key=True, index=True)
    num_farmacia = Column(String, index=True)
    user_id = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

class LineaDevolucion(Base):
    __tablename__ = "lineas_devolucion"
    id = Column(Integer, primary_key=True, index=True)
    devolucion_id = Column(Integer, ForeignKey("devoluciones.id"))
    codigo_articulo = Column(String, index=True)
    cantidad = Column(Float)

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    codigo_articulo = Column(String, unique=True, index=True)
    descripcion = Column(String)
    cantidad = Column(Float)

class Albaran(Base):
    __tablename__ = "albaranes"
    id = Column(Integer, primary_key=True, index=True)
    numero_albaran = Column(String, unique=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String, unique=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
