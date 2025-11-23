from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    salt = Column(String(32), nullable=False)
    is_admin = Column(Boolean, default=False)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    codigo_cliente = Column(String(20), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)


class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_articulo = Column(String(20), unique=True, index=True, nullable=False)
    descripcion = Column(String(200), nullable=False)


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


class Devolucion(Base):
    __tablename__ = "devoluciones"

    id = Column(Integer, primary_key=True, index=True)
    numero_devolucion = Column(String(50), unique=True, index=True, nullable=False)
    codigo_cliente = Column(String(20), nullable=False, index=True)
    fecha_devolucion = Column(String(19), nullable=False)
    raw_json = Column(Text, nullable=False)


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
