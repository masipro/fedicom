from flask import Blueprint, request, jsonify

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET'])
def consulta_pedido():
    return jsonify(ok=True, message="dummy consulta pedido")

@pedidos_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    return jsonify(ok=True, message="dummy crear pedido")

@pedidos_bp.route('/pedidos', methods=['PUT'])
def actualizar_pedido():
    return jsonify(ok=True, message="dummy actualizar pedido")

@pedidos_bp.route('/pedidos/<numeroPedido>', methods=['GET'])
def consulta_pedido_numero(numeroPedido):
    return jsonify(ok=True, message=f"dummy consulta pedido {numeroPedido}")
