
from typing import Dict

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from config import API_VERSION
from database import get_db
from fedicom.schemas.auth import AuthRequest, TokenResponse
from fedicom.models import User
from fedicom.auth_utils import verify_password, create_jwt, AuthError
from fedicom.api.deps import common_headers

router = APIRouter(tags=["Autenticación"])


@router.post("/authenticate", response_model=TokenResponse, status_code=201)
def authenticate(
    auth: AuthRequest,
    db: Session = Depends(get_db),
    headers: Dict[str, str] = Depends(common_headers),
    response: Response = None,
) -> TokenResponse:
    user = db.query(User).filter(User.username == auth.user).first()
    if not user:
        raise AuthError("AUTH-005", "Usuario o contraseña inválidos", status_code=401)
    if not verify_password(auth.password, user.password_hash, user.salt):
        raise AuthError("AUTH-005", "Usuario o contraseña inválidos", status_code=401)

    token = create_jwt(
        sub=user.username,
        extra_claims={"nombre": "Usuario Fedicom", "admin": str(user.is_admin).lower()},
    )

    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    return TokenResponse(auth_token=token)
