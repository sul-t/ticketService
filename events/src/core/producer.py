from abc import ABC, abstractmethod

import pika

from events.src.core.models import AbstractRmqSender


def admin_change_ticket_price(event_id, new_price, db, rmq_sender: AbstractRmqSender)
    db.change_price(event_id, new_price)
    rmq_sender.send_event(TICKET_PRICE_CHANGE, {})