from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.allocation.domain.model import OrderStatus
from src.allocation.adapters.orm import Order, Ticket


class AbstractOrderRepository(ABC):    
    @abstractmethod
    async def get(self, **filters: int | OrderStatus) -> Order| None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_cart(self, **filters: int | OrderStatus) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def create_cart(self, order_orm: Order) -> Order:
        raise NotImplementedError
    

class SqlAlchemyOrderRepository(AbstractOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: int | OrderStatus) -> Order | None:
        result = await self.session.execute(select(Order).filter_by(**filters))
        return result.scalar_one_or_none()
    
    async def delete_cart(self, **filters: int | OrderStatus) -> bool:
        stmt = delete(Order).filter_by(**filters)
        result = await self.session.execute(stmt)

        return result.rowcount > 0
    
    async def create_cart(self, order_orm: Order) -> Order:
        self.session.add(order_orm)

        return order_orm
    
    

class AbstractTicketRepository(ABC):
    @abstractmethod
    async def add_all(self, tickets_data: list[dict]) -> list[Ticket]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, order_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_tickets_by_filter(self, **filters: int | OrderStatus) -> Sequence[Ticket]:
        raise NotImplementedError


class SqlAlchemyTicketRepository(AbstractTicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_all(self, tickets_data: list[dict]) -> list[Ticket]:
        tickets_orm = [Ticket(**ticket_data) for ticket_data in tickets_data]

        self.session.add_all(tickets_orm)
        await self.session.flush()

        return tickets_orm
    
    async def delete(self, order_id: int) -> None:
        stmt = delete(Ticket).filter_by(order_id=order_id)
        await self.session.execute(stmt)
    
    async def get_tickets_by_filter(self, **filters: int | OrderStatus) -> Sequence[Ticket]:
        stmt = select(Ticket).join(Order).filter_by(**filters).options(joinedload(Ticket.order))
        result = await self.session.execute(stmt)

        return result.scalars().all()