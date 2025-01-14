from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar


@dataclass(slots=True)
class DomainModel:
    id: int | None

    dt_cr: datetime | None
    dt_up: datetime | None
    status: bool


AbstractDomainModel = TypeVar('AbstractDomainModel', bound=DomainModel)
