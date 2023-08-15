import json
from dataclasses import asdict
from enum import Enum
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer
from broker.schemas import ProducerEvent

from application.settings.broker import Settings as Broker_settings


def serializer(obj: Any) -> bytes:
    if isinstance(obj, Enum):
        obj = obj.value
    if isinstance(obj, UUID):
        obj = obj.hex
    return json.dumps(obj).encode()


async def produce_event(event: ProducerEvent, broker_settings: Broker_settings) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=broker_settings.SERVER, value_serializer=serializer, key_serializer=serializer
    )
    await producer.start()
    await producer.send_and_wait(**asdict(event))
    await producer.stop()
