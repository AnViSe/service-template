from pydantic import BaseModel, Field


class BaseResultResponse(BaseModel):
    result: str = Field(..., examples=['Successful'])
    message: str | None = Field(None, examples=['Operation completed'])
    detail: dict | None = Field(None, examples=[{'key': 'value'}])


class DeleteResultSuccess(BaseResultResponse):
    result: str = Field('DeleteSuccessful')
    message: str = Field('Запись успешно удалена')


class EmailSent(BaseResultResponse):
    result: str = Field('EmailSent')
    message: str = Field('Сообщение отправлено на электронную почту.')


class ResetPasswordEmailSent(BaseResultResponse):
    result: str = Field('ResetPasswordEmailSent')
    message: str = Field('Сообщение с инструкцией по восстановлению пароля отправлено на электронную почту.')


class UpdatePasswordSuccess(BaseResultResponse):
    result: str = Field('UpdatePasswordSuccess')
    message: str = Field('Пароль успешно изменен.')
