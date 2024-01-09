from typing import Any, Callable, Generic, Optional, TypeVar

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


class SensorWithUnit(SensorBase[T], Generic[T]):
    unit: str = Field(default="")
    device_class: Optional[str] = Field(default=None)


class TemperaturSensor(SensorWithUnit[float]):
    unit: str = Field(default="°C")
    device_class: str = "temperature"


class VoltageSensor(SensorWithUnit[int]):
    unit: str = Field(default="V")
    device_class: str = "voltage"


class FlowSensor(SensorWithUnit[int]):
    unit: str = Field(default="m³/h")
    device_class: Optional[str] = None


class PressureSensor(SensorWithUnit[int]):
    unit: str = Field(default="Pa")
    device_class: str = "atmospheric_pressure"


class SpeedSensor(SensorWithUnit[int]):
    unit: str = Field(default="m/s")
    device_class: str = "speed"


class TimeSensor(SensorWithUnit[int]):
    unit: str = Field(default="min")
    device_class: str = "duration"


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
    4: _("Short circuit"),
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
    id: SensorBase[str] = Field(description=_("id"))
    serial_id: SensorBase[str] = Field(description=_("serial_id"))
    sw_version: SensorBase[str] = Field(description=_("sw_version"))
    regulation_mode: RegulationMode = Field(description=_("regulation_mode"))
    fan_mode: FanMode = Field(description=_("fan_mode"))
    night_cooling: SensorBase[int] = Field(description=_("night_cooling"))
    bypass_exchanger: BypassExchanger = Field(description=_("bypass_exchanger"))

    regulation_system: RegulationSystem = Field(description=_("regulation_system"))
    holiday_time: TimeSensor = Field(description=_("holiday_time"))
    kitchen_time: TimeSensor = Field(description=_("kitchen_time"))
    boost_time: TimeSensor = Field(description=_("boost_time"))
    filter_time: SensorBase[int] = Field(description=_("filter_time"))
    aux_time_1: SensorBase[int] = Field(description=_("aux_time_1"))
    aux_time_2: SensorBase[int] = Field(description=_("aux_time_2"))
    extract_airflow: FlowSensor = Field(description=_("extract_airflow"))
    supply_airflow: FlowSensor = Field(description=_("supply_airflow"))
    extract_pressure: PressureSensor = Field(description=_("extract_pressure"))
    supply_pressure: PressureSensor = Field(description=_("supply_pressure"))
    extract_speed: SpeedSensor = Field(description=_("extract_speed"))
    supply_speed: SpeedSensor = Field(description=_("supply_speed"))
    extract_supply_ratio: SensorBase[int] = Field(description=_("extract_supply_ratio"))
    temperature_summer_comfort: TemperaturSensor = Field(
        description=_("temperature_summer_comfort")
    )
    u1_value: SensorBase[int] = Field(description=_("u1_value"))
    u2_value: SensorBase[int] = Field(description=_("u2_value"))
    supply_voltage: VoltageSensor = Field(description=_("supply_voltage"))
    voltage_0_10: SensorBase[int] = Field(description=_("voltage_0_10"))
    switch_state: SensorBase[int] = Field(description=_("switch_state"))
    usb_state: SensorBase[int] = Field(description=_("usb_state"))
    radio_state: SensorWithUnit[int] = Field(description=_("radio_state"))
    ibus_receptions: SensorBase[int] = Field(description=_("ibus_receptions"))
    ibus_auxiliary: SensorBase[int] = Field(description=_("ibus_auxiliary"))
    hmi_installer: SensorBase[int] = Field(description=_("hmi_installer"))
    hmi_user: SensorBase[int] = Field(description=_("hmi_user"))
    filter_condition: SensorBase[int] = Field(description=_("filter_condition"))
    filter_condition_time: SensorBase[int] = Field(
        description=_("filter_condition_time")
    )
    bypass_position: BypassPosition = Field(description=_("bypass_position"))
    bypass_consumption: SensorBase[int] = Field(description=_("bypass_consumption"))
    outdoor_air_temperature: TemperaturSensor = Field(
        description=_("outdoor_air_temperature")
    )
    indoor_air_temperature: TemperaturSensor = Field(
        description=_("indoor_air_temperature")
    )
    error_code: SensorWithUnit[int] = Field(description=_("error_code"))
    error_code_2: SensorWithUnit[int] = Field(description=_("error_code_2"))

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
