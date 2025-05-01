from fastapi import APIRouter

from src.allocation.service_layer import handlers
from src.allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.allocation.domain.commands import UpdateCartRequest


router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('')
async def create_cart(user_id: int) -> list[dict]:
    return await handlers.add(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.put('')
async def update_cart(request: UpdateCartRequest) -> dict:
    return await handlers.update(cmd=request, uow=SqlAlchemyUnitOfWork())


@router.delete('')
async def delete_cart(user_id: int) -> dict:
    return await handlers.delete(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('/current')
async def get_current_cart(user_id: int) -> dict:
    return await handlers.get_current_cart(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('')
async def get_orders(user_id: int) -> dict:
    return await handlers.get_orders(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.get('/{id}')
async def get_order_by_id(user_id: int, id: int) -> dict:
    return await handlers.get_order_by_id(user_id=user_id, order_id=id, uow=SqlAlchemyUnitOfWork())