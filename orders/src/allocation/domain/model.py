from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    REFUND = "refund"
    PARTIAL_REFUND = "partial_refund"
    DONE = 'done'


class TicketModel:
    def __init__(self, event_id: int, order_id: int, price: int):
        self.event_id = event_id
        self.order_id = order_id
        self.price = price


class OrderModel:
    def __init__(self, status: OrderStatus, user_id: int, tickets: list[TicketModel]):
        self.status = status
        self.user_id = user_id
        self.tickets = tickets
    