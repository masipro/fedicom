from database import Base, engine, SessionLocal
from models import User, Cliente, Articulo, Factura, Albaran
from auth_utils import hash_password
import json


def main() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        password_hash, salt = hash_password("administrat0r")
        admin = User(username="admin", password_hash=password_hash, salt=salt, is_admin=True)
        db.add(admin)

        c1 = Cliente(codigo_cliente="4612547", nombre="Farmacia Central")
        c2 = Cliente(codigo_cliente="9999999", nombre="Farmacia Pruebas")
        db.add_all([c1, c2])

        articulos = [
            Articulo(codigo_articulo="84021545454572", descripcion="Artículo de prueba 1"),
            Articulo(codigo_articulo="84021545454533", descripcion="Artículo de prueba 2"),
            Articulo(codigo_articulo="8437011646361", descripcion="Artículo de prueba 3"),
            Articulo(codigo_articulo="84021545454574", descripcion="Artículo de prueba 4"),
            Articulo(codigo_articulo="84021888854577", descripcion="Artículo de prueba 5"),
        ]
        db.add_all(articulos)
        db.commit()

        factura1 = {
            "codigoCliente": "4612547",
            "numeroFactura": "FA600054",
            "fechaFactura": "11/05/2017",
            "fechaVencimiento": "15/08/2017",
            "codigoAlmacen": "19",
            "descipcionAlmacen": "Almacén Central",
            "albaranes": [],
            "totales": {
                "importeBruto": 539.13,
                "importeIva": 48.14,
                "importeRecargo": 7.50,
                "importeTotal": 594.77,
                "importeCargos": 0.00,
            },
            "impuestos": [],
            "cargos": [],
        }

        f1 = Factura(
            numero_factura=factura1["numeroFactura"],
            codigo_cliente=factura1["codigoCliente"],
            fecha_factura=factura1["fechaFactura"],
            fecha_vencimiento=factura1["fechaVencimiento"],
            codigo_almacen=factura1["codigoAlmacen"],
            descripcion_almacen=factura1["descipcionAlmacen"],
            raw_json=json.dumps(factura1, ensure_ascii=False),
        )
        db.add(f1)

        albaran1 = {
            "codigoCliente": "4612547",
            "numeroAlbaran": "AV2600054",
            "fechaAlbaran": "02/10/2016",
        }

        a1 = Albaran(
            numero_albaran=albaran1["numeroAlbaran"],
            codigo_cliente=albaran1["codigoCliente"],
            fecha_albaran=albaran1["fechaAlbaran"],
            numero_pedido="00000001",
            numero_pedido_origen="ABC123",
            hora_albaran="10:30:00",
            codigo_almacen="19",
            descripcion_almacen="Almacén Central",
            raw_json=json.dumps(albaran1, ensure_ascii=False),
        )
        db.add(a1)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
