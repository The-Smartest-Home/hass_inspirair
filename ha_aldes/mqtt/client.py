import logging

from aiomqtt import Client

from ha_aldes.config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


def get_client() -> Client:
    return Client(*DEFAULT_CONFIG.mqtt)


async def _publish(topic: str, value: str) -> None:
    async with get_client() as client:
        await client.publish(topic, value)


async def publish(topic: str, value: str) -> None:
    await _publish(topic, value)
