from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
import jwt, os, time

from db.models import get_db, User
from db.crud import (
    authenticate_user,
    create_user,
    change_password,
    get_user_by_username,
)

router = APIRouter()

# === Config JWT ===
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret_noloadivinarias")
ALGO = "HS256"
TOKEN_TTL_SECONDS = 8 * 60 * 60  # 8 horas

# === Esquema de seguridad para Swagger (Authorize) ===
security = HTTPBearer()  # <--- esto crea el "candadito" y el botón Authorize


class AuthRequest(BaseModel):
    user: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Obtiene el usuario actual a partir del token Bearer.
    Esta dependencia activa el candadito en Swagger.
    """
    token = credentials.credentials  # sólo el token, sin "Bearer "
    payload = decode_token(token)
    username = payload.get("sub", "")
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol admin")
    return user


# ================== ENDPOINTS AUTH ==================


@router.post("/authenticate", summary="Login y obtención de JWT")
def authenticate(auth: AuthRequest, db: Session = Depends(get_db)):
    ok = authenticate_user(db, auth.user, auth.password)
    if not ok:
        raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")

    now = int(time.time())
    token = jwt.encode(
        {"sub": auth.user, "iat": now, "exp": now + TOKEN_TTL_SECONDS},
        SECRET_KEY,
        algorithm=ALGO,
    )
    return {"auth_token": token}


@router.post(
    "/users",
    summary="Crear usuario (requiere admin)",
    description="Crea un usuario nuevo en la BBDD. Sólo accesible con rol admin.",
)
def create_user_endpoint(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    try:
        u = create_user(db, data.username, data.password, data.role)
        return {"id": u.id, "username": u.username, "role": u.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/users/change-password",
    summary="Cambiar contraseña (usuario autenticado)",
)
def change_password_endpoint(
    data: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        change_password(db, user.username, data.old_password, data.new_password)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/token/verify",
    summary="Verificar token actual",
    description="Comprueba que el token Bearer es válido.",
)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    decode_token(credentials.credentials)
    return {"status": "valid"}
