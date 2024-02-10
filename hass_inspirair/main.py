import logging
from asyncio import AbstractEventLoop

from hass_inspirair.config import DEFAULT_CONFIG
from hass_inspirair.modbus.client import get_async_client, modbus_polling_loop
from hass_inspirair.mqtt.actions import mqtt_action_loop, register
from hass_inspirair.mqtt.client import get_client as get_mqtt_client

logger = logging.getLogger(__name__)


async def main_loop(event_loop: AbstractEventLoop) -> None:
    logger.info("Starting main loop")
    logger.debug(DEFAULT_CONFIG)
    async with await get_async_client() as modbus_client:
        async with get_mqtt_client() as mqtt_client:
            args = (modbus_client, mqtt_client)
            await register(*args)
            modbus_task = event_loop.create_task(modbus_polling_loop(*args))
            await mqtt_action_loop(*args)
            await modbus_task
