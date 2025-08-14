import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


# ------------------- Base ------------------- #
class PaymentBaseSchema(BaseModel):
    account_id: int
    user_id: int
    amount: float
    transaction_id: uuid.UUID

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )


# ------------------- Create Request ------------------- #
class PaymentCreateSchema(PaymentBaseSchema): ...


# ------------------- Read Schema ------------------- #
class PaymentReadSchema(PaymentBaseSchema):
    id: int
    created_at: datetime


# ------------------- Update Schema ------------------- #
class PaymentUpdateSchema(BaseModel):
    amount: float | None = Field(None, gt=0)
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )
