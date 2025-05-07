from fastapi import APIRouter, Request

from src.allocation.service_layer import handlers
from src.allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.allocation.domain.commands import UpdateCartRequest


router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('')
async def create_cart(request: Request) -> list[dict]:
    user_id = request.headers.get('User-ID')

    return await handlers.add(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.put('')
async def update_cart(request: Request, tickets: UpdateCartRequest) -> dict:
    user_id = request.headers.get('User-ID')
    
    return await handlers.update(cmd=tickets, user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.delete('')
async def delete_cart(request: Request) -> dict:
    user_id = request.headers.get('User-ID')

    return await handlers.delete(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('/current')
async def get_current_cart(request: Request) -> dict:
    user_id = request.headers.get('User-ID')

    return await handlers.get_current_cart(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('')
async def get_orders(request: Request) -> dict:
    user_id = request.headers.get('User-ID')

    return await handlers.get_orders(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('/{id}')
async def get_order_by_id(request: Request, id: int) -> dict:
    user_id = request.headers.get('User-ID')

    return await handlers.get_order_by_id(user_id=user_id, order_id=id, uow=SqlAlchemyUnitOfWork())