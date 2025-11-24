from sqlalchemy.orm import Session
from db.models import User, Pedido, Devolucion, Producto, Farmacia, Albaran, LineaAlbaran, Factura
from db.security import hash_password, verify_password, validate_password_strength
import uuid, datetime

def create_user(db: Session, username: str, password: str, role: str = "user"):
    validate_password_strength(password)
    if db.query(User).filter(User.username == username).first():
        raise ValueError("Usuario ya existe")
    h, salt = hash_password(password)
    user = User(username=username, password_hash=h, salt=salt, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    return verify_password(password, user.password_hash, user.salt)

def change_password(db: Session, username: str, old_password: str, new_password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(old_password, user.password_hash, user.salt):
        raise ValueError("Credenciales inválidas")
    validate_password_strength(new_password)
    h, salt = hash_password(new_password)
    user.password_hash, user.salt = h, salt
    db.commit()
    return True

def insert_pedido(pedido, db: Session):
    new_id = str(uuid.uuid4())
    db_pedido = Pedido(numeroPedidoOrigen=pedido.numeroPedidoOrigen, num_farmacia=pedido.num_farmacia, user_id=new_id)
    db.add(db_pedido)
    db.commit()
    return new_id

def insert_devolucion(dev, db: Session):
    new_id = str(uuid.uuid4())
    db_dev = Devolucion(numeroPedidoOrigen=dev.numeroPedidoOrigen, num_farmacia=dev.num_farmacia, user_id=new_id)
    db.add(db_dev)
    db.commit()
    return new_id

def validate_farmacia(codigo, db: Session):
    if not db.query(Farmacia).filter(Farmacia.codigo == codigo).first():
        raise Exception("Farmacia no encontrada")

def validate_articulo(codigo, db: Session):
    if not db.query(Producto).filter(Producto.codigo == codigo).first():
        raise Exception("Artículo no encontrado")

def search_albaranes(db: Session, codigoCliente, numeroAlbaran, numeroPedidoOrigen, fechaDesde, fechaHasta, offset, limit):
    q = db.query(Albaran)
    if codigoCliente:
        q = q.filter(Albaran.codigoCliente == codigoCliente)
    if numeroAlbaran:
        q = q.filter(Albaran.numeroAlbaran == numeroAlbaran)
    if numeroPedidoOrigen:
        q = q.filter(Albaran.numeroPedidoOrigen == numeroPedidoOrigen)
    if fechaDesde:
        q = q.filter(Albaran.fechaAlbaran >= fechaDesde)
    if fechaHasta:
        q = q.filter(Albaran.fechaAlbaran <= fechaHasta)
    total = q.count()
    rows = q.order_by(Albaran.fechaAlbaran.desc()).offset(offset).limit(limit).all()
    return total, rows

def get_albaran_by_numero(db: Session, numero: str):
    return db.query(Albaran).filter(Albaran.numeroAlbaran == numero).first()

def search_facturas(db: Session, codigoCliente, numeroFactura, fechaDesde, fechaHasta, offset, limit):
    q = db.query(Factura)
    if codigoCliente:
        q = q.filter(Factura.codigoCliente == codigoCliente)
    if numeroFactura:
        q = q.filter(Factura.numeroFactura == numeroFactura)
    if fechaDesde:
        q = q.filter(Factura.fechaFactura >= fechaDesde)
    if fechaHasta:
        q = q.filter(Factura.fechaFactura <= fechaHasta)
    total = q.count()
    rows = q.order_by(Factura.fechaFactura.desc()).offset(offset).limit(limit).all()
    return total, rows

def get_factura_by_numero(db: Session, numero: str):
    return db.query(Factura).filter(Factura.numeroFactura == numero).first()