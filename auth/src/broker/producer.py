import json
from dataclasses import asdict
from datetime import datetime, time, timezone
from enum import Enum
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer

from application.settings.broker import Settings as Broker_settings
from broker.schemas import ProducerEvent


def recursive_serializer(obj: Any) -> Any:
    if isinstance(obj, Enum):
        obj = obj.value
    if isinstance(obj, UUID):
        obj = obj.hex
    if isinstance(obj, (datetime, time)):
        obj = obj.replace(tzinfo=timezone.utc).isoformat(timespec="milliseconds")
    if isinstance(obj, dict):
        obj = {key: recursive_serializer(value) for key, value in obj.items()}
    if isinstance(obj, list):
        obj = [recursive_serializer(elem) for elem in obj]
    return obj


def serializer(obj: Any) -> bytes:
    return json.dumps(recursive_serializer(obj)).encode()


async def produce_event(event: ProducerEvent, broker_settings: Broker_settings) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=broker_settings.SERVER, value_serializer=serializer, key_serializer=serializer
    )
    await producer.start()
    await producer.send_and_wait(**asdict(event))
    await producer.stop()
