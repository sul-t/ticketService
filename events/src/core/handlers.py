from datetime import date, datetime, time

from src.core.dao import EventDAO
from src.core.models import Event, RmqAdapter
from src.core.producer import admin_change_available_ticket, admin_change_ticket_price, admin_delete_not_started_event
from src.core.schemas import SEvent


async def create_event_handler(event_data: SEvent, event_dao: EventDAO) -> dict:
    is_created = await event_dao.create_event(Event(**event_data.model_dump()))

    return {"message": "Мероприятие успешно создано" if is_created else "Ошибка при создании мероприятия"}


async def update_event_handler(event_id: int, event_data: SEvent, event_dao: EventDAO) -> dict:
    event = await event_dao.find_event_by_id(event_id=event_id)
    old_event_data = {"available_tickets": event.available_tickets, "ticket_price": event.ticket_price}

    event = await event_dao.update_event(event_id, event_data.model_dump())

    if event is None:
        return {"message": "Ошибка при обновлении мероприятия"}


    rmq_sender = RmqAdapter(queue="events_to_orders")

    if old_event_data["available_tickets"] > event.available_tickets:
        admin_change_available_ticket(event_id=event_id, available_ticket=event.available_tickets, rmq_sender=rmq_sender)

    if old_event_data["ticket_price"] != event.ticket_price:
        admin_change_ticket_price(event_id=event_id, new_price=event_data.ticket_price, rmq_sender=rmq_sender)

    return {"message": "Мероприятие успешно обновлено"}



async def delete_event_handler(event_id: int, event_dao: EventDAO) -> dict:
    is_delete = await event_dao.delete_event(event_id)

    if not is_delete:
        return {"message": "Ошибка при удалении мероприятия"}
    elif is_delete.event_date <= datetime.now(tz=None):
        return {"message": "Мероприятие успешно удалено"}
    else:
        admin_delete_not_started_event(event_id=event_id, ticket_price=is_delete.ticket_price, rmq_sender=RmqAdapter(queue="events_to_orders"))

        return {"message": "Мероприятие успешно удалено и деньги возвращены"}






async def find_event_by_id(event_id: int, event_dao: EventDAO) -> SEvent | dict:
    event = await event_dao.find_event_by_id(event_id)

    if event:
        return SEvent(
            name=event.name,
            description=event.description,
            event_date=event.event_date,
            available_tickets=event.available_tickets,
            ticket_price=event.ticket_price,
        )

    return {"message": "Данное мероприятие не найдено"}


async def find_event_by_date(date_from: date, date_to: date, page: int, items_count: int, event_dao: EventDAO):
    datetime.combine(date_from, time.min)
    datetime.combine(date_to, time.max)

    events = await event_dao.find_event_by_date(date_from, date_to, page, items_count)

    event_dicts = [event.to_dict() for event in events]

    return event_dicts
