from pydantic import Field

RoleCodeField = Field(..., min_length=3, max_length=100, examples=['base:role:user'])
RoleCodeOptionalField = Field(None, min_length=3, max_length=100, examples=['base:role:user'])

RoleNameField = Field(..., max_length=150, examples=['Роль пользователя'])
RoleNameOptionalField = Field(None, max_length=150, examples=['Роль пользователя'])

RoleDescOptionalField = Field(None, max_length=200, examples=['Доступ к системе'])
