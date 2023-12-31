import logging
from asyncio import AbstractEventLoop

from ha_aldes.config import DEFAULT_CONFIG
from ha_aldes.modbus.client import modbus_polling_loop
from ha_aldes.mqtt.actions import mqtt_action_loop, register

logger = logging.getLogger(__name__)


async def main_loop(event_loop: AbstractEventLoop) -> None:
    logger.info("Starting main loop")
    logger.debug(DEFAULT_CONFIG)
    await register()
    modbus_task = event_loop.create_task(modbus_polling_loop())
    await mqtt_action_loop()
    await modbus_task
