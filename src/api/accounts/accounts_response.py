from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AccountResponseSchema(BaseModel):
    id: int
    user_id: int
    balance: float
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

class AccountsResponseSchema(BaseModel):
    accounts: list[AccountResponseSchema]