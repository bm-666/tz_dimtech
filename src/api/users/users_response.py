from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

from src.enums.user_role import UserRole


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    full_name: str
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
