from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        frozen=True,
        from_attributes=True
    )
