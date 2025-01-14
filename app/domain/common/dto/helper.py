from pydantic import Field

IdField = Field(..., gt=0, examples=[1], title='Код записи')
IdWithZeroField = Field(..., ge=0, examples=[0], title='Код записи')

ParentIdOptionalField = Field(None, ge=0, examples=[0], title='Код родителя')

SortField = Field(999, ge=0, le=999, examples=[999], title='Сортировка')
SortOptionalField = Field(None, ge=0, le=999, examples=[999], title='Сортировка')

DtCrField = Field(..., title='Создана')
DtUpField = Field(None, title='Изменена')

StatusField = Field(True, examples=['true'], title='Статус')
StatusOptionalField = Field(None, examples=['true'], title='Статус')

SkipField = Field(0, examples=[0], title='Пропустить')
RecordsField = Field(0, examples=[0], title='Всего записей')
ResultsField = Field(None, title='Данные')

ItemsField = Field([], title='Список значений')
ItemsOptionalField = Field(None, title='Список значений')

# SDNameField = Field(..., max_length=100, examples=['РУП "Белпочта"'], title='Наименование подразделения')
# SDNameOptionalField = Field(None, max_length=100, examples=['РУП "Белпочта"'], title='Наименование подразделения')
# SDNameFullField = Field(
#     None, max_length=255, examples=['Республиканское унитарное предприятие "Белпочта"'],
#     title='Полное наименование подразделения'
# )

# POZipcodeField = Field(..., ge=200000, lt=300000, examples=[220010], title='Индекс отделения связи')
# POZipcodeOptionalField = Field(None, ge=200000, lt=300000, examples=[220010], title='Индекс отделения связи')

# LabelField = Field(..., max_length=100, examples=['РУП Белпочта'], title='Наименование')
# LastLoginOptionalField = Field(None, title='Последний вход')

# CredentialCodeField = Field(..., min_length=3, max_length=100, examples=['base:permission:user'])
