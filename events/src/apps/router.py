from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from src.core.dao import EventDAO
from src.core.handlers import (
    create_event_handler,
    delete_event_handler,
    find_event_by_date,
    find_event_by_id,
    update_event_handler,
)
from src.core.schemas import SEvent


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("")
async def create_event(event_data: SEvent, request: Request, event_dao: Annotated[EventDAO, Depends(EventDAO)]) -> dict:
    return await create_event_handler(event_data, event_dao)


@router.put("/{id}")
async def update_event(id: int, request: Request, event_data: SEvent, event_dao: Annotated[EventDAO, Depends(EventDAO)]) -> dict:
    return await update_event_handler(id, event_data, event_dao)


@router.delete("/{id}")
async def delete_event_by_id(id: int, request: Request, event_dao: Annotated[EventDAO, Depends(EventDAO)]) -> dict:
    return await delete_event_handler(id, event_dao)



@router.get("/{id}")
async def get_event_by_id(id: int, event_dao: Annotated[EventDAO, Depends(EventDAO)]) -> SEvent | dict:
    return await find_event_by_id(id, event_dao)


@router.get("")
async def get_event(
    event_dao: Annotated[EventDAO, Depends(EventDAO)],
    date_from: date = Query(...),
    date_to: date = Query(...),
    page: int = Query(0, ge=0),
    items_count: int = Query(20, ge=20, le=100)
):
    return await find_event_by_date(date_from, date_to, page, items_count, event_dao)
