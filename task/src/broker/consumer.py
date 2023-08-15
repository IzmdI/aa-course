import asyncio
import json
import sys
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from application.settings.broker import Settings as Broker_settings
from broker.dependencies import broker_settings, get_broker_service
from broker.schemas import UserMessage
from broker.service import BrokerUserService


def key_deserializer(obj: bytes) -> UUID | str:
    if isinstance(obj, bytes):
        return obj.decode()


def deserializer(obj: bytes) -> Any:
    return json.loads(obj.decode())


async def consume(broker_settings: Broker_settings) -> None:
    consumer = AIOKafkaConsumer(
        broker_settings.TOPIC_USER_STREAM,
        broker_settings.TOPIC_USER_ROLE_CHANGED,
        bootstrap_servers=broker_settings.SERVER,
        enable_auto_commit=True,
        key_deserializer=key_deserializer,
        value_deserializer=deserializer,
    )
    broker_service: BrokerUserService = await get_broker_service()
    await consumer.start()
    try:
        async for msg in consumer:
            await broker_service(UserMessage(**msg.value))
    finally:
        await consumer.stop()


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    asyncio.run(consume(broker_settings))
