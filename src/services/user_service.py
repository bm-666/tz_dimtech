from src.schemas.auth_schemas import UserAuthSchema
from src.models.user_model import UserModel
from src.repositories.user_repositories import UserRepository
from src.schemas.user_shemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserReadSchema
)
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)

    async def get(self) ->list[UserReadSchema]:
        accounts = await self.user_repository.find()
        return [
            UserReadSchema.model_validate(account)
            for account in accounts
        ]

    async def create(self, user: UserCreateSchema) -> UserReadSchema:
        _user = UserModel(**user.model_dump())
        _user = await self.user_repository.create(_user)
        await self.session.commit()
        return UserReadSchema.model_validate(_user)

    async def get_by_email(self, email: str) -> UserReadSchema | None:
        user = await self.user_repository.find_by_email(email)
        if user is None:
            return None
        return UserReadSchema.model_validate(user)
    async def get_by_id(self, user_id: int) -> UserReadSchema | None:
        user = await self.user_repository.find_by_id(user_id)
        return UserReadSchema.model_validate(user) if user else None

    async def get_user_with_password(self, email: str) -> UserAuthSchema:
        user = await self.user_repository.find_by_email(email)
        return UserAuthSchema.model_validate(user) if user else None

    async def update(self, user_id: int, user: UserUpdateSchema) -> UserReadSchema:

        update_data = {
            k: v for k, v in user.model_dump(exclude_unset=True).items()
            if v is not None
        }
        user = await self.user_repository.update(user_id=user_id, **update_data)
        await self.session.commit()
        return UserReadSchema.model_validate(user)

    async def delete(self, user_id: int) -> None:
        await self.user_repository.delete_by_id(user_id)
        await self.session.commit()
