import base64
import json
import hmac
import hashlib
import time
import secrets
from typing import Dict, Any, Optional

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Security
from sqlalchemy.orm import Session

from config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models import User


class AuthError(Exception):
    def __init__(self, code: str, description: str, status_code: int) -> None:
        self.code = code
        self.description = description
        self.status_code = status_code


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_jwt(sub: str, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    header = {"typ": "JWT", "alg": JWT_ALGORITHM}
    iat = int(time.time())
    exp = iat + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload: Dict[str, Any] = {
        "iss": "",
        "iat": iat,
        "exp": exp,
        "aud": "",
        "sub": sub,
    }
    if extra_claims:
        payload.update(extra_claims)
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    if JWT_ALGORITHM != "HS256":
        raise ValueError("Only HS256 is supported")
    signature = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_jwt(token: str) -> Dict[str, Any]:
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        raise AuthError("AUTH-002", "Token inválido", status_code=401)
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = _b64url_decode(sig_b64)
    expected_sig = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_sig):
        raise AuthError("AUTH-002", "Token inválido", status_code=401)
    payload_json = _b64url_decode(payload_b64)
    payload = json.loads(payload_json)
    if "exp" in payload and int(time.time()) > int(payload["exp"]):
        raise AuthError("AUTH-002", "Token inválido", status_code=401)
    return payload


def hash_password(password: str, salt: Optional[str] = None) -> (str, str):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256()
    h.update((salt + password).encode("utf-8"))
    return h.hexdigest(), salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    h, _ = hash_password(password, salt)
    return h == password_hash


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthError("AUTH-001", "Usuario no autentificado", status_code=401)
    token = credentials.credentials
    payload = decode_jwt(token)
    username = payload.get("sub")
    if not username:
        raise AuthError("AUTH-002", "Token inválido", status_code=401)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise AuthError("AUTH-002", "Token inválido", status_code=401)
    return user
