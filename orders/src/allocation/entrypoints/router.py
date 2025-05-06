from fastapi import APIRouter

from src.allocation.service_layer.handlers import add, update, delete
from src.allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.allocation.domain.commands import UpdateCartRequest


router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('')
async def create_cart(user_id: int):
    return await add(user_id=user_id, uow=SqlAlchemyUnitOfWork())


@router.put('')
async def update_cart(request: UpdateCartRequest):
    return await update(cmd=request, uow=SqlAlchemyUnitOfWork())


@router.delete('')
async def delete_cart(user_id: int):
    return await delete(user_id=user_id, uow=SqlAlchemyUnitOfWork())