import logging

from aiomqtt import Client, Message
from pymodbus.client.base import ModbusBaseClient

from hass_inspirair.config import Config
from hass_inspirair.ha.devices import create_all
from hass_inspirair.modbus.client import change_fan_mode, poll_push
from hass_inspirair.modbus.model import fan_mode_mapping
from hass_inspirair.mqtt.client import publish

HA_IS_ONLINE = False

logger = logging.getLogger(__name__)


async def register(modbus_client: ModbusBaseClient, mqtt_client: Client) -> None:
    logger.info("handle_register")
    response = await poll_push(modbus_client, mqtt_client)
    for config in create_all(response):
        await publish(
            config.config_topic + "/config", config.model_dump_json(), mqtt_client
        )


async def set_fan_mode(
    message: Message,
    modbus_client: ModbusBaseClient,
    mqtt_client: Client,
) -> None:
    logger.info(f"set_fan_mode:  {message.payload}")
    for k, v in fan_mode_mapping.items():
        if v == message.payload.decode(encoding="utf-8"):
            if await change_fan_mode(k, modbus_client=modbus_client):
                await poll_push(modbus_client, mqtt_client)
            return

    logger.error("Could not update fan_mode for message=%s", message.payload)


async def set_unknown(
    message: Message, modbus_client: ModbusBaseClient, mqtt_client: Client
) -> None:
    # update current values
    logger.warning(
        f"Setter for unimplemented selection: {message.topic} - {message.payload}"
    )
    await poll_push(modbus_client, mqtt_client)


async def handle_ha_state(
    message: Message, modbus_client: ModbusBaseClient, mqtt_client: Client
) -> None:
    logger.info(f"handle_ha_state: {message.payload}")
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
        await register(modbus_client, mqtt_client)


async def mqtt_action_loop(
    modbus_client: ModbusBaseClient, mqtt_client: Client
) -> None:
    mqtt_client.subscribe
    logger.info("starting mqtt rpc loop")
    # poll one time to get the unique id
    response = await poll_push(modbus_client, mqtt_client)
    config = Config()
    setter_topic = "/".join(
        [config.get_base_topic("+", response.serial_id.value, "+"), "set"]
    )
    config_topic = "/".join(
        [config.get_base_topic("+", response.serial_id.value, "+"), "config"]
    )

    async with mqtt_client.messages() as messages:
        # react to ha status change and setters

        await mqtt_client.subscribe(setter_topic)

        await mqtt_client.subscribe(config.ha_state_topic)
        await mqtt_client.subscribe(config_topic)

        async for message in messages:
            logger.debug(message.__dict__)
            if message.topic.matches(config.ha_state_topic):
                await handle_ha_state(message, modbus_client, mqtt_client)
            elif message.topic.matches(setter_topic):
                if message.topic.matches(f"+/+/{response.fan_mode.id}/+/set"):
                    await set_fan_mode(message, modbus_client, mqtt_client)
                else:
                    await set_unknown(message, modbus_client, mqtt_client)
            elif message.topic.matches(config_topic):
                pass
            else:
                logger.warning(f"Received message on unexpected topic {message.topic}")
