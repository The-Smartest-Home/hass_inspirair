import unittest

from pymodbus.client.mixin import ModbusClientMixin
from pymodbus.pdu import ModbusRequest

from ha_aldes.modbus.client import poll_values


class MockClient(ModbusClientMixin):
    def execute(self, request: ModbusRequest) -> ModbusRequest:
        request.registers = [1] * 100
        return request


class ModbusPollTest(unittest.TestCase):
    def test_poll(self) -> None:
        client = MockClient()
        expected_json = {
            "id": "65537",
            "serial_id": "281479271743489",
            "sw_version": "256",
            "regulation_mode": "Hygro",
            "fan_mode": "Standard",
            "night_cooling": 1,
            "bypass_exchanger": "Auto",
            "regulation_system": "Separated Airflows",
            "holiday_time": 256,
            "kitchen_time": 256,
            "boost_time": 256,
            "filter_time": 256,
            "aux_time_1": 256,
            "aux_time_2": 256,
            "extract_airflow": 256,
            "supply_airflow": 256,
            "extract_pressure": 256,
            "supply_pressure": 256,
            "extract_speed": 256,
            "supply_speed": 256,
            "extract_supply_ratio": 256,
            "temperature_summer_comfort": 1.0,
            "u1_value": 1,
            "u2_value": 1,
            "supply_voltage": 1,
            "voltage_0_10": 1,
            "switch_state": 1,
            "usb_state": 1,
            "radio_state": 1,
            "ibus_receptions": 1,
            "ibus_auxiliary": 1,
            "hmi_installer": 1,
            "hmi_user": 1,
            "filter_condition": 1,
            "filter_condition_time": 1,
            "bypass_position": "Offen",
            "bypass_consumption": 1,
            "outdoor_air_temperature": 0.01,
            "indoor_air_temperature": 0.01,
            "error_code": 1,
            "error_code_2": 256,
        }

        expected = {
            "id": {
                "value": "65537",
                "category": "diagnostic",
                "name": "GeräteID",
                "id": "id",
            },
            "serial_id": {
                "value": "281479271743489",
                "category": "diagnostic",
                "name": "Seriennummer",
                "id": "serial_id",
            },
            "sw_version": {
                "value": "256",
                "category": "diagnostic",
                "name": "Software Version",
                "id": "sw_version",
            },
            "regulation_mode": {
                "value": 1,
                "category": "diagnostic",
                "name": "Regelart",
                "id": "regulation_mode",
                "options": {0: "Auto", 1: "Hygro", 2: "Constant Speed"},
            },
            "fan_mode": {
                "value": 1,
                "category": "diagnostic",
                "name": "Lüfter Modus",
                "id": "fan_mode",
                "options": {0: "Ferien", 1: "Standard", 2: "Boost", 3: "Gäste"},
            },
            "night_cooling": {
                "value": 1,
                "category": "diagnostic",
                "name": "Nachtkühlung",
                "id": "night_cooling",
            },
            "bypass_exchanger": {
                "value": 1,
                "category": "diagnostic",
                "name": "Beipass Management",
                "id": "bypass_exchanger",
                "options": {0: "Aus", 1: "Auto", 2: "Winter", 3: "Sommer", 4: "Offen"},
            },
            "regulation_system": {
                "value": 1,
                "category": "diagnostic",
                "name": "Regelsystem",
                "id": "regulation_system",
                "options": {
                    0: "Separated Speeds",
                    1: "Separated Airflows",
                    2: "Separated Pressures",
                    3: "Adjusted Pressure",
                },
            },
            "holiday_time": {
                "value": 256,
                "category": "diagnostic",
                "name": "Ferienmodus Zeit",
                "id": "holiday_time",
                "unit": "min",
            },
            "kitchen_time": {
                "value": 256,
                "category": "diagnostic",
                "name": "Kochenmodus Zeit",
                "id": "kitchen_time",
                "unit": "min",
            },
            "boost_time": {
                "value": 256,
                "category": "diagnostic",
                "name": "Boostmodus Zeit",
                "id": "boost_time",
                "unit": "min",
            },
            "filter_time": {
                "value": 256,
                "category": "diagnostic",
                "name": "Filter Zeit",
                "id": "filter_time",
            },
            "aux_time_1": {
                "value": 256,
                "category": "diagnostic",
                "name": "Aux1 Zeit",
                "id": "aux_time_1",
            },
            "aux_time_2": {
                "value": 256,
                "category": "diagnostic",
                "name": "Aux2 Zeit",
                "id": "aux_time_2",
            },
            "extract_airflow": {
                "value": 256,
                "category": "diagnostic",
                "name": "Abluft Durchfluss",
                "id": "extract_airflow",
                "unit": "m³/h",
            },
            "supply_airflow": {
                "value": 256,
                "category": "diagnostic",
                "name": "Zuluft Durchfluss",
                "id": "supply_airflow",
                "unit": "m³/h",
            },
            "extract_pressure": {
                "value": 256,
                "category": "diagnostic",
                "name": "Abluft Druck",
                "id": "extract_pressure",
                "unit": "Pa",
            },
            "supply_pressure": {
                "value": 256,
                "category": "diagnostic",
                "name": "Zuluft Durchfluss",
                "id": "supply_pressure",
                "unit": "Pa",
            },
            "extract_speed": {
                "value": 256,
                "category": "diagnostic",
                "name": "Abluft Geschwindigkeit",
                "id": "extract_speed",
                "unit": "m/s",
            },
            "supply_speed": {
                "value": 256,
                "category": "diagnostic",
                "name": "Zuluft Geschwindigkeit",
                "id": "supply_speed",
                "unit": "m/s",
            },
            "extract_supply_ratio": {
                "value": 256,
                "category": "diagnostic",
                "name": "Zuluft/Abluft Balance",
                "id": "extract_supply_ratio",
            },
            "temperature_summer_comfort": {
                "value": 1.0,
                "category": "diagnostic",
                "name": "Sommer Komforttemperatur",
                "id": "temperature_summer_comfort",
                "unit": "°C",
            },
            "u1_value": {
                "value": 1,
                "category": "diagnostic",
                "name": "U1",
                "id": "u1_value",
            },
            "u2_value": {
                "value": 1,
                "category": "diagnostic",
                "name": "U2",
                "id": "u2_value",
            },
            "supply_voltage": {
                "value": 1,
                "category": "diagnostic",
                "name": "Spannung",
                "id": "supply_voltage",
                "unit": "V",
            },
            "voltage_0_10": {
                "value": 1,
                "category": "diagnostic",
                "name": "Spannung 10V",
                "id": "voltage_0_10",
            },
            "switch_state": {
                "value": 1,
                "category": "diagnostic",
                "name": "Schalter Status",
                "id": "switch_state",
            },
            "usb_state": {
                "value": 1,
                "category": "diagnostic",
                "name": "USH Status",
                "id": "usb_state",
            },
            "radio_state": {
                "value": 1,
                "category": "diagnostic",
                "name": "Radio Status",
                "id": "radio_state",
                "unit": "",
            },
            "ibus_receptions": {
                "value": 1,
                "category": "diagnostic",
                "name": "ibus_receptions",
                "id": "ibus_receptions",
            },
            "ibus_auxiliary": {
                "value": 1,
                "category": "diagnostic",
                "name": "Anzahl Ibus",
                "id": "ibus_auxiliary",
            },
            "hmi_installer": {
                "value": 1,
                "category": "diagnostic",
                "name": "Installateur HMI",
                "id": "hmi_installer",
            },
            "hmi_user": {
                "value": 1,
                "category": "diagnostic",
                "name": "Benutzer HMI",
                "id": "hmi_user",
            },
            "filter_condition": {
                "value": 1,
                "category": "diagnostic",
                "name": "Filter Zustand",
                "id": "filter_condition",
            },
            "filter_condition_time": {
                "value": 1,
                "category": "diagnostic",
                "name": "Filter Zustand Zeit",
                "id": "filter_condition_time",
            },
            "bypass_position": {
                "value": 1,
                "category": "diagnostic",
                "name": "Beipass Position",
                "id": "bypass_position",
                "options": {
                    0: "Close",
                    1: "Offen",
                    2: "Closing",
                    3: "Opening",
                    4: "Short circuit",
                    5: "Open circuit",
                    6: "Under supply",
                },
            },
            "bypass_consumption": {
                "value": 1,
                "category": "diagnostic",
                "name": "Beipass Verbrauch",
                "id": "bypass_consumption",
            },
            "outdoor_air_temperature": {
                "value": 0.01,
                "category": "diagnostic",
                "name": "Außenluft Temperatur",
                "id": "outdoor_air_temperature",
                "unit": "°C",
            },
            "indoor_air_temperature": {
                "value": 0.01,
                "category": "diagnostic",
                "name": "Innenluft Temperatur",
                "id": "indoor_air_temperature",
                "unit": "°C",
            },
            "error_code": {
                "value": 1,
                "category": "diagnostic",
                "name": "Fehlercode 1",
                "id": "error_code",
                "unit": "",
            },
            "error_code_2": {
                "value": 256,
                "category": "diagnostic",
                "name": "Fehlercode 2",
                "id": "error_code_2",
                "unit": "",
            },
        }

        poll = poll_values(client)

        self.assertDictEqual(poll.model_dump(), expected)
        self.assertDictEqual(poll.model_dump(mode="json"), expected_json)
