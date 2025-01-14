from pydantic import Field

PermCodeField = Field(..., min_length=3, max_length=100, examples=['base:permission:user'], title='Permission Code')
PermCodeOptionalField = Field(
    None, min_length=3, max_length=100, examples=['base:permission:user'], title='Permission Code'
)

PermNameField = Field(..., max_length=150, examples=['Базовое разрешение пользователя'], title='Permission Name')
PermNameOptionalField = Field(
    None, max_length=150, examples=['Базовое разрешение пользователя'], title='Permission Name'
)

PermDescOptionalField = Field(
    None, max_length=200, examples=['Право пользовательского доступа'], title='Permission Description'
)
