from typing import Any, Generator, Union

from ha_aldes.config import DEFAULT_CONFIG, Config
from ha_aldes.env_config import EnvConfig
from ha_aldes.ha.model import (
    ClimateConfig,
    Device,
    DeviceInfo,
    SelectConfig,
    SensorConfig,
)
from ha_aldes.modbus.model import AldesModbusResponse, Selection, SensorWithUnit


def create_device(modbus_data: AldesModbusResponse) -> DeviceInfo:
    device_info = DeviceInfo(
        enabled_by_default=True,
        device=Device(
            **{
                "configuration_url": f"http://{DEFAULT_CONFIG.host}",
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

    return device_info


def create_select(device_info: DeviceInfo, select: Selection) -> SelectConfig:
    config = Config()
    return SelectConfig(
        name=select.name,
        unique_id="_".join([device_info.device.identifiers, select.id]),
        state_topic=config.get_state_topic(device_info.device.identifiers),
        command_topic="/".join(
            [
                config.get_base_topic(
                    select.id, device_info.device.identifiers, "select"
                ),
                "set",
            ]
        ),
        options=select.options.values(),
        entity_category=select.category,
        optimistic=False,
        value_template="{{value_json.%s}}" % select.id,
        expire_after=EnvConfig.HA_ALDES_MODBUS_POLLING_INTERVALL * 2,
        object_id=config.get_object_id(select.id),
        device=device_info.device,
        config_topic=config.get_base_topic(
            select.id, device_info.device.identifiers, "select"
        ),
    )


def create_sensor(device_info: DeviceInfo, sensor: SensorWithUnit[Any]) -> SensorConfig:
    config = Config()
    return SensorConfig(
        name=sensor.name,
        unique_id="_".join([device_info.device.identifiers, sensor.id]),
        state_topic=config.get_state_topic(device_info.device.identifiers),
        unit_of_measurement=sensor.unit,
        entity_category=sensor.category,
        value_template="{{value_json.%s}}" % sensor.id,
        device=device_info.device,
        config_topic=config.get_base_topic(
            sensor.id, device_info.device.identifiers, "sensor"
        ),
        device_class=sensor.device_class,
        object_id=config.get_object_id(sensor.id),
        expire_after=EnvConfig.HA_ALDES_MODBUS_POLLING_INTERVALL * 2,
    )


def create_climate(
    device_info: DeviceInfo, modbus_data: AldesModbusResponse
) -> ClimateConfig:
    config = Config()
    state_topic = config.get_state_topic(device_info.device.identifiers)
    power_topic = "/".join(
        [
            config.get_base_topic("power", device_info.device.identifiers, "climate"),
            "set",
        ]
    )
    fan_topic = "/".join(
        [
            config.get_base_topic(
                modbus_data.fan_mode.id, device_info.device.identifiers, "climate"
            ),
            "set",
        ]
    )
    return ClimateConfig(
        name=None,
        power_command_topic=power_topic,
        mode_state_topic=state_topic,
        unique_id="_".join([device_info.device.identifiers, "climate"]),
        fan_mode_state_topic=state_topic,
        fan_mode_command_topic=fan_topic,
        current_temperature_topic=state_topic,
        fan_mode_state_template="{{value_json.%s}}" % modbus_data.fan_mode.id,
        current_temperature_template="{{value_json.%s}}"
        % modbus_data.indoor_air_temperature.id,
        json_attributes_topic=state_topic,
        device=device_info.device,
        config_topic=config.get_base_topic(
            "climate", device_info.device.identifiers, "climate"
        ),
        object_id=config.get_object_id(),
        expire_after=EnvConfig.HA_ALDES_MODBUS_POLLING_INTERVALL * 2,
    )


def create_all(
    modbus_data: AldesModbusResponse,
) -> Generator[Union[ClimateConfig, SelectConfig, SensorConfig], None, None]:
    device = create_device(modbus_data)
    yield create_climate(device, modbus_data)
    for k, v in modbus_data.model_fields.items():
        if v.annotation is None:
            continue
        if issubclass(v.annotation, Selection):
            yield create_select(device, getattr(modbus_data, k))
        if issubclass(v.annotation, SensorWithUnit):
            yield create_sensor(device, getattr(modbus_data, k))
    return None
