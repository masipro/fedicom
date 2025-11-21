import sqlite3
import uuid
from bson import json_util
from config import Config

class SQLite:
    def __init__(self):
        self.connection = sqlite3.connect(Config.SQLITE_DB_PATH, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tx(uid TEXT PRIMARY KEY, txid TEXT, data TEXT, retryCount INTEGER)')

    def grabar_transaccion(self, transaccion):
        uid = str(uuid.uuid4())
        txid = transaccion['$setOnInsert']['_id']
        json_extendido = json_util.dumps(transaccion)

        try:
            self.cursor.execute(
                'INSERT INTO tx(uid, txid, data, retryCount) VALUES(?, ?, ?, ?)',
                (uid, txid, json_extendido, 0)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"*** FALLO AL GRABAR EN LA BASE DE DATOS DE RESPALDO - PELIGRO DE PERDIDA DE DATOS: {e}")
            return False

        return True

    def numero_entradas_pendientes(self):
        self.cursor.execute('SELECT count(*) as count FROM tx WHERE retryCount < ?', (Config.SQLITE_MAXIMO_REINTENTOS,))
        resultado = self.cursor.fetchone()
        return resultado['count'] if resultado else 0

    def obtener_entradas(self, numero_fallos_maximo=0, limite=0):
        sql = 'SELECT * FROM tx'
        parametros = []
        if numero_fallos_maximo > 0:
            sql += ' WHERE retryCount < ?'
            parametros.append(numero_fallos_maximo)
        sql += ' ORDER BY uid'
        if limite > 0:
            sql += ' LIMIT ?'
            parametros.append(limite)
        
        self.cursor.execute(sql, parametros)
        entradas = self.cursor.fetchall()
        
        entradas_saneadas = []
        for entrada in entradas:
            entrada_dict = dict(entrada)
            entrada_dict['data'] = json_util.loads(entrada_dict['data'])
            entradas_saneadas.append(entrada_dict)
        return entradas_saneadas

    def eliminar_entrada(self, uid):
        try:
            self.cursor.execute('DELETE FROM tx WHERE uid = ?', (uid,))
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"*** Fallo al borrar la entrada de la base de datos de respaldo: {e}")
            return 0

    def incrementar_numero_de_intentos(self, uid):
        try:
            self.cursor.execute('UPDATE tx SET retryCount = retryCount + 1 WHERE uid = ?', (uid,))
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"*** Fallo al incrementar el número de intentos para la entrada: {e}")
            return 0

    def recuento_registros(self):
        umbral_intentos_maximos = Config.SQLITE_MAXIMO_REINTENTOS
        self.cursor.execute('SELECT CASE WHEN retryCount BETWEEN 0 AND ? THEN "pendientes" ELSE "expiradas" END AS estado, count(*) AS cantidad FROM tx GROUP BY estado;', (umbral_intentos_maximos,))
        return self.cursor.fetchall()

    def consulta_registros(self, opciones):
        sql = 'SELECT uid, txid, data as transaccion, retryCount as intentos FROM tx'
        sql_contador = 'SELECT count(*) as count FROM tx'
        valores = []

        limite = min(opciones.get('limite', 50), 50)
        skip = max(opciones.get('skip', 0), 0)

        if 'filtro' in opciones:
            sql += ' ' + opciones['filtro']['sql']
            sql_contador += ' ' + opciones['filtro']['sql']
            valores = opciones['filtro']['valores']
        
        if 'orden' in opciones:
            sql += ' ORDER BY ' + opciones['orden']
        
        sql += ' LIMIT ?'
        valores.append(limite)
        sql += ' OFFSET ?'
        valores.append(skip)

        self.cursor.execute(sql_contador, valores[:-2]) # Exclude limit and offset for count
        numero_entradas = self.cursor.fetchone()['count']

        self.cursor.execute(sql, valores)
        entradas = self.cursor.fetchall()

        entradas_saneadas = []
        for entrada in entradas:
            entrada_dict = dict(entrada)
            entrada_dict['transaccion'] = json_util.loads(entrada_dict['transaccion'])
            entradas_saneadas.append(entrada_dict)

        return {
            'resultados': entradas_saneadas,
            'limite': limite,
            'skip': skip,
            'total': numero_entradas
        }

sqlite = SQLite()
