from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.types import Integer

from config import get_db_uri


engine = create_async_engine(get_db_uri())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f'{self.__name__.lower()}s'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    