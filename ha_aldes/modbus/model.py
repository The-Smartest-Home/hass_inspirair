from ha_aldes.i18n import _

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
    2: _("Separated Preasures"),
    3: _("Adjusted Pressure"),
}

byte_mappings = {
    "night_cooling": 258,
    "holiday_time": 264,
    "kitchen_time": 265,
    "boost_time": 266,
    "filter_time": 267,
    "extract_airflow": 272,
    "supply_airflow": 273,
    "extract_pressure": 274,
    "supply_pressure": 275,
    "extract_speed": 276,
    "supply_speed": 277,
    "extract_supply_ratio": 278,
    "temperature_summer_comfort": 282,
    "u1_value": 284,
    "u2_value": 285,
}
