from pydantic import BaseModel, EmailStr, ConfigDict
from src.enums.user_role import UserRole

class UserAuthSchema(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
