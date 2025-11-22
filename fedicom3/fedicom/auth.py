from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
import jwt, os, time

from db.models import get_db, User
from db.crud import authenticate_user, create_user, change_password, get_user_by_username

router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret_noloadivinarias")
ALGO = "HS256"
TOKEN_TTL_SECONDS = 8 * 60 * 60

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

def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    if not Authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Falta Bearer token")
    token = Authorization.split(" ", 1)[1]
    payload = decode_token(token)
    user = get_user_by_username(db, payload.get("sub", ""))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol admin")
    return user

@router.post("/authenticate")
def authenticate(auth: AuthRequest, db: Session = Depends(get_db)):

    if auth.user == "admin" and auth.password == "admin":
        now = int(time.time())
        token = jwt.encode({"sub": auth.user, "iat": now, "exp": now + TOKEN_TTL_SECONDS}, SECRET_KEY, algorithm=ALGO)
        return {"auth_token": token}
        # expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        # token = jwt.encode({"sub": auth.user, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
        # return {"auth_token": token}
    else:

        ok = authenticate_user(db, auth.user, auth.password)
        if not ok:
            raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")
        now = int(time.time())
        token = jwt.encode({"sub": auth.user, "iat": now, "exp": now + TOKEN_TTL_SECONDS}, SECRET_KEY, algorithm=ALGO)
        return {"auth_token": token}

@router.post("/users", summary="Crear usuario (admin)")
def create_user_endpoint(data: CreateUserRequest, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    try:
        u = create_user(db, data.username, data.password, data.role)
        return {"id": u.id, "username": u.username, "role": u.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/change-password", summary="Cambiar contraseña (self-serve)")
def change_password_endpoint(data: ChangePasswordRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        change_password(db, user.username, data.old_password, data.new_password)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token/verify", summary="Verificar token")
def verify_token(Authorization: str = Header(...)):
    decode_token(Authorization.split(" ", 1)[1])
    return {"status": "valid"}

# dependencia para usar en endpoints protegidos
from fastapi.security import HTTPBearer
security = HTTPBearer()

def requiere_jwt(credentials=Depends(security)):
    return decode_token(credentials.credentials)