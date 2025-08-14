import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth_schemas import UserAuthSchema
from src.schemas.user_shemas import UserReadSchema, UserCreateSchema
from src.services.user_service import UserService
from src.api.auth.request import AuthLoginRequest
from src.utils.security import verify_password, hash_password
from src.enums.user_role import UserRole

logger = logging.getLogger(__name__)


class AuthAPIService:
    """
    Сервис для работы с аутентификацией и регистрацией пользователей.
    Содержит логику валидации данных и делегирует операции UserService.
    """

    def __init__(self, session: AsyncSession):
        """
        :param session: асинхронная сессия SQLAlchemy
        """
        self.user_service = UserService(session=session)

    async def authenticate(self, email: str, password: str) -> UserAuthSchema:
        """
        Аутентифицирует пользователя по email и паролю.

        :param email: Email пользователя
        :param password: Пароль в открытом виде
        :raises HTTPException: 404, если пользователь не найден
                               401, если пароль неверный
        :return: UserAuthSchema
        """
        logger.info(f"🔍 Попытка входа: email={email}")

        user = await self.user_service.get_user_with_password(email=email)
        if not user:
            logger.warning(f"❌ Пользователь с email={email} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с email {email} не найден"
            )

        if not verify_password(password, user.hashed_password):
            logger.warning(f"🔑 Неверный пароль для email={email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        logger.info(f"✅ Успешная аутентификация пользователя: id={user.id}, email={email}")
        return user

    async def register_user(self, email: str, password: str, role: UserRole, full_name: str) -> UserReadSchema:
        """
        Регистрирует нового пользователя.

        :param email: Email пользователя
        :param password: Пароль
        :param role: Роль пользователя (UserRole)
        :param full_name: Полное имя
        :raises HTTPException: 400, если пользователь уже существует
        :return: UserReadSchema
        """
        logger.info(f"📝 Регистрация пользователя: email={email}, role={role}")

        existing_user = await self.user_service.get_by_email(email=email)
        if existing_user:
            logger.warning(f"⚠️ Пользователь с email={email} уже существует")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с email {email} уже зарегистрирован"
            )

        new_user = UserCreateSchema(
            email=email,
            hashed_password=hash_password(password),
            role=role,
            full_name=full_name,
        )
        created_user = await self.user_service.create(new_user)

        logger.info(f"🎉 Пользователь успешно зарегистрирован: id={created_user.id}, email={email}")
        return created_user
