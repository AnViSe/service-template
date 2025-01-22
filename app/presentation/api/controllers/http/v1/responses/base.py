from pydantic import BaseModel, Field


class BaseResultResponse(BaseModel):
    result: str = Field(..., examples=['Successful'])
    message: str | None = Field(None, examples=['Operation completed'])
    detail: dict | None = Field(None, examples=[{'key': 'value'}])


class DeleteResultSuccess(BaseResultResponse):
    result: str = Field('DeleteSuccessful')
    message: str = Field('Запись успешно удалена')
