from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

from src.enums.user_role import UserRole


class BasePasswordField(BaseModel):
    password: str

class BaseAuthRequest(BasePasswordField):
    email: EmailStr
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

class AuthLoginRequest(BaseAuthRequest): ...

class RegisterUserRequest(BaseAuthRequest):
    role: UserRole
    full_name: str
