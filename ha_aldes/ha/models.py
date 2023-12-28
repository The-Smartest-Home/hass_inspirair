from collections import namedtuple
from ha_aldes.i18n import _

Sensor = namedtuple("Sensor", "name, id, unit, category")
Select = namedtuple("Select", "name, id, options, category")
Device = namedtuple(
    "Device",
    "manufacturer, model, discovery_prefix, entity_name",
)
Topics = namedtuple("Topics", "state, id,fan_mode")

selects = [
    {
        "name": _("regulation_mode"),
        "id": "regulation_mode",
        "options": [_("Auto"), _("Hygro"), _("Constant Speed")],
        "category": "diagnostic",
    },
    {
        "name": _("Bypass Exchanger Management"),
        "id": "bypass_exchanger",
        "options": [
            _("Off"),
            _("Auto"),
            _("Winter optimisation"),
            _("Summer optimisation"),
            _("Open"),
        ],
        "category": "diagnostic",
    },
    {
        "name": _("Regulation system"),
        "id": "regulation_system",
        "options": [
            _("Separated Speeds"),
            _("Separated Airflows"),
            _("Separated Pressures"),
            _("Adjusted Pressure"),
        ],
        "category": "diagnostic",
    },
    {
        "name": _("Bypass Position"),
        "id": "bypass_position",
        "category": "diagnostic",
        "options": [
            _("Close"),
            _("Open"),
            _("Closing"),
            _("Opening"),
            _("Short circuit"),
            _("Open circuit"),
            _("Under supply"),
        ],
    },
]

sensors = [
    {
        "name": _("outdoor_air_temperature"),
        "id": "outdoor_air_temperature",
        "unit": "°C",
        "category": "diagnostic",
    },
    {
        "name": _("indoor_air_temperature"),
        "id": "indoor_air_temperature",
        "unit": "°C",
        "category": "diagnostic",
    },
    {
        "name": _("supply_voltage"),
        "id": "supply_voltage",
        "unit": "V",
        "category": "diagnostic",
    },
    {
        "name": _("extract_airflow"),
        "id": "extract_airflow",
        "unit": "m³/h",
        "category": "diagnostic",
    },
    {
        "name": _("supply_airflow"),
        "id": "supply_airflow",
        "unit": "m³/h",
        "category": "diagnostic",
    },
    {
        "name": _("extract_pressure"),
        "id": "extract_pressure",
        "unit": "Pa",
        "category": "diagnostic",
    },
    {
        "name": _("supply_pressure"),
        "id": "supply_pressure",
        "unit": "Pa",
        "category": "diagnostic",
    },
    {
        "name": _("extract_speed"),
        "id": "extract_speed",
        "unit": "m/s",
        "category": "diagnostic",
    },
    {
        "name": _("supply_speed"),
        "id": "supply_speed",
        "unit": "m/s",
        "category": "diagnostic",
    },
    {
        "name": _("extract_supply_ratio"),
        "id": "extract_supply_ratio",
        "unit": None,
        "category": "diagnostic",
    },
    {
        "name": _("temperature_summer_comfort"),
        "id": "temperature_summer_comfort",
        "unit": "°C",
        "category": "diagnostic",
    },
    {
        "name": _("holiday_time"),
        "id": "holiday_time",
        "unit": "min",
        "category": "diagnostic",
    },
    {
        "name": _("kitchen_time"),
        "id": "kitchen_time",
        "unit": "min",
        "category": "diagnostic",
    },
    {
        "name": _("boost_time"),
        "id": "boost_time",
        "unit": "min",
        "category": "diagnostic",
    },
    {
        "name": _("error_code"),
        "id": "error_code",
        "unit": None,
        "category": "diagnostic",
    },
    {
        "name": _("error_code_2"),
        "id": "error_code_2",
        "unit": None,
        "category": "diagnostic",
    },
]
