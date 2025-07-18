from models.error_fedicom import ErrorFedicom

class SolicitudAutenticacion:
    def __init__(self, req):
        self.txId = req.txId
        json_data = req.get_json()

        if not json_data:
            raise ErrorFedicom('AUTH-001', 'No se ha enviado un JSON en el body', 400)

        errors = []
        if 'user' not in json_data or not json_data['user']:
            errors.append(ErrorFedicom('AUTH-003', 'El parámetro "user" es obligatorio').to_dict())
        if 'password' not in json_data or not json_data['password']:
            errors.append(ErrorFedicom('AUTH-004', 'El parámetro "password" es obligatorio').to_dict())

        if errors:
            raise ErrorFedicom('AUTH-002', 'Errores de validación', 400) # TODO: embed errors

        self.usuario = json_data['user'].strip()
        self.clave = json_data['password'].strip()
        self.dominio = json_data.get('domain', 'FEDICOM') # TODO: C.dominios.resolver

        self.metadatos = {
            'aciertoCache': False,
            'evitarCache': bool(json_data.get('noCache')),
            'debug': bool(json_data.get('debug'))
        }

    def es_transfer(self):
        # TODO: C.dominios.TRANSFER, C.dominios.FEDICOM
        return self.dominio == 'TRANSFER' or (self.dominio == 'FEDICOM' and self.usuario.startswith(('TR', 'TG', 'TP')))

    async def validar_credenciales(self):
        from interfaces.sap import sap
        from interfaces.ldap import ldap
        from models.error_fedicom import ErrorFedicom

        if self.dominio in ['FEDICOM', 'TRANSFER']:
            try:
                respuesta_sap = await sap.verificar_credenciales(self)
                if respuesta_sap.get('username'):
                    return {'tokenGenerado': True, 'respuesta': self.generar_respuesta_token(None), 'codigoEstado': 201}
                else:
                    return {'tokenGenerado': False, 'respuesta': ErrorFedicom('AUTH-005', 'Usuario o contraseña inválidos', 401), 'codigoEstado': 401}
            except Exception as e:
                # In the original code, a token is generated even if SAP call fails.
                return {'tokenGenerado': True, 'respuesta': self.generar_respuesta_token(None), 'codigoEstado': 201}
        elif self.dominio == 'HEFAME':
            try:
                grupos = await ldap.autenticar(self)
                return {'tokenGenerado': True, 'respuesta': self.generar_respuesta_token(grupos), 'codigoEstado': 201}
            except Exception as e:
                return {'tokenGenerado': False, 'respuesta': ErrorFedicom('AUTH-005', 'Usuario o contraseña inválidos', 401), 'codigoEstado': 401}
        else:
            return {'tokenGenerado': False, 'respuesta': ErrorFedicom('AUTH-005', 'Usuario o contraseña inválidos', 401), 'codigoEstado': 401}

    def generar_token(self, permisos):
        from global.tokens import generar_token
        return generar_token(self.txId, self, permisos)

    def generar_respuesta_token(self, grupos):
        from global.tokens import verificar_token
        token = self.generar_token(grupos)
        respuesta = {'auth_token': token}
        if self.metadatos['debug']:
            respuesta['data'] = verificar_token(token)
        return respuesta
