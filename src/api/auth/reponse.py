from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AuthLoginResponse(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    token_type: str
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

class AuthTokensSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

