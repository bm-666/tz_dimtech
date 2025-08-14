from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

from src.enums.user_role import UserRole

class UserBaseSchema(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

class UserCreateSchema(UserBaseSchema):
    hashed_password: str

class UserReadSchema(UserBaseSchema):
    id: int

class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRole | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )