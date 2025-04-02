from src.core.models import AbstractRmqSender


TICKET_PRICE_CHANGE = "ticket_price_changed"
TICKET_DELETE_NOT_STARTED = "ticket_delete_not_started"
TICKET_AVAILABLE_CHANGE = "ticket_available_change"


def admin_change_ticket_price(event_id: int, new_price: int, rmq_sender: AbstractRmqSender):
    rmq_sender.send_event(
        event_name=TICKET_PRICE_CHANGE,
        payload={"event_id": str(event_id), "new_price": new_price}
    )


def admin_delete_not_started_event(event_id: int, ticket_price: int, rmq_sender: AbstractRmqSender):
    rmq_sender.send_event(
        event_name=TICKET_DELETE_NOT_STARTED,
        payload={"event_id": str(event_id), "ticket_price": ticket_price}
    )


def admin_change_available_ticket(event_id: int, available_ticket: int, rmq_sender: AbstractRmqSender):
    rmq_sender.send_event(
        event_name=TICKET_AVAILABLE_CHANGE,
        payload={"event_id": event_id, "available_ticket": available_ticket}
    )



