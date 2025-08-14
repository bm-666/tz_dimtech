from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.auth.request import AuthLoginRequest, RegisterUserRequest
from src.api.auth.reponse import AuthTokensSchema
from src.api.auth.services.auth_api_service import AuthAPIService
from src.api.auth.services.jwt_service import JWTService
from src.helpers.helper import get_auth_service, get_jwt_service

auth_route = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={
        401: {"description": "Unauthorized"},
        400: {"description": "Bad request"},
    }
)


@auth_route.post(
    "/register",
    response_model=AuthTokensSchema,
    status_code=HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="""
Создает нового пользователя в системе и возвращает пару токенов доступа (access и refresh).
После успешной регистрации пользователь сразу авторизован.
    """,
)
async def register_user(
    request: RegisterUserRequest,
    auth_service: AuthAPIService = Depends(get_auth_service),
    jwt_service: JWTService = Depends(get_jwt_service)
):
    """
    ### Процесс:
    1. Создаем пользователя с переданными данными
    2. Хэшируем пароль
    3. Сохраняем в базу
    4. Возвращаем пару JWT токенов

    - **email**: уникальный email пользователя
    - **password**: пароль (будет захэширован)
    - **role**: роль пользователя (`USER` или `ADMIN`)
    - **full_name**: полное имя пользователя
    """
    user = await auth_service.register_user(
        email=request.email,
        password=request.password,
        role=request.role,
        full_name=request.full_name
    )
    return jwt_service.create_token_pair(user_id=user.id, role=user.role)


@auth_route.post(
    "/login",
    response_model=AuthTokensSchema,
    status_code=HTTP_200_OK,
    summary="Авторизация пользователя",
    description="""
Аутентифицирует пользователя по email и паролю.  
При успешной авторизации возвращает пару токенов (access, refresh).
    """,
)
async def login(
    request: AuthLoginRequest,
    auth_service: AuthAPIService = Depends(get_auth_service),
    jwt_service: JWTService = Depends(get_jwt_service)
):
    """
    ### Процесс:
    1. Проверяем, что пользователь с таким email существует
    2. Валидируем пароль
    3. Генерируем пару JWT токенов

    - **email**: email зарегистрированного пользователя
    - **password**: пароль
    """
    user = await auth_service.authenticate(request.email, request.password)
    return jwt_service.create_token_pair(user_id=user.id, role=user.role)
