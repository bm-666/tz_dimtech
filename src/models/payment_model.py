import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Numeric, String, Index
from src.models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class PaymentModel(BaseModel):
    """
    Модель платежа.

    Хранит данные о транзакции пополнения баланса:
    - уникальный UUID транзакции
    - сумму
    - связь с пользователем и счётом
    """

    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payments_user_id", "user_id"),
        Index("ix_payments_account_id", "account_id"),
        Index("ix_payments_user_account", "user_id", "account_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    user = relationship("UserModel", back_populates="payments")
    account = relationship("AccountModel", back_populates="payments")
