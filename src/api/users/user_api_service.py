import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.user_request import UserUpdateRequest
from src.enums.user_role import UserRole
from src.schemas.user_shemas import UserUpdateSchema, UserReadSchema, UserCreateSchema
from src.services.user_service import UserService
from src.api.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from src.utils.security import hash_password
from src.api.users.users_response import UserResponse

logger = logging.getLogger(__name__)


class UserApiService:
    """
    Сервис для работы с пользователями: создание, получение, обновление, удаление.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация UserApiService с асинхронной сессией SQLAlchemy.

        :param session: асинхронная сессия базы данных
        """
        self.user_service = UserService(session)

    async def get_users(self) -> list[UserResponse]:
        """
        Получить список всех пользователей.

        :return: список пользователей в формате UserResponse
        """
        logger.info("👀 Запрос списка всех пользователей")
        users = await self.user_service.get()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserReadSchema:
        """
        Получить пользователя по ID.

        :param user_id: идентификатор пользователя
        :return: данные пользователя в формате UserReadSchema
        :raises HTTPException: если пользователь не найден
        """
        logger.info(f"🔍 Получение пользователя с id={user_id}")
        user = await self.user_service.get_by_id(user_id)
        if user is None:
            logger.warning(f"⚠️ Пользователь с id={user_id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с id={user_id} не найден"
            )
        logger.info(f"✅ Пользователь с id={user_id} найден")
        return user

    async def create_user(self, email: str, password: str, role: UserRole, full_name: str) -> UserReadSchema:
        """
        Создать нового пользователя.

        :param email: email пользователя
        :param password: пароль пользователя
        :param role: роль пользователя
        :param full_name: полное имя пользователя
        :return: данные созданного пользователя в формате UserReadSchema
        :raises HTTPException: если пользователь с таким email уже существует
        """
        logger.info(f"✍️ Создание пользователя с email={email}")
        existing_user = await self.user_service.get_by_email(email=email)
        if existing_user:
            logger.warning(f"⚠️ Пользователь с email={email} уже существует")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с email={email} уже зарегистрирован"
            )

        user_data = UserCreateSchema(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            role=role
        )
        user = await self.user_service.create(user_data)
        logger.info(f"🎉 Пользователь с email={email} успешно создан")
        return user

    async def update_user(self, user_id: int, request: UserUpdateRequest) -> UserReadSchema:
        """
        Обновить данные пользователя по ID.

        :param user_id: идентификатор пользователя
        :param request: объект запроса на обновление пользователя
        :return: обновленные данные пользователя в формате UserReadSchema
        :raises HTTPException: если пользователь не найден
        """
        logger.info(f"✏️ Обновление пользователя с id={user_id}")
        user = await self.user_service.get_by_id(user_id)
        if user is None:
            logger.warning(f"⚠️ Попытка обновить несуществующего пользователя id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )

        updated_data = UserUpdateSchema.model_validate(request)
        user = await self.user_service.update(user_id, updated_data)
        logger.info(f"✅ Пользователь с id={user_id} успешно обновлен")
        return user

    async def delete_user(self, user_id: int) -> None:
        """
        Удалить пользователя по ID.

        :param user_id: идентификатор пользователя для удаления
        :return: None
        :raises HTTPException: если пользователь не найден
        """
        logger.info(f"🗑️ Удаление пользователя с id={user_id}")
        try:
            await self.user_service.delete(user_id)
            logger.info(f"✅ Пользователь с id={user_id} успешно удален")
        except UserNotFoundError:
            logger.warning(f"⚠️ Попытка удалить несуществующего пользователя id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
