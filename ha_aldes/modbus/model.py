from collections import namedtuple

from ha_aldes.i18n import _

AldesModbusResponse = namedtuple(
    "AldesModbusResponse",
    "id, serial_id, sw_version, regulation_mode, fan_mode, night_cooling, "
    "bypass_exchanger, regulation_system, holiday_time, kitchen_time, boost_time, "
    "filter_time, aux_time_1, aux_time_2, extract_airflow, supply_airflow, "
    "extract_pressure, supply_pressure, extract_speed, supply_speed, "
    "extract_supply_ratio, temperature_summer_comfort, u1_value, u2_value, "
    "supply_voltage, voltage_0_10, switch_state, usb_state, radio_state, "
    "ibus_receptions, ibus_auxiliary, hmi_installer, hmi_user, filter_condition, "
    "filter_condition_time, bypass_position, bypass_consumption, "
    "outdoor_air_temperature, indoor_air_temperature, error_code, error_code_2",
)

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
