import asyncio
from asyncio import AbstractEventLoop

from ha_aldes.modbus.client import modbus_polling_loop
from ha_aldes.mqtt import mqtt_action_loop, publish


async def main(event_loop: AbstractEventLoop) -> None:
    modbus_task = event_loop.create_task(modbus_polling_loop(publish))
    await mqtt_action_loop()
    await modbus_task


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
