import os, base64, hashlib, hmac, re

PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{6,}$')

def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return base64.b64encode(dk).decode('utf-8'), base64.b64encode(salt).decode('utf-8')

def verify_password(password: str, password_hash_b64: str, salt_b64: str) -> bool:
    salt = base64.b64decode(salt_b64.encode('utf-8'))
    expected = base64.b64decode(password_hash_b64.encode('utf-8'))
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return hmac.compare_digest(dk, expected)

def validate_password_strength(pw: str):
    if not PASSWORD_REGEX.match(pw):
        raise ValueError("La contraseña debe tener mínimo 6 caracteres y ser alfanumérica.")