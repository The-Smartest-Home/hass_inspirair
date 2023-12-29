import unittest

from ha_aldes.ha.devices import create_all
from ha_aldes.modbus.model import AldesModbusResponse, regulation_mode_mapping


class ModelTestCase(unittest.TestCase):
    def test_serialization(self) -> None:
        raw_data = {
            **{k: 1 for k, v in AldesModbusResponse.model_fields.items()},
            "id": "id_value",
            "serial_id": "serial_id_value",
            "sw_version": "sw_version_value",
        }
        expected_data = {
            **{k: 1 for k, v in AldesModbusResponse.model_fields.items()},
            "id": "id_value",
            "serial_id": "serial_id_value",
            "sw_version": "sw_version_value",
            "bypass_position": "Offen",
            "bypass_exchanger": "Auto",
            "fan_mode": "Standard",
            "regulation_mode": "Hygro",
            "regulation_system": "Separated Airflows",
        }
        response = AldesModbusResponse(**raw_data)

        self.assertEqual(response.regulation_mode.options, regulation_mode_mapping)
        self.assertEqual(str(response.fan_mode.id), "fan_mode")
        self.assertDictEqual(expected_data, response.model_dump(mode="json"))
        stuff = list(create_all(response))
        self.assertEqual(22, len(stuff))
