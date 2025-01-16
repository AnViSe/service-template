from typing import TypeVar

from app.domain.common.models.aggregate import Aggregate

AbstractDomainModel = TypeVar('AbstractDomainModel', bound=Aggregate)
