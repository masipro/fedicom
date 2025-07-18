import jwt
import time
from config import Config
from models.error_fedicom import ErrorFedicom

def generar_token(tx_id, autenticacion, permisos):
    payload = {
        'sub': autenticacion.usuario,
        'aud': autenticacion.dominio,
        'exp': int(time.time()) + Config.JWT_TTL,
        'jti': tx_id
    }
    if permisos:
        payload['perms'] = permisos

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    if not token:
        return {
            'meta': {
                'ok': False,
                'error': 'No se especifica token',
                'errorFedicom': ErrorFedicom('AUTH-002', 'Token inválido', 401)
            }
        }
    try:
        decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        decoded['meta'] = {'ok': True}
        return decoded
    except jwt.ExpiredSignatureError:
        return {
            'meta': {
                'ok': False,
                'error': 'Token caducado',
                'errorFedicom': ErrorFedicom('AUTH-001', 'Usuario no autentificado', 401)
            }
        }
    except jwt.InvalidTokenError as e:
        return {
            'meta': {
                'ok': False,
                'error': str(e),
                'errorFedicom': ErrorFedicom('AUTH-002', 'Token inválido', 401)
            }
        }
