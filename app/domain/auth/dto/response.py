from pydantic import BaseModel, Field


class AuthResultResponse(BaseModel):
    result: str = Field(..., examples=['Successful'])
    message: str | None = Field(None, examples=['Operation completed'])
    info: dict | None = Field(None, examples=[{'key': 'value'}])


class UpdatePasswordSuccess(AuthResultResponse):
    result: str = Field('UpdatePasswordSuccess')
    message: str = Field('Пароль успешно изменен.')


class EmailSent(AuthResultResponse):
    result: str = Field('EmailSent')
    message: str = Field('Сообщение отправлено на электронную почту.')


class ResetPasswordEmailSent(AuthResultResponse):
    result: str = Field('ResetPasswordEmailSent')
    message: str = Field('Сообщение с инструкцией по восстановлению пароля отправлено на электронную почту.')
