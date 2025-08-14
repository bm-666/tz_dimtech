
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from starlette import status

from src.api.payments.service.payments_api_service import PaymentApiService
from src.api.accounts.service.accounts_api_service import AccountsApiService
from src.api.auth.services.jwt_service import JWTService
from src.helpers.helper import get_jwt_service
from src.schemas.user_shemas import UserReadSchema
from src.services.user_service import UserService
from src.helpers.exceptions.http_exceptions import ForbiddenError

from src.enums.user_role import UserRole
from src.api.users.user_api_service import UserApiService
from src.helpers.helper import get_session


security = HTTPBearer()

async def get_user_service() -> UserService:
    async with get_session() as session:
        return UserService(session)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
) -> UserReadSchema:  # ✅ корректно
    token = credentials.credentials

    try:
        payload = jwt_service.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный JWT токен",
        )

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не содержит идентификатор пользователя",
        )

    user = await user_service.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user  # если это UserReadSchema — всё ок

def require_roles(*allowed_roles: UserRole):
    """Фабрика зависимостей для проверки роли"""
    async def dependency(
        user: Annotated[UserReadSchema, Depends(get_current_user)]
    ) -> UserReadSchema:
        if user.role not in allowed_roles:
            raise ForbiddenError()
        return user
    return dependency

async def get_user_api_service() -> UserApiService:
    async with get_session() as session:
        return UserApiService(session)

async def get_account_api_service() -> AccountsApiService:
    async with get_session() as session:
        return AccountsApiService(session)

async def get_payment_api_service() -> PaymentApiService:
    async with get_session() as session:
        return PaymentApiService(session)