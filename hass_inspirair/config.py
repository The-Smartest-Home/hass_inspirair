import socket
from typing import NamedTuple, Optional

from hass_inspirair.i18n import _

from .env_config import EnvConfig


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("255.255.255.0", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


class MQTTConfig(NamedTuple):
    hostname: str = EnvConfig.HI_MQTT_HOST
    port: int = EnvConfig.HI_MQTT_PORT
    username: str = EnvConfig.HI_MQTT_USERNAME
    password: str = EnvConfig.HI_MQTT_PASSWORD


class ModbusConfig(NamedTuple):
    client: str = EnvConfig.HI_MODBUS_CLIENT
    polling_intervall: int = EnvConfig.HI_MODBUS_POLLING_INTERVALL


BASE_NAME = "Ventilation"


class Config(NamedTuple):
    manufacturer: str = "Aldes"
    model: str = "InspirAIR Home SC 370"  # TODO might be something else
    discovery_prefix: str = EnvConfig.HI_MQTT_PREFIX
    ha_state_topic: str = "/".join([discovery_prefix, "status"])
    entity_name: str = _(BASE_NAME)
    host: str = get_ip()
    mqtt: MQTTConfig = MQTTConfig()
    modbus: ModbusConfig = ModbusConfig()

    def get_object_id(self, sensor_id: Optional[str] = None) -> str:
        if sensor_id is not None:
            return "_".join([BASE_NAME, sensor_id]).lower()
        return BASE_NAME.lower()

    def get_base_topic(
        self, node_id: Optional[str], object_id: str, component: str
    ) -> str:
        return "/".join(
            a
            for a in [
                self.discovery_prefix,
                component,
                node_id,
                object_id,
            ]
            if a is not None
        )

    def get_state_topic(self, object_id: str) -> str:
        return "/".join([self.get_base_topic(None, object_id, "climate"), "state"])


DEFAULT_CONFIG = Config()
