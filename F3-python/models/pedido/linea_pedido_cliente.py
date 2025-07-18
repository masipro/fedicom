from models.error_fedicom import ErrorFedicom
from models.crc import generar as generar_crc
from global import validador

class LineaPedidoCliente:
    def __init__(self, json_data, tx_id, numero_posicion):
        self.metadatos = {'linea_incorrecta': False}
        self.incidencias = []

        error_fedicom = ErrorFedicom()
        if not validador.es_cadena_no_vacia(json_data.get('codigoArticulo'), error_fedicom, 'LIN-PED-ERR-001', 'El campo "codigoArticulo" es inválido'):
            self.metadatos['linea_incorrecta'] = True
            self.incidencias = error_fedicom.errors
            if validador.es_entero_positivo_mayor_que_cero(json_data.get('cantidad'), None, None, None):
                self.cantidad_falta = json_data.get('cantidad')
            if validador.es_entero_positivo_mayor_que_cero(json_data.get('cantidadBonificacion'), None, None, None):
                self.cantidad_bonificacion_falta = json_data.get('cantidadBonificacion')

        self.orden = json_data.get('orden')
        self.codigo_articulo = json_data.get('codigoArticulo', '').strip()
        self.codigo_ubicacion = json_data.get('codigoUbicacion')
        self.cantidad_bonificacion = json_data.get('cantidadBonificacion')
        self.cantidad = json_data.get('cantidad') or 1
        if self.cantidad <= 0:
            self.cantidad = 1 if not self.cantidad_bonificacion else 0

        self.vale_estupefaciente = json_data.get('valeEstupefaciente')
        self.condicion = json_data.get('condicion')
        self.servicio_demorado = json_data.get('servicioDemorado')
        self.fecha_limite_servicio = json_data.get('fechaLimiteServicio')
        self.observaciones = json_data.get('observaciones')

        self.crc = self._generar_crc()

    def es_linea_correcta(self):
        return not self.metadatos['linea_incorrecta']

    def _generar_crc(self):
        return generar_crc(
            self.codigo_articulo or '',
            self.cantidad or 1,
            self.cantidad_bonificacion or 0,
            self.vale_estupefaciente or ''
        )

    def to_json(self, para_sap=True):
        json_data = {}
        if self.orden is not None:
            json_data['orden'] = self.orden
        if self.codigo_articulo:
            json_data['codigoArticulo'] = self.codigo_articulo
        if self.codigo_ubicacion:
            json_data['codigoUbicacion'] = self.codigo_ubicacion
        if self.cantidad is not None:
            json_data['cantidad'] = self.cantidad
        if hasattr(self, 'cantidad_falta'):
            json_data['cantidadFalta'] = self.cantidad_falta
        if self.cantidad_bonificacion:
            json_data['cantidadBonificacion'] = self.cantidad_bonificacion
        if hasattr(self, 'cantidad_bonificacion_falta'):
            json_data['cantidadBonificacionFalta'] = self.cantidad_bonificacion_falta
        if self.vale_estupefaciente:
            json_data['valeEstupefaciente'] = self.vale_estupefaciente
        if self.condicion:
            json_data['condicion'] = self.condicion
        if self.servicio_demorado:
            json_data['servicioDemorado'] = self.servicio_demorado
            json_data['estadoServicio'] = 'SC'
        if self.fecha_limite_servicio:
            json_data['fechaLimiteServicio'] = self.fecha_limite_servicio
        if self.observaciones:
            json_data['observaciones'] = self.observaciones
        if self.incidencias:
            json_data['incidencias'] = self.incidencias

        if para_sap and self.metadatos['linea_incorrecta']:
            json_data['sap_ignore'] = True

        return json_data
