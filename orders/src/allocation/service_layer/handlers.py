from src.allocation.service_layer.unit_of_work import AbstractUnitOfWork
from src.allocation.domain.model import TicketModel, OrderModel, OrderStatus
from src.allocation.domain.commands import UpdateCartRequest
from src.allocation.adapters.orm import convert_to_dict_cart


async def add(user_id: int, uow: AbstractUnitOfWork):
    async with uow:
        order = await uow.orders.get(user_id)
        if order is None:
            order = OrderModel(status=OrderStatus.CREATED, user_id=user_id)
            order = await uow.orders.add(order)

            await uow.commit()

        tickets = await uow.tickets.get(order_id=order.id)
        tickets_dict = [ticket.to_dict() for ticket in tickets]

        return tickets_dict
    

async def update(cmd: UpdateCartRequest, uow: AbstractUnitOfWork):
    async with uow:
        order = await uow.orders.get(cmd.user_id)
        if order is None:
            return {'ok': False, 'data': 'Корзины не существует'}

        await uow.tickets.delete(order_id=order.id)

        if not cmd.tickets:
            return {'ok': True, 'data': 'Корзина очищена'}

        tickets_data = [{
            "event_id": t.event_id,
            "order_id": order.id,
            "price": t.price
        } for t in cmd.tickets]

        tickets = await uow.tickets.add_all(tickets_data)
        await uow.commit()

        return convert_to_dict_cart(order, tickets)
    

async def delete(user_id: int, uow: AbstractUnitOfWork):
    async with uow:
        try:
            order = await uow.orders.get(user_id=user_id)
            if order is None:
                return {'ok': False, 'data': 'У пользователя нет корзины'}

            await uow.tickets.delete(order.id)
            await uow.orders.delete(user_id)

            await uow.commit()

            return {'ok': True, 'data': 'Корзина была полностью очищена'}
        except Exception as e:
            print(e)

            return {'ok': False, 'data': 'Ошибка при очистки корзины'}




