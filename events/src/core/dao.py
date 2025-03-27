from datetime import date

from fastapi import Depends

from sqlalchemy import update, delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.core.database import Base, async_session
from src.core.models import Event
from src.core.schemas import SEvent


class EventDAO(Base):
    def __init__(self, session: AsyncSession = Depends(async_session)):
        self.session = session

    async def create_event(self, event_data: Event) -> Event | None:
        try:
            self.session.add(event_data)
            await self.session.commit()

            return event_data
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка добавления мероприятия: {e}")

            return None
        
        
    async def update_event(self, event_id: int, event_data: dict) -> Event | None:
        try:
            stmt = (
                update(Event)
                .where(Event.id == event_id)
                .values(**event_data)
                .returning(Event)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result.fetchone()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка обновления мероприятия: {e}")

            return None


    async def delete_event(self, event_id: int) -> Event | None:
        try:
            stmt = delete(Event).where(Event.id == event_id).returning(Event)
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f'Ошибка при удалении мероприятия: ', {e})

            return None


    async def find_event_by_id(self, event_id: int) -> Event | None:
        stmt = select(Event).where(Event.id == event_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    

    async def find_event_by_date(self, date_from: date, date_to: date, page: int, items_count: int):
        stmt = (
            select(Event)
            .where(and_(Event.event_date >= date_from, Event.event_date <= date_to))
            .offset((page - 1) * items_count)
            .limit(items_count)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

