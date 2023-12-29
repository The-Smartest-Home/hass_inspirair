import os
import socket
from typing import Generator, Union

from ha_aldes.ha.model import (
    ClimateConfig,
    DefaultConfig,
    Device,
    DeviceInfo,
    SelectConfig,
    SensorConfig,
    Topics,
)
from ha_aldes.i18n import _
from ha_aldes.modbus.model import AldesModbusResponse, Selection, SensorWithUnit

DEFAULT_CONFIG = DefaultConfig(
    **{
        "manufacturer": "Aldes",
        "model": "InspirAIR Home SC 370",  # TODO might be something else
        "discovery_prefix": os.getenv("HA_ALDES_MQTT_PREFIX", "homeassistant"),
        "entity_name": _("Ventilation"),
    }
)


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("127.0.0.1", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


print(get_ip())


def create_device(modbus_data: AldesModbusResponse) -> tuple[DeviceInfo, Topics]:
    device_info = DeviceInfo(
        enabled_by_default=True,
        device=Device(
            **{
                "configuration_url": f"http://{get_ip()}",
                "connections": ['["modbus", "2;115200;1E1"]'],
                "manufacturer": DEFAULT_CONFIG.manufacturer,
                "identifiers": modbus_data.serial_id.value,
                "name": DEFAULT_CONFIG.entity_name,
                "model": DEFAULT_CONFIG.model,
                "sw_version": modbus_data.sw_version.value,
                "hw_version": modbus_data.id.value,
                "via_device": "mqtt",
            }
        ),
    )

    default_topic = [
        DEFAULT_CONFIG.discovery_prefix,
        "ventilation",
        modbus_data.serial_id.value,
    ]

    topics = Topics(
        state="/".join([*default_topic, "state"]),
        fan_mode="/".join([*default_topic, "state", modbus_data.fan_mode.id, "set"]),
    )

    return device_info, topics


def create_select(
    device_info: DeviceInfo, topics: Topics, select: Selection
) -> SelectConfig:
    return SelectConfig(
        name=select.name,
        unique_id="_".join([device_info.device.identifiers, select.id]),
        state_topic=topics.state,
        command_topic="/".join([topics.state, select.id, "set"]),
        options=select.options.values(),
        entity_category=select.category,
        optimistic=False,
        value_template="{{value_json.%s}}" % select.id,
    )


def create_sensor(
    device_info: DeviceInfo, topics: Topics, sensor: SensorWithUnit
) -> SensorConfig:
    return SensorConfig(
        name=sensor.name,
        unique_id="_".join([device_info.device.identifiers, sensor.id]),
        state_topic=topics.state,
        unit_of_measurement=sensor.unit,
        entity_category=sensor.category,
        value_template="{{value_json.%s}}" % sensor.id,
    )


def create_climate(
    device_info: DeviceInfo, topics: Topics, modbus_data: AldesModbusResponse
) -> ClimateConfig:
    return ClimateConfig(
        name=device_info.device.name,
        power_command_topic="/".join([topics.state, "power", "set"]),
        mode_state_topic=topics.state,
        unique_id="_".join([device_info.device.identifiers, "climate"]),
        fan_mode_state_topic=topics.state,
        fan_mode_command_topic=topics.fan_mode,
        current_temperature_topic=topics.state,
        fan_mode_state_template="{{value_json.%s}}" % modbus_data.fan_mode.id,
        current_temperature_template="{{value_json.%s}}"
        % modbus_data.indoor_air_temperature.id,
        json_attributes_topic=topics.state,
    )


def create_all(
    modbus_data: AldesModbusResponse,
) -> Generator[Union[ClimateConfig, SelectConfig, SensorConfig], None, None]:
    device, topics = create_device(modbus_data)
    yield create_climate(device, topics, modbus_data)
    for k, v in modbus_data.model_fields.items():
        if v.annotation is None:
            continue
        if issubclass(v.annotation, Selection):
            yield create_select(device, topics, getattr(modbus_data, k))
        if issubclass(v.annotation, SensorWithUnit):
            yield create_sensor(device, topics, getattr(modbus_data, k))
    return None
