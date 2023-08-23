import asyncio
import json
from datetime import datetime, time, timezone
from enum import Enum
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError

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


async def produce_event(
    event: ProducerEvent,
    broker_settings: Broker_settings,
    attempts: int = 5,
) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=broker_settings.SERVER,
        value_serializer=serializer,
        key_serializer=serializer,
        enable_idempotence=True,
    )
    await producer.start()
    step = 1
    while step <= attempts:
        try:
            await producer.send_and_wait(**event.model_dump(exclude_none=True))
        except KafkaTimeoutError as exc:
            # TODO: добавить логгер, вынести продюсера как отдельный инструмент (класс/модуль/либа),
            #  заменить цикл на рекурсию
            await asyncio.sleep(2 * step)
            step += 1
        else:
            break
    # TODO: если попытки закончились, отправить в аутбокс.
    await producer.stop()
