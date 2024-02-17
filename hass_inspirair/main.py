import logging
from asyncio import AbstractEventLoop

from hass_inspirair.config import DEFAULT_CONFIG
from hass_inspirair.modbus.client import modbus_polling_loop
from hass_inspirair.mqtt.actions import mqtt_action_loop, register
from hass_inspirair.mqtt.client import get_client as get_mqtt_client

logger = logging.getLogger(__name__)


async def main_loop(event_loop: AbstractEventLoop) -> None:
    logger.info("Starting main loop")
    logger.debug(DEFAULT_CONFIG)
    async with get_mqtt_client() as mqtt_client:
        await register(mqtt_client)
        modbus_task = event_loop.create_task(modbus_polling_loop(mqtt_client))
        await mqtt_action_loop(mqtt_client)
        await modbus_task
