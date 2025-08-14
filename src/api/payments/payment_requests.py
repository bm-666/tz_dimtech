from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class PaymentCreateRequest(BaseModel):
    account_id: int
    user_id: int
    amount: float
    transaction_id: str
    signature: str

    model_config = ConfigDict(from_attributes=True, populate_by_name = True, alias_generator = to_camel)