from pydantic import Field

UserNameField = Field(..., max_length=100, examples=['User'], title='Имя пользователя')
UserNameOptionalField = Field(None, max_length=100, examples=['User'], title='Имя пользователя')

SubdivisionIdOptionalField = Field(None, gt=0, examples=[1], title='Код подразделения пользователя')
SubdivisionNameOptionalField = Field(None, examples=['РУП "Белпочта"'], title='Наименование подразделения пользователя')

UserMailOptionalField = Field(None, examples=['user@example.org'], title='E-Mail пользователя')

UserPassField = Field(..., max_length=100, examples=['password'], title='Пароль')
UserPassOptionalField = Field(None, max_length=100, examples=['password'], title='Пароль')
UserPassOldField = Field(..., max_length=100, examples=['password'], title='Старый пароль')
UserPassNewField = Field(..., max_length=100, examples=['password'], title='Новый пароль')

UserDescOptionalField = Field(None, max_length=150, examples=['Good user'], title='Описание пользователя')

UserAvatarOptionalField = Field(None, max_length=100, examples=['avatar.png'], title='Аватар пользователя')

LastLoginOptionalField = Field(None, title='Последний вход')
