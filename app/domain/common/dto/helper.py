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

