from pydantic import BaseModel
from pydantic_core.core_schema import model_field
from sqlalchemy.testing.schema import mapped_column


def get_concatenate_values(model: BaseModel) -> str:
    dict_fields = model.model_dump()
    sorted_fields = sorted(dict_fields.items())

    return "".join(str(value) for _, value in sorted_fields)