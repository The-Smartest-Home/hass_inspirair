import configparser
import os
from typing import Any


class EnvConfigMeta(type):
    """Configuration options for the application.

    The following order will be applied while looking options up.

    1. Environment variables
    2. Config file
    3. default values defined here
    """

    HI_CFG_LANGUAGE = "de"
    """The language in which selection options and entity names will be registered"""

    HI_CFG_LOGLEVEL = "INFO"
    """logging level"""

    HI_MQTT_HOST = "localhost"
    """MQTT Broker Hostname"""

    HI_MQTT_PORT = 1883
    """MQTT Broker Port"""

    HI_MQTT_PREFIX = "homeassistant"
    """MQTT topic prefix, which will be applied on every request"""

    HI_MQTT_USERNAME = ""
    """MQTT username"""

    HI_MQTT_PASSWORD = ""
    """MQTT password"""

    HI_MODBUS_CLIENT = "hass_inspirair.modbus.client.get_async_serial_client"
    """
    "<package>.<function>" which should be used to create an modbus client.
    
    e.g. "hass_inspirair.modbus.client.get_async_serial_client" will basically result in an import of the following form:
    
    ``from hass_inspirair.modbus.client import get_async_serial_client``
    
    """

    HI_MODBUS_SLAVE_ID = 2
    """Slave id used to connect to"""

    HI_MODBUS_POLLING_INTERVALL = 30
    """Frequency of polling in seconds"""

    HI_MODBUS_SERIAL_DEVICE = "/dev/ttyACM"
    """Serial device when using hass_inspirair.modbus.client.get_async_serial_client"""

    HI_MODBUS_TCP_HOST = "localhost"
    """Hostname when using hass_inspirair.modbus.client.get_async_tcp_client"""

    HI_MODBUS_TCP_PORT = 5020
    """Port when using hass_inspirair.modbus.client.get_async_tcp_client"""

    _file_config = None

    def _read_config(self) -> dict[str, str]:
        if self._file_config is None:
            config = configparser.ConfigParser()
            config.read(os.getenv("HI_CFG_FILE", "./config.ini"))

            self._file_config = {
                "_".join(["HI", sec_name, config_key]).upper(): config_value
                for sec_name, sec_val in config.items()
                for config_key, config_value in sec_val.items()
            }
        return self._file_config

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
