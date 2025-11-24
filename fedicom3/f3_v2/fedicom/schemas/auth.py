
from pydantic import BaseModel


class AuthRequest(BaseModel):
    user: str
    password: str


class TokenResponse(BaseModel):
    auth_token: str
