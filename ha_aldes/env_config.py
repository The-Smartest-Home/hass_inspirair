import os
from typing import Any


class EnvConfigMeta(type):
    LANGUAGE = "de"
    HA_ALDES_MQTT_HOST = "localhost"
    HA_ALDES_MQTT_PORT = 1883
    HA_ALDES_MQTT_PREFIX = "homeassistant"

    HA_ALDES_MODBUS_CLIENT = "ha_aldes.modbus.client.get_async_serial_client"
    HA_ALDES_MODBUS_POLLING_INTERVALL = 30
    HA_ALDES_MODBUS_SERIAL_DEVICE = "/dev/ttyACM"
    HA_ALDES_MODBUS_TCP_HOST = "localhost"
    HA_ALDES_MODBUS_TCP_PORT = 5020

    def __getattribute__(self, item: str) -> Any:
        super_value = super().__getattribute__(item)
        if not item.startswith("_"):
            env_value = os.getenv(item)
            if env_value is None:
                return super_value
            else:
                value_type = type(super_value)
                return value_type(env_value)

        return super_value


class EnvConfig(metaclass=EnvConfigMeta):
    pass
