class Sap:
    async def verificar_credenciales(self, solicitud):
        # Dummy implementation
        if solicitud.usuario == 'test' and solicitud.clave == 'test':
            return {'username': 'test'}
        else:
            return {}

sap = Sap()
