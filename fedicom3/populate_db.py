from db.database import SessionLocal
from db.models import Producto, Farmacia, User, Albaran, LineaAlbaran, Factura
from db.crud import create_user
from datetime import date

def main():
    db = SessionLocal()
    if not db.query(Farmacia).first():
        db.add_all([Farmacia(codigo="F123"), Farmacia(codigo="F999")])
    if not db.query(Producto).first():
        db.add_all([Producto(codigo="ART001", stock=100), Producto(codigo="ART002", stock=0)])
    if not db.query(User).first():
        create_user(db, "admin", "administrat0r", role="admin")
    if not db.query(Albaran).first():
        a1 = Albaran(numeroAlbaran="A001", fechaAlbaran=date(2025,1,10), codigoCliente="F123",
                     numeroPedido="PED-1001", numeroPedidoOrigen="PV001", almacen="0400",
                     importeNeto=20.0, importeBruto=24.2)
        a1.lineas = [
            LineaAlbaran(orden=1, codigoArticulo="ART001", descripcionArticulo="Producto 1", cantidad=2, precioUnitario=10.0, importeTotal=20.0)
        ]
        a2 = Albaran(numeroAlbaran="A002", fechaAlbaran=date(2025,1,12), codigoCliente="F123",
                     numeroPedido="PED-1002", numeroPedidoOrigen="PV002", almacen="0400",
                     importeNeto=0.0, importeBruto=0.0)
        db.add_all([a1, a2])
    if not db.query(Factura).first():
        f1 = Factura(numeroFactura="F2025-0001", fechaFactura=date(2025,1,15), codigoCliente="F123",
                     almacen="0400", importeNeto=20.0, importeBruto=24.2, vencimiento=date(2025,2,15))
        db.add(f1)
    db.commit()
    db.close()
    print("BBDD inicial lista (usuarios, farmacias, productos, albaranes, facturas).")

if __name__ == "__main__":
    main()