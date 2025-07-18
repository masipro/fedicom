from flask import Blueprint, request, jsonify

albaranes_bp = Blueprint('albaranes', __name__)

@albaranes_bp.route('/albaranes', methods=['GET'])
def listado_albaranes():
    return jsonify(ok=True, message="dummy listado albaranes")

@albaranes_bp.route('/albaranes/confirmacion', methods=['POST'])
def confirmacion_albaran():
    return jsonify(ok=True, message="dummy confirmacion albaran")

@albaranes_bp.route('/albaranes/<numeroAlbaran>', methods=['GET'])
def consulta_albaran(numeroAlbaran):
    return jsonify(ok=True, message=f"dummy consulta albaran {numeroAlbaran}")
