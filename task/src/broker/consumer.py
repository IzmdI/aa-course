import asyncio
import json
import sys
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from task.src.application.settings.broker import Settings as Broker_settings
from task.src.broker.dependencies import broker_settings, get_user_broker_service
from task.src.broker.service import BrokerUserService
from task.src.broker.schemas import (
    EventDataUserRole,
    EventDataUserStreaming,
)

from schema_registry import validators

user_role_validator = validators.UserRoleSchemaValidator()
user_streaming_validator = validators.UserStreamingSchemaValidator()


def key_deserializer(obj: bytes) -> UUID | str:
    return obj.decode()


def deserializer(obj: bytes) -> Any:
    return json.loads(obj.decode())


async def consume_users(broker_settings: Broker_settings) -> None:
    consumer = AIOKafkaConsumer(
        broker_settings.TOPIC_USER_STREAM,
        broker_settings.TOPIC_USER_ROLE,
        bootstrap_servers=broker_settings.SERVER,
        enable_auto_commit=True,
        key_deserializer=key_deserializer,
        value_deserializer=deserializer,
    )
    user_service: BrokerUserService = await get_user_broker_service()
    await consumer.start()
    try:
        async for msg in consumer:
            match msg.topic:
                case broker_settings.TOPIC_USER_STREAM:
                    validator = user_streaming_validator
                    event = EventDataUserStreaming
                case broker_settings.TOPIC_USER_ROLE:
                    validator = user_role_validator
                    event = EventDataUserRole
                case _:
                    continue
            if validator.is_valid(msg.value):
                await user_service(event(**msg.value).event_data)
            else:
                # TODO: невалидные сообщения будем сваливать в мёртвую очередь,
                #  которую будет разбирать специально обученный попуг
                continue
    finally:
        await consumer.stop()


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        asyncio.run(consume_users(broker_settings))
    except (RuntimeError, SystemExit, KeyboardInterrupt):
        pass
