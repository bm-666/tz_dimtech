from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseAccountSchema(BaseModel):
    user_id: int
    balance: float
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

class AccountReadSchema(BaseAccountSchema):
    id: int


class AccountCreateSchema(BaseAccountSchema):
    id: int | None

class UpdateAccountSchema(BaseModel): ...