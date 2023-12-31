import os
import socket
from typing import NamedTuple, Optional

from ha_aldes.i18n import _


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
    hostname: str = os.getenv("HA_ALDES_MQTT_HOST", "localhost")
    port: int = int(os.getenv("HA_ALDES_MQTT_PORT", "1883"))


class ModbusConfig(NamedTuple):
    port: str = os.getenv("HA_ALDES_MODBUS_SERIAL_DEVICE", "/dev/ttyACM")
    baudrate: int = 115200
    bytesize: int = 8
    parity: str = "E"
    stopbits: int = 1


class Config(NamedTuple):
    manufacturer: str = "Aldes"
    model: str = "InspirAIR Home SC 370"  # TODO might be something else
    discovery_prefix: str = os.getenv("HA_ALDES_MQTT_PREFIX", "homeassistant")
    ha_state_topic: str = "/".join([discovery_prefix, "status"])
    entity_name: str = _("Ventilation")
    host: str = get_ip()
    mqtt: MQTTConfig = MQTTConfig()
    modbus: ModbusConfig = ModbusConfig()

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
