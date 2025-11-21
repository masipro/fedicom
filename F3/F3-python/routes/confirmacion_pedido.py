from flask import Blueprint, request, jsonify

confirmacion_pedido_bp = Blueprint('confirmacion_pedido', __name__)

@confirmacion_pedido_bp.route('/confirmaPedido', methods=['POST'])
def confirma_pedido():
    return jsonify(ok=True, message="dummy confirma pedido")
