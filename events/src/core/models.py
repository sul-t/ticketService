from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime

from src.core.database import Base



class Event(Base):
    name: Mapped[str]
    description: Mapped[str]
    event_date: Mapped[datetime] = mapped_column(DateTime, unique=True)
    available_tickets: Mapped[int]
    ticket_price: Mapped[int]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "event_date": self.event_date,
            "available_tickets": self.available_tickets,
            "ticket_price": self.ticket_price
        }



class AbstractRmqSender(ABC):
    @abstractmethod
    def send_event(self, event_name: str, payload):
        pass

class RmqAdapter(AbstractRmqSender):
    def send_event(self, event_name, payload):
        self._rmq_client.send('queue', event_name, payload)