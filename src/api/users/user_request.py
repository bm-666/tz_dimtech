from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel

from src.enums.user_role import UserRole


class BaseUserRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
class UserCreateRequest(BaseUserRequest):
    email: EmailStr
    password: str
    role: UserRole
    full_name: str

class UserUpdateRequest(BaseUserRequest):
    email: EmailStr | None = None
    role: UserRole | None = None
    full_name: str | None = None
