import configparser
import os
from typing import Any


class EnvConfigMeta(type):
    HI_CFG_LANGUAGE = "de"
    HI_CFG_LOGLEVEL = "INFO"
    HI_MQTT_HOST = "localhost"
    HI_MQTT_PORT = 1883
    HI_MQTT_PREFIX = "homeassistant"
    HI_MQTT_USERNAME = ""
    HI_MQTT_PASSWORD = ""

    HI_MODBUS_CLIENT = "hass_inspirair.modbus.client.get_async_serial_client"
    HI_MODBUS_POLLING_INTERVALL = 30
    HI_MODBUS_SERIAL_DEVICE = "/dev/ttyACM"
    HI_MODBUS_TCP_HOST = "localhost"
    HI_MODBUS_TCP_PORT = 5020

    def _read_config(self) -> dict[str, str]:
        if not hasattr(self, "__file_config"):
            config = configparser.ConfigParser()
            config.read("config.ini")

            self.__file_config = {
                "_".join(["HI", sec_name, config_key]).upper(): config_value
                for sec_name, sec_val in config.items()
                for config_key, config_value in sec_val.items()
            }
        return self.__file_config

    def __getattribute__(self, item: str) -> Any:
        super_value = super().__getattribute__(item)
        if not item.startswith("_"):
            file_config = self._read_config()
            env_value = os.getenv(item)
            file_value = file_config.get(item, None)
            cfg_value = env_value if env_value is not None else file_value

            if cfg_value is None:
                return super_value
            else:
                value_type = type(super_value)
                return value_type(cfg_value)

        return super_value


class EnvConfig(metaclass=EnvConfigMeta):
    pass
