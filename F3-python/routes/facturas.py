from flask import Blueprint, request, jsonify

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/facturas', methods=['GET'])
def listado_facturas():
    return jsonify(ok=True, message="dummy listado facturas")

@facturas_bp.route('/facturas/<numeroFactura>', methods=['GET'])
def consulta_factura(numeroFactura):
    return jsonify(ok=True, message=f"dummy consulta factura {numeroFactura}")
