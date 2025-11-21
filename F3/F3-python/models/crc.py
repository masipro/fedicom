import hashlib

def generar(*valores):
    base = "".join(str(v) for v in valores if v is not None)
    hash_object = hashlib.sha1(base.encode())
    return hash_object.hexdigest()[1:25].upper()
