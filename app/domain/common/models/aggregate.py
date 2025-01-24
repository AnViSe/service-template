import logging
from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from app.domain.common.models.entity import Entity

logger = logging.getLogger('aggregate')

@dataclass
class Aggregate(Entity, ABC):
    id: int | None
    dt_cr: datetime | None
    dt_up: datetime | None
    status: bool

    # events: list[str] = field(default_factory=list, init=False, repr=False, compare=False, hash=False)

    def to_dict(self, exclude: set[str] | None = None) -> dict:
        result = self.__dict__
        items = exclude.union(['dt_cr', 'dt_up'])
        for item in items:
            result.pop(item, None)
        return result
