from sqlalchemy import String, Enum, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import BaseModel
from src.enums.user_role import UserRole
from src.models.account_model import AccountModel
from src.models.payment_model import PaymentModel



class UserModel(BaseModel):
    """
    Модель пользователя системы.

    Содержит:
    - уникальный email
    - захэшированный пароль
    - полное имя
    - роль (пользователь или администратор)
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_role", "role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)

    # Relationships
    accounts: Mapped[list["AccountModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    payments: Mapped[list["PaymentModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


