from src.allocation.service_layer.unit_of_work import AbstractUnitOfWork
from src.allocation.domain.model import OrderModel, OrderStatus
from src.allocation.domain.commands import UpdateCartRequest
from src.allocation.adapters.orm import serialize_order_data, convert_order_to_orm


async def add(user_id: int, uow: AbstractUnitOfWork) -> list[dict]:
    async with uow:
        tickets = await uow.tickets.get_tickets_by_filter(user_id=user_id, order_status=OrderStatus.CREATED)
        if not tickets:
            order = OrderModel(status=OrderStatus.CREATED, user_id=user_id, tickets=[])
    
            await uow.orders.create_cart(convert_order_to_orm(order))
            await uow.commit()

        tickets_dict = [ticket.to_dict() for ticket in tickets]

        return tickets_dict
    

async def update(cmd: UpdateCartRequest, uow: AbstractUnitOfWork) -> dict:
    async with uow:
        order_orm = await uow.orders.get(user_id=cmd.user_id, order_status=OrderStatus.CREATED)
        if order_orm is None:
            return {'ok': False, 'data': 'Корзины не существует'}

        await uow.tickets.delete(order_id=order_orm.id)

        if not cmd.tickets:
            return {'ok': True, 'data': 'Корзина очищена'}

        tickets_data = [{
            "event_id": t.event_id,
            "order_id": order_orm.id,
            "price": t.price
        } for t in cmd.tickets]

        await uow.tickets.add_all(tickets_data)
        await uow.commit()

        return {'ok': True, 'data': 'Данные успешно обновлены'}
    

async def delete(user_id: int, uow: AbstractUnitOfWork) -> dict:
    async with uow:
        cart = await uow.orders.delete_cart(user_id=user_id, order_status=OrderStatus.CREATED)
        if not cart:
            return {'ok': False, 'data': 'У пользователя нет корзины'}
        
        await uow.commit()

        return {'ok': True, 'data': 'Корзина была полностью очищена'}


async def get_current_cart(user_id: int, uow: AbstractUnitOfWork) -> dict:
    async with uow:
        try:
            carts = await uow.tickets.get_tickets_by_filter(user_id=user_id, order_status=OrderStatus.CREATED)
            if not carts:
                return {'ok': False, 'data': 'У пользователя нет корзины'}
            
            return serialize_order_data(carts)
        except Exception as e:
            print(e)

            return {'ok': False, 'data': 'Ошибка при получении корзины пользователя'}
        

async def get_orders(user_id: int, uow: AbstractUnitOfWork) -> dict:
    async with uow:
        try:
            tickets = await uow.tickets.get_tickets_by_filter(user_id=user_id, order_status=OrderStatus.DONE)
            if not tickets:
                return {'ok': False, 'data': 'У пользователя нет завершенных заказов'}
            
            return serialize_order_data(tickets)
        except Exception as e:
            print(e)

            return {'ok': False, 'data': 'Ошибка при получении завершенных заказов пользователя'}


async def get_order_by_id(user_id: int, order_id: int, uow: AbstractUnitOfWork) -> dict:
    async with uow:
        tickets = await uow.tickets.get_tickets_by_filter(user_id=user_id, id=order_id, order_status=OrderStatus.DONE)
        if not tickets:
            return {'ok': False, 'data': 'У пользователя нет завершенных заказов по данному id'}

        return serialize_order_data(tickets)
        
