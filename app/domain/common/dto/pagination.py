from typing import Generic, TypeVar

from .base import DTO
from .helper import RecordsField, SkipField

Item = TypeVar('Item')


class PaginatedItemsDTO(DTO, Generic[Item]):
    skip: int = SkipField
    records: int = RecordsField
    results: list[Item]
