from abc import ABC, abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.allocation.domain.model import OrderModel, TicketModel
from src.allocation.adapters.orm import convert_order_to_orm, Order, Ticket


class AbstractOrderRepository(ABC):
    @abstractmethod
    async def add(self, order: OrderModel):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, user_id: int) -> OrderModel:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, user_id: int):
        raise NotImplementedError
    

class SqlAlchemyOrderRepository(AbstractOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: OrderModel): 
        order_orm = convert_order_to_orm(order)
        self.session.add(order_orm)
        await self.session.flush()

        return order_orm

    async def get(self, user_id: int) -> OrderModel:
        result = await self.session.execute(select(Order).filter_by(user_id=user_id))
        return result.scalar_one_or_none()
    
    async def delete(self, user_id):
        stmt = delete(Order).filter_by(user_id=user_id).returning(Order.id)
        return await self.session.execute(stmt)



class AbstractTicketRepository(ABC):
    @abstractmethod
    async def add_all(self, tickets_data: list[dict]):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, order_id: int) -> list[TicketModel]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, order_id: int):
        raise NotImplementedError


class SqlAlchemyTicketRepository(AbstractTicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_all(self, tickets_data: list[dict]):
        tickets_orm = [Ticket(**ticket_data) for ticket_data in tickets_data]

        self.session.add_all(tickets_orm)
        await self.session.flush()

        return tickets_orm
    
    async def get(self, order_id):
        result = await self.session.execute(select(Ticket).filter_by(order_id=order_id))

        return result.scalars().all()
    
    async def delete(self, order_id):
        stmt = delete(Ticket).filter_by(order_id=order_id)
        return await self.session.execute(stmt)
    