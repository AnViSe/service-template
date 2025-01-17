from fastapi import Query
from pydantic import BaseModel, Field, Json

SkipQuery = Query(0, dt=0, description='Пропустить строк')
LimitQuery = Query(100, gt=0, le=1000, description='Количество строк')
# PageQuery = Query(None, gt=0, description='Номер страницы'),
SearchQuery = Query(None, description='Поиск (фильтрация) данных')
SortQuery = Query(None, description='Очередность сортировки')
FilterQuery = Query(None, description='Фильтр данных')

# CodeQuery: str | None = Query(None, description='Тип данных')


class QueryParams(BaseModel):
    skip: int = Field(SkipQuery)
    limit: int = Field(LimitQuery)
    search: str | None = Field(SearchQuery)
    sort: str | None = Field(SortQuery)
    filter: Json | None = Field(FilterQuery)
