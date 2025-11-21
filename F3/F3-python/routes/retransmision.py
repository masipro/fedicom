from flask import Blueprint, request, jsonify

retransmision_bp = Blueprint('retransmision', __name__)

@retransmision_bp.route('/retransmitir/<txId>', methods=['GET'])
def retransmite_pedido(txId):
    return jsonify(ok=True, message=f"dummy retransmite pedido {txId}")
