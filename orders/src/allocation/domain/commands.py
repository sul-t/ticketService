from pydantic import BaseModel

class Command(BaseModel):
    pass


class CartTicketItem(Command):
    event_id: int
    price: int


class UpdateCartRequest(BaseModel):
    user_id: int
    tickets: list[CartTicketItem]

