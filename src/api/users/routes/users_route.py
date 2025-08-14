from fastapi import APIRouter, Depends
from typing import List, Annotated

from src.api.dependencies import get_user_api_service, require_roles, get_current_user
from src.api.users.user_request import UserCreateRequest, UserUpdateRequest
from src.api.users.user_api_service import UserApiService
from src.api.accounts.service.accounts_api_service import AccountsApiService
from src.api.payments.service.payments_api_service import PaymentApiService
from src.models import UserModel
from src.enums.user_role import UserRole
from src.schemas.user_shemas import UserReadSchema
from src.api.users.users_response import UserResponse
from src.api.dependencies import get_account_api_service, get_payment_api_service

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# ------------------- User Endpoints ------------------- #

@users_router.get(
    "/me",
    response_model=UserReadSchema,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает информацию о текущем аутентифицированном пользователе."
)
async def get_me(current_user: UserReadSchema = Depends(get_current_user)):
    return current_user


@users_router.get(
    "/me/accounts",
    summary="Получить аккаунты текущего пользователя",
    description="Возвращает список всех аккаунтов, принадлежащих текущему пользователю."
)
async def get_my_accounts(
    current_user: UserReadSchema = Depends(get_current_user),
    service: AccountsApiService = Depends(get_account_api_service),
):
    return await service.get_accounts_by_user_id(current_user.id)


@users_router.get(
    "/me/payments",
    summary="Получить платежи текущего пользователя",
    description="Возвращает все платежи, совершенные текущим пользователем."
)
async def get_my_payments(
    current_user: UserModel = Depends(get_current_user),
    service: PaymentApiService = Depends(get_payment_api_service),
):
    return await service.get_user_payments(current_user.id)


@users_router.get(
    "/",
    response_model=list[UserResponse],
    summary="Список всех пользователей",
    description="Возвращает список всех пользователей. Доступно только администраторам."
)
async def list_users(
    _: UserModel = Depends(require_roles(UserRole.ADMIN)),
    service: UserApiService = Depends(get_user_api_service),
):
    return await service.get_users()


@users_router.get(
    "/{user_id}",
    response_model=UserReadSchema,
    summary="Получить пользователя по ID",
    description="Возвращает информацию о пользователе по его идентификатору. Доступно только администраторам."
)
async def get_user(
    user_id: int,
    _: UserModel = Depends(require_roles(UserRole.ADMIN)),
    service: UserApiService = Depends(get_user_api_service),
):
    return await service.get_user_by_id(user_id)


@users_router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Создать нового пользователя",
    description="Создает нового пользователя с указанным email, паролем, ролью и полным именем. Доступно только администраторам."
)
async def create_user(
    body: UserCreateRequest,
    _: Annotated[UserReadSchema, Depends(require_roles(UserRole.ADMIN))],
    service: UserApiService = Depends(get_user_api_service),
):
    user = await service.create_user(body.email, body.password, body.role, body.full_name)
    return UserResponse.model_validate(user)


@users_router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Обновить пользователя",
    description="Обновляет данные пользователя по ID. Доступно только администраторам."
)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    _: Annotated[UserReadSchema, Depends(require_roles(UserRole.ADMIN))],
    service: UserApiService = Depends(get_user_api_service),
):
    return await service.update_user(user_id, request)


@users_router.delete(
    "/{user_id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по ID. Доступно только администраторам."
)
async def delete_user(
    user_id: int,
    _: UserModel = Depends(require_roles(UserRole.ADMIN)),
    service: UserApiService = Depends(get_user_api_service),
):
    await service.delete_user(user_id)
    return {"status": "deleted"}
