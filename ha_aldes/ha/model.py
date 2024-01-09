from collections import namedtuple
from typing import NamedTuple, Optional

from pydantic import BaseModel, Field

from ha_aldes.modbus.model import fan_mode_mapping

Sensor = namedtuple("Sensor", "name, id, unit, category")

DefaultConfig = namedtuple(
    "DefaultConfig", "manufacturer, model, discovery_prefix, entity_name"
)


class Device(BaseModel):
    configuration_url: str
    # connections: list[str]
    identifiers: str
    manufacturer: str
    model: str
    name: str
    via_device: str
    sw_version: str
    hw_version: str


class DeviceInfo(NamedTuple):
    enabled_by_default: bool
    device: Device


class ClimateConfig(BaseModel):
    name: Optional[str]
    modes: list[str] = Field(default=["fan_only"])
    fan_modes: list[str] = Field(default=list(fan_mode_mapping.values()))
    power_command_topic: str
    mode_state_topic: str
    temperature_unit: str = Field(default="C")
    unique_id: str
    fan_mode_state_topic: str
    fan_mode_command_topic: str
    current_temperature_topic: str
    fan_mode_state_template: str
    current_temperature_template: str

    mode_state_template: str = Field(default="fan_only")
    json_attributes_topic: str
    device: Device
    config_topic: str = Field(exclude=True)


class SelectConfig(BaseModel):
    name: str
    unique_id: str
    state_topic: str
    command_topic: str
    options: list[str]
    entity_category: str
    optimistic: bool
    value_template: str
    device: Device
    config_topic: str = Field(exclude=True)


class SensorConfig(BaseModel):
    name: str
    unique_id: str
    state_topic: str
    unit_of_measurement: Optional[str] = Field(default="")
    entity_category: str
    value_template: str
    device: Device
    config_topic: str = Field(exclude=True)
    device_class: Optional[str]
