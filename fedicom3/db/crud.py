# db/crud.py
from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def crear_pedido(db: Session, numero_pedido_origen: str, num_farmacia: str, user_id: str, lineas: list):
    pedido = models.Pedido(
        numero_pedido_origen=numero_pedido_origen,
        num_farmacia=num_farmacia,
        user_id=user_id,
        fecha=datetime.utcnow()
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    for linea in lineas:
        lp = models.LineaPedido(
            pedido_id=pedido.id,
            codigo_articulo=linea["codigo_articulo"],
            cantidad=linea["cantidad"]
        )
        db.add(lp)
    db.commit()
    return pedido

def crear_devolucion(db: Session, num_farmacia: str, user_id: str, lineas: list):
    devolucion = models.Devolucion(
        num_farmacia=num_farmacia,
        user_id=user_id,
        fecha=datetime.utcnow()
    )
    db.add(devolucion)
    db.commit()
    db.refresh(devolucion)
    for linea in lineas:
        ld = models.LineaDevolucion(
            devolucion_id=devolucion.id,
            codigo_articulo=linea["codigo_articulo"],
            cantidad=linea["cantidad"]
        )
        db.add(ld)
    db.commit()
    return devolucion

def obtener_stock(db: Session, codigo_articulo: str):
    return db.query(models.Stock).filter(models.Stock.codigo_articulo == codigo_articulo).first()

def obtener_albaran(db: Session, numero_albaran: str):
    return db.query(models.Albaran).filter(models.Albaran.numero_albaran == numero_albaran).first()

def obtener_factura(db: Session, numero_factura: str):
    return db.query(models.Factura).filter(models.Factura.numero_factura == numero_factura).first()