import asyncio
from flask import Blueprint, request, jsonify
from models.pedido.pedido_cliente import PedidoCliente
from models.error_fedicom import ErrorFedicom
from interfaces.sap import sap
from interfaces.mongo import mongo
from global.tokens import verifica_permisos

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['POST'])
async def crear_pedido():

    # estado_token = verifica_permisos(req, res, {'admitirSimulaciones': True, 'simulacionRequiereSolicitudAutenticacion': True})
    # if not estado_token['ok']:
    #     return jsonify(estado_token['respuesta']), 401

    try:
        pedido_cliente = PedidoCliente(request)
    except ErrorFedicom as e:
        return jsonify(e.to_dict()), e.status_code

    if not pedido_cliente.contiene_lineas_validas():
        # This part of the logic is not fully implemented in the provided snippet
        return jsonify({'error': 'Todas las lineas contienen errores'}), 400

    # Dummy duplicate check
    # tx_original = await mongo.db.tx.find_one({'crc': pedido_cliente.crc})
    # if tx_original:
    #     return jsonify({'error': 'Pedido duplicado'}), 400

    try:
        respuesta_sap = await sap.realizar_pedido(pedido_cliente.to_json(para_sap=True))
        # Process sap response
        return jsonify(respuesta_sap), 201
    except Exception as e:
        # Simulate SAP error
        return jsonify({'error': str(e)}), 500


from bson import ObjectId

@pedidos_bp.route('/pedidos', methods=['GET'])
async def consulta_pedido():
    numero_pedido = request.args.get('numeroPedido')
    if not numero_pedido or not ObjectId.is_valid(numero_pedido):
        return jsonify({'error': 'El parámetro "numeroPedido" es inválido'}), 400

    db_tx = await mongo.consulta_tx_por_crc(numero_pedido)
    if db_tx and 'clientResponse' in db_tx:
        return jsonify(db_tx['clientResponse']['body']), 200
    else:
        return jsonify({'error': 'El pedido solicitado no existe'}), 404

@pedidos_bp.route('/pedidos/<numeroPedido>', methods=['GET'])
async def consulta_pedido_numero(numeroPedido):
    if not ObjectId.is_valid(numeroPedido):
        return jsonify({'error': 'El parámetro "numeroPedido" es inválido'}), 400

    db_tx = await mongo.consulta_tx_por_crc(numeroPedido)
    if db_tx and 'clientResponse' in db_tx:
        return jsonify(db_tx['clientResponse']['body']), 200
    else:
        return jsonify({'error': 'El pedido solicitado no existe'}), 404

@pedidos_bp.route('/pedidos', methods=['PUT'])
def actualizar_pedido():
    return jsonify(ok=True, message="dummy actualizar pedido")
