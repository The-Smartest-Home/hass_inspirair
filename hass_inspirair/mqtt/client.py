import logging

from aiomqtt import Client

from hass_inspirair.config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


def get_client() -> Client:
    return Client(**DEFAULT_CONFIG.mqtt._asdict())


async def publish(topic: str, value: str, client: Client = None) -> None:
    if client is None:
        async with get_client() as _client:
            await publish(topic, value, _client)
    else:
        await client.publish(topic, value)
