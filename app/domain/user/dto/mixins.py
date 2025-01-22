from datetime import datetime

from pydantic import BaseModel

from .fields import LastLoginOptionalField


class LastLoginMixin(BaseModel):
    last_login: datetime | None = LastLoginOptionalField
