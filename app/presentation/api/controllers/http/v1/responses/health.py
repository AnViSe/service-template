from pydantic import BaseModel


class Status(BaseModel):
    name: str = 'Service name: version'
    status: bool | str | float | None


class HealthStatus(BaseModel):
    statuses: list[Status]
    errors: list[str] | None
