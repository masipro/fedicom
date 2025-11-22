from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base, SessionLocal

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    role = Column(String, default="user")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    numeroPedidoOrigen = Column(String)
    num_farmacia = Column(String)
    user_id = Column(String)

class Devolucion(Base):
    __tablename__ = "devoluciones"
    id = Column(Integer, primary_key=True, index=True)
    numeroPedidoOrigen = Column(String)
    num_farmacia = Column(String)
    user_id = Column(String)

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True)
    stock = Column(Integer)

class Farmacia(Base):
    __tablename__ = "farmacias"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True)

class Albaran(Base):
    __tablename__ = "albaranes"
    id = Column(Integer, primary_key=True, index=True)
    numeroAlbaran = Column(String, unique=True, index=True, nullable=False)
    fechaAlbaran = Column(Date, nullable=False)
    codigoCliente = Column(String, index=True, nullable=False)
    numeroPedido = Column(String, index=True, nullable=True)
    numeroPedidoOrigen = Column(String, index=True, nullable=True)
    almacen = Column(String, nullable=True)
    importeNeto = Column(Float, default=0.0)
    importeBruto = Column(Float, default=0.0)
    lineas = relationship("LineaAlbaran", back_populates="albaran", cascade="all, delete-orphan")

class LineaAlbaran(Base):
    __tablename__ = "lineas_albaran"
    id = Column(Integer, primary_key=True, index=True)
    albaran_id = Column(Integer, ForeignKey("albaranes.id"), nullable=False)
    orden = Column(Integer, default=1)
    codigoArticulo = Column(String, index=True, nullable=False)
    descripcionArticulo = Column(String, nullable=True)
    cantidad = Column(Integer, default=0)
    precioUnitario = Column(Float, default=0.0)
    importeTotal = Column(Float, default=0.0)
    albaran = relationship("Albaran", back_populates="lineas")

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    numeroFactura = Column(String, unique=True, index=True, nullable=False)
    fechaFactura = Column(Date, nullable=False)
    codigoCliente = Column(String, index=True, nullable=False)
    almacen = Column(String, nullable=True)
    importeNeto = Column(Float, default=0.0)
    importeBruto = Column(Float, default=0.0)
    vencimiento = Column(Date, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()