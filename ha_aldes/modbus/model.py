from typing import Any, Callable, Generic, TypeVar

from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    model_serializer,
    model_validator,
)
from typing_extensions import Annotated

from ha_aldes.i18n import _

T = TypeVar("T")


class SensorBase(BaseModel, Generic[T]):
    value: T
    category: str = Field(default="diagnostic")
    name: str
    id: str

    @model_serializer(when_used="json")
    def serialize(self) -> T:
        return self.value


OptionsDict = Annotated[
    dict[int, str],
    PlainSerializer(lambda x: x.values(), return_type=list[str], when_used="json"),
]


class SensorWithUnit(SensorBase[int]):
    unit: str = Field(default="")


class TemperaturSensor(SensorWithUnit):
    unit: str = Field(default="°C")


class VoltageSensor(SensorWithUnit):
    unit: str = Field(default="V")


class FlowSensor(SensorWithUnit):
    unit: str = Field(default="m³/h")


class PressureSensor(SensorWithUnit):
    unit: str = Field(default="Pa")


class SpeedSensor(SensorWithUnit):
    unit: str = Field(default="m/s")


class TimeSensor(SensorWithUnit):
    unit: str = Field(default="min")


class Selection(SensorBase[int]):
    options: OptionsDict

    @model_serializer(when_used="json")
    def serialize_value(self) -> str:
        value = self.options.get(self.value)
        assert value is not None
        return value


regulation_mode_mapping = {0: _("Auto"), 1: _("Hygro"), 2: _("Constant Speed")}

fan_mode_mapping = {
    0: _("Holidays"),
    1: _("Standard"),
    2: _("Kitchen High Speed"),
    3: _("Guests"),
}

bypass_exchanger_mapping = {
    0: _("Off"),
    1: _("Auto"),
    2: _("Winter optimisation"),
    3: _("Summer optimisation"),
    4: _("Open"),
}

regulation_system_mapping = {
    0: _("Separated Speeds"),
    1: _("Separated Airflows"),
    2: _("Separated Pressures"),
    3: _("Adjusted Pressure"),
}

bypass_position_mapping = {
    0: _("Close"),
    1: _("Open"),
    2: _("Closing"),
    3: _("Opening"),
    4: "Short circuit",
    5: _("Open circuit"),
    6: _("Under supply"),
}


class RegulationMode(Selection):
    options: OptionsDict = Field(default=regulation_mode_mapping)


class FanMode(Selection):
    options: OptionsDict = Field(default=fan_mode_mapping)


class BypassExchanger(Selection):
    options: OptionsDict = Field(default=bypass_exchanger_mapping)


class RegulationSystem(Selection):
    options: OptionsDict = Field(default=regulation_system_mapping)


class BypassPosition(Selection):
    options: OptionsDict = Field(default=bypass_position_mapping)


class AldesModbusResponse(BaseModel):
    id: SensorBase[str]
    serial_id: SensorBase[str]
    sw_version: SensorBase[str]
    regulation_mode: RegulationMode
    fan_mode: FanMode
    night_cooling: SensorBase[int]
    bypass_exchanger: BypassExchanger

    regulation_system: RegulationSystem
    holiday_time: TimeSensor
    kitchen_time: TimeSensor
    boost_time: TimeSensor
    filter_time: SensorBase[int]
    aux_time_1: SensorBase[int]
    aux_time_2: SensorBase[int]
    extract_airflow: FlowSensor
    supply_airflow: FlowSensor
    extract_pressure: PressureSensor
    supply_pressure: PressureSensor
    extract_speed: SpeedSensor
    supply_speed: SpeedSensor
    extract_supply_ratio: SensorBase[int]
    temperature_summer_comfort: TemperaturSensor
    u1_value: SensorBase[int]
    u2_value: SensorBase[int]
    supply_voltage: VoltageSensor
    voltage_0_10: SensorBase[int]
    switch_state: SensorBase[int]
    usb_state: SensorBase[int]
    radio_state: SensorWithUnit
    ibus_reception: SensorBase[int]
    ibus_auxiliary: SensorBase[int]
    hmi_installer: SensorBase[int]
    hmi_user: SensorBase[int]
    filter_condition: SensorBase[int]
    filter_condition_time: SensorBase[int]
    bypass_position: BypassPosition
    bypass_consumption: SensorBase[int]
    outdoor_air_temperature: TemperaturSensor
    indoor_air_temperature: TemperaturSensor
    error_code: SensorWithUnit
    error_code_2: SensorWithUnit

    @model_validator(mode="wrap")  # type: ignore  [arg-type]
    def _validate(
        self,
        handler: Callable[[type["AldesModbusResponse"], Any], "AldesModbusResponse"],
    ) -> "AldesModbusResponse":
        assert isinstance(self, dict)
        _data: dict[str, Any] = self
        _self = {k: {"name": _(k), "value": v, "id": k} for k, v in self.items()}
        validated_self = handler(_self)

        return validated_self
