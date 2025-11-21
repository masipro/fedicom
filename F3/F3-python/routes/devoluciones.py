from flask import Blueprint, request, jsonify

devoluciones_bp = Blueprint('devoluciones', __name__)

@devoluciones_bp.route('/devoluciones', methods=['GET'])
def consulta_devolucion():
    return jsonify(ok=True, message="dummy consulta devolucion")

@devoluciones_bp.route('/devoluciones', methods=['POST'])
def crear_devolucion():
    return jsonify(ok=True, message="dummy crear devolucion")

@devoluciones_bp.route('/devoluciones/<numeroDevolucion>', methods=['GET'])
def consulta_devolucion_numero(numeroDevolucion):
    return jsonify(ok=True, message=f"dummy consulta devolucion {numeroDevolucion}")
