from datetime import date, datetime, time

from src.core.schemas import SEvent
from src.core.dao import EventDAO
from src.core.models import Event


async def create_event_handler(event_data: SEvent, event_dao: EventDAO) -> dict:
    is_created = await event_dao.create_event(Event(**event_data.model_dump()))

    return {"message": "Мероприятие успешно создано" if is_created else "Ошибка при создании мероприятия"}


async def update_event_handler(event_id: int, event_data: SEvent, event_dao: EventDAO) -> dict:
    is_updated = await event_dao.update_event(event_id, event_data.model_dump())

    return {"message": "Мероприятие успешно обновлено" if is_updated else "Ошибка при обновлении мероприятия"}


async def delete_event_handler(event_id: int, event_dao: EventDAO) -> dict:
    is_delete = await event_dao.delete_event(event_id)

    return {"message": "Мероприятие успешно удалено" if is_delete else "Ошибка при удалении мероприятия"}


async def find_event_by_id(event_id: int, event_dao: EventDAO) -> SEvent | dict:
    event = await event_dao.find_event_by_id(event_id)

    if event:
        return SEvent(
            name=event.name,
            description=event.description,
            event_date=event.event_date,
            available_tickets=event.available_tickets,
            ticket_price=event.ticket_price
        )

    return {"message": 'Данное мероприятие не найдено'}


async def find_event_by_date(date_from: date, date_to: date, page: int, items_count: int, event_dao: EventDAO):
    datetime.combine(date_from, time.min)
    datetime.combine(date_to, time.max)

    events = await event_dao.find_event_by_date(date_from, date_to, page, items_count)

    event_dicts = [event.to_dict() for event in events]

    return event_dicts