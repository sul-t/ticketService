from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator


class SEvent(BaseModel):
    name: str = Field(..., description="Название")
    description: str = Field(..., description="Описание")
    event_date: datetime = Field(..., description="Дата проведения")
    available_tickets: int = Field(..., gt=0, description="Доступное количество билетов")
    ticket_price: int = Field(..., ge=0, description="Стоимость билета")

    @field_validator("event_date")
    @classmethod
    def validate_event_date(cls, value):
        value = value.replace(tzinfo=None)
        if not value or value <= datetime.now(UTC).replace(tzinfo=None):
            raise ValueError("Дата проведения мероприятия не должна быть позднее текущего времени!")

        return value
