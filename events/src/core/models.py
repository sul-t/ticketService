from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Any

import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime

from config import settings
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
            "ticket_price": self.ticket_price,
        }


class AbstractRmqSender(ABC):
    @abstractmethod
    def send_event(self, event_name: str, payload):
        pass


class RmqAdapter(AbstractRmqSender):
    def __init__(self, queue: str):
        self.connection = None
        self.channel = None
        self.queue = queue


    def connect(self):
        try:
            if self.connection and not self.connection.is_closed():
                self.connection.close()

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
            self.channel = self.connection.channel()

            self.channel.queue_declare(queue=self.queue, durable=True)
            self.channel.confirm_delivery()
        except AMQPConnectionError as e:
            print(f"Ошибка подклчюения к RabbitMQ: {e}")
            self.connection = None
            self.channel = None


    def send_event(self, event_name: str, payload: dict[str, Any]):
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()

            self.channel.basic_publish(
                exchange="",
                routing_key="events_to_orders",
                body=json.dumps({"event_type": event_name, "payload": payload}).encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except (AMQPConnectionError, ChannelClosedByBroker) as e:
            print(f"Ошибка отправки в RabbitMQ: {e}")
            self.connect()


    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
