class Sap:
    async def verificar_credenciales(self, solicitud):
        # Dummy implementation
        if solicitud.usuario == 'test' and solicitud.clave == 'test':
            return {'username': 'test'}
        else:
            return {}

    async def realizar_pedido(self, pedido):
        # Dummy implementation
        return {'crc': pedido['crc'], 'numeroPedido': 'dummy-sap-order-number'}

sap = Sap()
