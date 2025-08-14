from sqlalchemy import select, update, delete, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.models.user_model import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find(self) -> ScalarResult[UserModel]:
        stmt = select(UserModel)
        return await self.session.scalars(stmt)

    async def find_by_email(self, email: str) -> UserModel | None:
        """Получить пользователя по email"""
        stmt = select(UserModel).where(
            UserModel.email == email,
        )

        return await self.session.scalar(stmt)

    async def find_by_id(self, find_id: int) -> UserModel | None:
        print("Hereeeeeeeeeeeee:", find_id)
        stmt = select(UserModel).where(
            UserModel.id == find_id,
        )

        return await self.session.scalar(stmt)
    async def create(self, user: UserModel) -> UserModel:
        """Создать нового пользователя"""
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user_id: int, **fields) -> UserModel:
        print("Fields",fields)
        """
        Обновить пользователя через UPDATE и вернуть обновленный объект.
        Коммит будет на уровне сервиса.
        """
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**fields)
            .returning(UserModel)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NoResultFound(f"User with id={user_id} not found")
        return user

    async def delete_by_id(self, user_id: int) -> None:
        """Удалить пользователя  по id"""
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)
        await self.session.flush()
        # Коммит на уровне сервиса

