from flask import Flask, jsonify
from routes.autenticacion import auth_bp
from routes.pedidos import pedidos_bp
from routes.confirmacion_pedido import confirmacion_pedido_bp
from routes.devoluciones import devoluciones_bp
from routes.albaranes import albaranes_bp
from routes.facturas import facturas_bp
from routes.retransmision import retransmision_bp
from routes.logistica import logistica_bp
from middleware.tx_id import tx_id_middleware
from middleware.bearer_token import bearer_token_middleware

app = Flask(__name__)
tx_id_middleware(app)
bearer_token_middleware(app)

app.register_blueprint(auth_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(confirmacion_pedido_bp)
app.register_blueprint(devoluciones_bp)
app.register_blueprint(albaranes_bp)
app.register_blueprint(facturas_bp)
app.register_blueprint(retransmision_bp)
app.register_blueprint(logistica_bp)

@app.route('/ping')
def ping():
    return jsonify(ok=True)

if __name__ == '__main__':
    app.run(debug=True)
