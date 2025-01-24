from pydantic import BaseModel, Field


class BaseErrorResponse(BaseModel):
    error: str = Field(..., examples=['ErrorName'])
    message: str | None = Field(None, examples=['Error message'])
    detail: dict | None = Field(None, examples=[{'key': 'value'}])


class BaseResultResponse(BaseModel):
    result: str = Field(..., examples=['Successful'])
    message: str | None = Field(None, examples=['Operation completed'])
    detail: dict | None = Field(None, examples=[{'key': 'value'}])


class DeleteResultSuccess(BaseResultResponse):
    result: str = Field('DeleteSuccessful')
    message: str = Field('Запись успешно удалена')
