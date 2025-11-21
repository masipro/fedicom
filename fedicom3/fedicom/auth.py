from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt, datetime

SECRET_KEY = "supersecreto"
ALGORITHM = "HS256"

router = APIRouter()

class AuthRequest(BaseModel):
    user: str
    password: str

@router.post("/authenticate")
def authenticate(auth: AuthRequest):
    if auth.user == "admin" and auth.password == "admin":
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"sub": auth.user, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
        return {"auth_token": token}
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# dependencia para usar en endpoints protegidos
from fastapi.security import HTTPBearer
security = HTTPBearer()

def requiere_jwt(credentials=Depends(security)):
    return verificar_token(credentials.credentials)
