from sqlalchemy import Integer, ForeignKey, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import BaseModel


class AccountModel(BaseModel):
    """
    Модель банковского счета пользователя.

    Атрибуты:
    - id — уникальный идентификатор счета
    - user_id — идентификатор владельца (FK на users.id)
    - balance — баланс счета (точность до 2 знаков)
    """

    __tablename__ = "accounts"
    __table_args__ = (
        Index("ix_accounts_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    balance: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0.0
    )

    # Relationships
    user = relationship("UserModel", back_populates="accounts")
    payments = relationship(
        "PaymentModel",
        back_populates="account",
        cascade="all, delete-orphan"
    )
