from flask import Blueprint, request, jsonify
from models.autenticacion.solicitud_autenticacion import SolicitudAutenticacion
from models.error_fedicom import ErrorFedicom

auth_bp = Blueprint('auth', __name__)

import asyncio
from flask import Blueprint, request, jsonify
from models.autenticacion.solicitud_autenticacion import SolicitudAutenticacion
from models.error_fedicom import ErrorFedicom

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authenticate', methods=['POST'])
async def autenticar():
    try:
        solicitud = SolicitudAutenticacion(request)
        resultado = await solicitud.validar_credenciales()
        if resultado['tokenGenerado']:
            return jsonify(resultado['respuesta']), resultado['codigoEstado']
        else:
            return jsonify(resultado['respuesta'].to_dict()), resultado['codigoEstado']
    except ErrorFedicom as e:
        return jsonify(e.to_dict()), e.status_code


from global.tokens import verificar_token as verificar_token_logic

@auth_bp.route('/authenticate', methods=['GET'])
def verificar_token():
    if request.token:
        token_data = verificar_token_logic(request.token)
        return jsonify(token=request.token, token_data=token_data)
    else:
        token_data = {'meta': {'ok': False, 'error': 'No se incluye token'}}
        return jsonify(token=request.token, token_data=token_data)
