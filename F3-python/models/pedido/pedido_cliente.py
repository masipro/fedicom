import datetime
from models.error_fedicom import ErrorFedicom
from models.crc import generar as generar_crc
from global import validador
from .linea_pedido_cliente import LineaPedidoCliente

class PedidoCliente:
    def __init__(self, req):
        self.tx_id = req.txId
        json_data = req.get_json()

        self.metadatos = {
            'todas_lineas_invalidas': True,
            'crc_de_lineas': False,
            'crc_lineas': '',
            'fecha_recepcion': datetime.datetime.now()
        }

        error_fedicom = ErrorFedicom()
        validador.es_cadena_no_vacia(json_data.get('codigoCliente'), error_fedicom, 'PED-ERR-002', 'El campo "codigoCliente" es obligatorio')
        validador.es_cadena_no_vacia(json_data.get('numeroPedidoOrigen'), error_fedicom, 'PED-ERR-006', 'El campo "numeroPedidoOrigen" es obligatorio')
        validador.es_array_no_vacio(json_data.get('lineas'), error_fedicom, 'PED-ERR-004', 'El campo "lineas" no puede estar vacío')

        if error_fedicom.tiene_errores():
            raise error_fedicom

        self.codigo_cliente = json_data.get('codigoCliente').strip()
        self.numero_pedido_origen = json_data.get('numeroPedidoOrigen').strip()
        self.notificaciones = json_data.get('notificaciones')
        self.direccion_envio = json_data.get('direccionEnvio')
        self.codigo_almacen_servicio = json_data.get('codigoAlmacenServicio')
        self.tipo_pedido = json_data.get('tipoPedido')
        self.fecha_servicio = json_data.get('fechaServicio')
        self.aplazamiento = json_data.get('aplazamiento')
        self.observaciones = json_data.get('observaciones')
        self.nombre_consumidor_final = json_data.get('nombreConsumidorFinal')

        self.lineas = self._analizar_posiciones(json_data.get('lineas', []))

        self.login = {
            'username': req.token['sub'],
            'domain': req.token['aud']
        }

        if len(self.codigo_cliente) > 10:
            self.codigo_cliente = self.codigo_cliente[-10:]

        if len(self.lineas) > 0: # TODO: C.pedidos.umbralLineasCrc
            self.crc = generar_crc(self.codigo_cliente, self.metadatos['crc_lineas'], self.codigo_almacen_servicio, self.tipo_pedido)
            self.metadatos['crc_de_lineas'] = True
        else:
            self.crc = generar_crc(self.codigo_cliente, self.numero_pedido_origen, self.tipo_pedido)
            self.metadatos['crc_de_lineas'] = False

    def _analizar_posiciones(self, lineas_data):
        lineas = []
        ordenes = []
        crc_lineas = ''
        for i, linea_data in enumerate(sorted(lineas_data, key=lambda x: x.get('codigoArticulo', ''))):
            linea = LineaPedidoCliente(linea_data, self.tx_id, i)
            crc_lineas = generar_crc(crc_lineas, linea.crc)
            lineas.append(linea)
            if linea.orden is not None:
                ordenes.append(linea.orden)
            if linea.es_linea_correcta():
                self.metadatos['todas_lineas_invalidas'] = False

        self.metadatos['crc_lineas'] = crc_lineas

        siguiente_ordinal = 1
        for linea in lineas:
            if linea.orden is None:
                while siguiente_ordinal in ordenes:
                    siguiente_ordinal += 1
                linea.orden = siguiente_ordinal
                siguiente_ordinal += 1
        return lineas

    def contiene_lineas_validas(self):
        return not self.metadatos['todas_lineas_invalidas']

    def to_json(self, para_sap=True):
        json_data = {
            'codigoCliente': self.codigo_cliente,
            'numeroPedidoOrigen': self.numero_pedido_origen,
            'lineas': [linea.to_json(para_sap) for linea in self.lineas]
        }
        if self.notificaciones:
            json_data['notificaciones'] = self.notificaciones
        if self.direccion_envio:
            json_data['direccionEnvio'] = self.direccion_envio
        if self.codigo_almacen_servicio:
            json_data['codigoAlmacenServicio'] = self.codigo_almacen_servicio
        if self.tipo_pedido:
            json_data['tipoPedido'] = self.tipo_pedido
        if self.fecha_servicio:
            json_data['fechaServicio'] = self.fecha_servicio
        if self.aplazamiento:
            json_data['aplazamiento'] = self.aplazamiento
        if self.observaciones:
            json_data['observaciones'] = self.observaciones
        if hasattr(self, 'incidencias'):
            json_data['incidencias'] = self.incidencias

        if para_sap:
            json_data['sap_url_confirmacion'] = 'http://localhost:5000/confirmaPedido' # Dummy URL
            json_data['crc'] = self.crc
            json_data['login'] = self.login
            json_data['fecha_recepcion'] = self.metadatos['fecha_recepcion'].strftime('%Y%m%d')
            json_data['hora_recepcion'] = self.metadatos['fecha_recepcion'].strftime('%H%M%S')

        return json_data
