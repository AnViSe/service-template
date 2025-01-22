from pydantic import Field

DtAcOptionalField = Field(None, title='Активирована')
VerificationCodeOptionalField = Field(None, max_length=100, examples=['SuperVerifyString'], title='Код верификации')
