from datetime import date, datetime
import logging
from typing import Sequence

from fastapi import Depends
from sqlalchemy import and_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base, async_session
from src.core.models import Event


log = logging.getLogger(__name__)


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
            log.error(f"Ошибка при создании мероприятия: {e}")

            return None


    async def update_event(self, event_id: int, event_data: dict) -> Event | None:
        try:
            stmt = update(Event).where(Event.id == event_id).values(**event_data).returning(Event)
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка обновления мероприятия: {e}")

            return None


    async def delete_event(self, event_id: int, delete_date: datetime) -> Event | None:
        try:
            stmt = update(Event).where(Event.id == event_id).values(delete_at = delete_date).returning(Event)
            # stmt = delete(Event).where(Event.id == event_id).returning(Event)
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print("Ошибка при удалении мероприятия: ", {e})

            return None


    async def find_event_by_id(self, event_id: int) -> Event | None:
        stmt = select(Event).where(Event.id == event_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def find_event_by_date(self, date_from: date, date_to: date, page: int, items_count: int) -> Sequence[Event]:
        stmt = (
            select(Event)
            .where(and_(Event.event_date > date_from, Event.event_date <= date_to, Event.available_tickets > 0, Event.delete_at.is_(None)))
            .offset((page) * items_count)
            .limit(items_count)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
