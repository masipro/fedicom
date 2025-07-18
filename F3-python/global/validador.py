from models.error_fedicom import ErrorFedicom

def existe(campo, error_fedicom, codigo_error, descripcion_error):
    if campo is None:
        if error_fedicom:
            error_fedicom.insertar(codigo_error, descripcion_error)
        return False
    return True

def es_cadena_no_vacia(campo, error_fedicom, codigo_error, descripcion_error):
    if not isinstance(campo, str) or not campo.strip():
        if error_fedicom:
            error_fedicom.insertar(codigo_error, descripcion_error)
        return False
    return True

def es_entero_positivo_mayor_que_cero(campo, error_fedicom, codigo_error, descripcion_error):
    if not isinstance(campo, int) or campo <= 0:
        if error_fedicom:
            error_fedicom.insertar(codigo_error, descripcion_error)
        return False
    return True

def es_entero_positivo(campo, error_fedicom, codigo_error, descripcion_error):
    if not isinstance(campo, int) or campo < 0:
        if error_fedicom:
            error_fedicom.insertar(codigo_error, descripcion_error)
        return False
    return True

def es_array_no_vacio(campo, error_fedicom, codigo_error, descripcion_error):
    if not isinstance(campo, list) or not campo:
        if error_fedicom:
            error_fedicom.insertar(codigo_error, descripcion_error)
        return False
    return True

# Dummy date validation functions
def es_fecha(campo, error_fedicom, codigo_error, descripcion_error):
    return True

def es_fecha_hora(campo, error_fedicom, codigo_error, descripcion_error):
    return True
