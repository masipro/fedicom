# populate_db.py
from sqlalchemy.orm import Session
from db import models, database

models.Base.metadata.create_all(bind=database.engine)

db = Session(bind=database.engine)

productos = [
    {"codigo_articulo": "1111111", "descripcion": "Paracetamol 500mg", "cantidad": 100},
    {"codigo_articulo": "2222222", "descripcion": "Ibuprofeno 400mg", "cantidad": 50},
    {"codigo_articulo": "3333333", "descripcion": "Amoxicilina 500mg", "cantidad": 75}
]

for prod in productos:
    if not db.query(models.Stock).filter(models.Stock.codigo_articulo == prod["codigo_articulo"]).first():
        db.add(models.Stock(**prod))

db.commit()
print("Base de datos poblada con datos de ejemplo.")