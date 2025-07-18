from flask import Blueprint, request, jsonify

logistica_bp = Blueprint('logistica', __name__)

@logistica_bp.route('/logistica', methods=['POST'])
def crear_logistica():
    return jsonify(ok=True, message="dummy crear logistica")

@logistica_bp.route('/logistica', methods=['GET'])
def consulta_logistica():
    return jsonify(ok=True, message="dummy consulta logistica")

@logistica_bp.route('/logistica/<numeroLogistica>', methods=['GET'])
def consulta_logistica_numero(numeroLogistica):
    return jsonify(ok=True, message=f"dummy consulta logistica {numeroLogistica}")
