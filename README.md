# fedicom
## BASIC RUN
```
uvicorn main:app --reload
```

# Fedicom3 Server (mock) — Pedidos, Devoluciones, Albaranes, Facturas

Basado en el PDF del protocolo: /mnt/data/007-Fedicom-3.4.15.pdf

## Setup
```
pip install -r requirements.txt
python populate_db.py
python main.py  # 127.0.0.1:50505
```
## Endpoints
- Auth: POST /authenticate, POST /users (admin), POST /users/change-password, POST /token/verify
- Pedidos: POST /pedidos (JWT)
- Devoluciones: POST /devoluciones (JWT)
- Albaranes: GET /albaran (filtros, paginación), GET /albaran/{numeroAlbaran}
- Facturas: GET /facturas (filtros, paginación), GET /facturas/{numeroFactura}
- Stock: GET /stock?codigo=