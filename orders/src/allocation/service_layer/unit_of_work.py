from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.allocation.adapters.repository import SqlAlchemyOrderRepository, SqlAlchemyTicketRepository, AbstractOrderRepository, AbstractTicketRepository
from config import get_db_uri


class AbstractUnitOfWork(ABC):
    tickets: AbstractTicketRepository
    orders: AbstractOrderRepository

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(
        url=get_db_uri()
    ),
    expire_on_commit=False
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.tickets = SqlAlchemyTicketRepository(self.session)
        self.orders = SqlAlchemyOrderRepository(self.session)

        return await super().__aenter__()
    
    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
