import enum
import os
from types import DynamicClassAttribute
from typing import Any


class EnvConfig(enum.Enum):
    LANGUAGE = "de"
    HA_ALDES_MQTT_HOST = "localhost"
    HA_ALDES_MQTT_PORT = 1883
    HA_ALDES_MQTT_PREFIX = "homeassistant"

    HA_ALDES_MODBUS_CLIENT = "ha_aldes.modbus.client.get_async_serial_client"
    HA_ALDES_MODBUS_POLLING_INTERVALL = 30
    HA_ALDES_MODBUS_SERIAL_DEVICE = "/dev/ttyACM"
    HA_ALDES_MODBUS_TCP_HOST = "localhost"
    HA_ALDES_MODBUS_TCP_PORT = 5020

    @DynamicClassAttribute
    def value(self) -> Any:
        env_value = os.getenv(self.name)
        if env_value is None:
            return super().value
        else:
            value_type = type(super().value)
            return value_type(env_value)
