import logging

from aiomqtt import Message

from ha_aldes.config import Config
from ha_aldes.ha.devices import create_all
from ha_aldes.modbus.client import poll_push
from ha_aldes.mqtt.client import get_client, publish

HA_IS_ONLINE = False

logger = logging.getLogger(__name__)


async def register() -> None:
    logger.info("handle_register")
    response = await poll_push()
    for config in create_all(response):
        await publish(config.config_topic + "/config", config.model_dump_json())


async def set_fan_mode(message: Message) -> None:
    # TODO implement me
    logger.info("set_fan_mode")
    # update current values
    await poll_push()


async def set_unknown(message: Message) -> None:
    # update current values
    logger.warning(f"Setter for unimplemented selection: {message.topic}")
    await poll_push()


async def handle_ha_state(message: Message) -> None:
    logger.info("handle_ha_state")
    global HA_IS_ONLINE
    _HA_IS_ONLINE = HA_IS_ONLINE
    if message.payload.decode(encoding="utf-8") == "online":
        HA_IS_ONLINE = True
    elif message.payload.decode(encoding="utf-8") == "offline":
        HA_IS_ONLINE = False
    else:
        print(f"unknown state received {message.payload}'")

    if HA_IS_ONLINE and not _HA_IS_ONLINE:
        # switched from offline to online
        await register()


async def mqtt_action_loop() -> None:
    logger.info("starting mqtt action loop")
    # poll one time to get the unique id
    response = await poll_push()
    config = Config()
    setter_topic = "/".join(
        [config.get_base_topic("+", response.serial_id.value, "+"), "set"]
    )
    config_topic = "/".join(
        [config.get_base_topic("+", response.serial_id.value, "+"), "config"]
    )

    async with get_client() as client:
        async with client.messages() as messages:
            # react to ha status change and setters

            await client.subscribe(setter_topic)

            await client.subscribe(config.ha_state_topic)
            await client.subscribe(config_topic)

            async for message in messages:
                logger.debug(message.__dict__)
                if message.topic.matches(config.ha_state_topic):
                    await handle_ha_state(message)
                elif message.topic.matches(setter_topic):
                    if message.topic.matches(f"+/+/{response.fan_mode.id}/+/set"):
                        await set_fan_mode(message)
                    else:
                        await set_unknown(message)
                elif message.topic.matches(config_topic):
                    pass
                else:
                    logger.warning(
                        f"Received message on unexpected topic {message.topic}"
                    )
