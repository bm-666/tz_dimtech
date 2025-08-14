from datetime import datetime, UTC

from sqlalchemy import text, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        default=lambda: datetime.now(UTC),  # Aware datetime по умолчанию
        nullable=False,
    )


