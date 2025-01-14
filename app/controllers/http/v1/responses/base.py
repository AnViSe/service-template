from pydantic import BaseModel, Field


class BaseResultResponse(BaseModel):
    result: str = Field(..., examples=['Successful'])
    message: str | None = Field(None, examples=['Operation completed'])
    info: dict | None = Field(None, examples=[{'key': 'value'}])


class DeleteResultSuccess(BaseResultResponse):
    result: str = 'DeleteSuccessful'
    message: str = 'Запись успешно удалена'
    info: dict = {'id': 1}


class EmailSent(BaseResultResponse):
    result: str = Field('EmailSent')
    message: str = Field('Сообщение на электронную почту отправлено.')
    info: dict = Field({'email': 'email@example.com'})


class ResetPasswordEmailSent(BaseResultResponse):
    result: str = Field('ResetPasswordEmailSent')
    message: str = Field('Сообщение с инструкцией по восстановлению пароля отправлено на электронную почту.')
    info: dict = Field({'email': 'email@example.com'})


class UpdatePasswordSuccess(BaseResultResponse):
    result: str = Field('UpdatePasswordSuccess')
    message: str = Field('Пароль успешно изменен.')
    info: dict = Field({'username': 'User'})
