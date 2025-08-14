from datetime import datetime, timedelta, timezone
from typing import Any
from src.api.auth.reponse import AuthTokensSchema
import jwt

from src.config import config
from src.enums.user_role import UserRole


class JWTService:
    def __init__(self) -> None:
        self.secret_key: str = config.JWT_SECRET_KEY
        self.algorithm: str = config.JWT_ALGORITHM
        self.access_token_expire_minutes: int = config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days: int = config.JWT_REFRESH_TOKEN_EXPIRE_DAYS

    def _create_token(self, payload: dict[str, Any], expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_access_token(self, user_id: int, role: UserRole) -> str:
        payload = {
            "sub": str(user_id),
            "role": role.value,
        }
        return self._create_token(payload, timedelta(minutes=self.access_token_expire_minutes))

    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
        }
        return self._create_token(payload, timedelta(days=self.refresh_token_expire_days))

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def create_token_pair(self, user_id: int, role: UserRole) -> AuthTokensSchema:
        return AuthTokensSchema(
            access_token=self.create_access_token(user_id=user_id, role=role),
            refresh_token=self.create_refresh_token(user_id=user_id),
            token_type="Bearer",
        )

