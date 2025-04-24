from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr, relationship
from sqlalchemy.types import Integer
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.allocation.domain.model import OrderStatus, OrderModel, TicketModel


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f'{self.__name__.lower()}s'


class Order(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    user_id: Mapped[int]

class Ticket(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    price: Mapped[int]

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "order_id": self.order_id,
            "price": self.price
        }


def convert_order_to_orm(order: OrderModel) -> Order:
    return Order(
        order_status = order.status,
        user_id = order.user_id
    )

def convert_orm_to_order(order_orm: Order, tickets: TicketModel) -> OrderModel:
    return OrderModel(
        id = order_orm.id,
        status = order_orm.order_status,
        user_id = order_orm.user_id,
        ticket_model = tickets
    )


def convert_ticket_to_orm(ticket: TicketModel) -> Ticket:
    return Ticket(
        event_id = ticket.event_id,
        order_id = ticket.order_id,
        price = ticket.price
    )

def convert_orm_to_ticket(ticket_orm: Ticket) -> TicketModel:
    return TicketModel(
        event_id = ticket_orm.event_id,
        order_id = ticket_orm.order_id,
        price = ticket_orm.price
    )

def convert_to_dict_cart(order, tickets) -> dict:
    return {
        "id": order.id,
        "status": order.order_status,
        "user_id": order.user_id,
        "tickets": [{
                "id": t.id,
                "event_id": t.event_id, 
                "order_id": t.order_id,
                "price": t.price
            }
            for t in tickets
        ]
    }