import os

from aiomqtt import Client


def get_client() -> Client:
    return Client(
        os.getenv("HA_ALDES_MQTT_HOST", "localhost"),
        port=int(os.getenv("HA_ALDES_MQTT_PORT", "1883")),
    )


async def _publish(value: str) -> None:
    async with get_client() as client:
        await client.publish("some/topic", payload=value)


async def publish(value: str) -> None:
    await _publish(value)


async def mqtt_action_loop() -> None:
    async with get_client() as client:
        async with client.messages() as messages:
            # TODO filter message
            await client.subscribe("#")
            async for message in messages:
                # TODO filter message
                print(message.__dict__)
