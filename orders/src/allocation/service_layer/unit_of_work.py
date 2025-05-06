from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.allocation.adapters.repository import SqlAlchemyOrderRepository, SqlAlchemyTicketRepository, AbstractOrderRepository, AbstractTicketRepository
from config import get_db_uri


class AbstractUnitOfWork(ABC):
    tickets: AbstractTicketRepository
    orders: AbstractOrderRepository

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self
    
    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(
        url=get_db_uri()
    ),
    expire_on_commit=False
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.tickets = SqlAlchemyTicketRepository(self.session)
        self.orders = SqlAlchemyOrderRepository(self.session)

        return await super().__aenter__()
    
    async def __aexit__(self, *args: Any) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
