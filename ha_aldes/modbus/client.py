import pymodbus.client as ModbusClient
from pymodbus import Framer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from ha_aldes.modbus.model import AldesModbusResponse


def get_client(port: str = "5020", framer: Framer = Framer.SOCKET) -> ModbusClient:
    return ModbusClient.AsyncModbusSerialClient(
        port,
        framer=framer,
        baudrate=115200,
        bytesize=8,
        parity="E",
        stopbits=1,
    )


def poll_values(client: ModbusClient) -> AldesModbusResponse:
    decoder_1 = BinaryPayloadDecoder.fromRegisters(
        client.read_holding_registers(1, 12, 2).registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )
    decoder_2 = BinaryPayloadDecoder.fromRegisters(
        client.read_holding_registers(256, 44, 2).registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )
    decoder_3 = BinaryPayloadDecoder.fromRegisters(
        client.read_holding_registers(337, 63, 2).registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )

    return AldesModbusResponse(
        **{
            k: v
            for k, v in [
                ("id", decoder_1.decode_32bit_uint()),  # 1-2
                ("serial_id", decoder_1.decode_64bit_uint()),  # 3-6;
                (None, decoder_1.skip_bytes(5)),  # 7-11
                ("sw_version", decoder_1.decode_16bit_uint()),  # 12
                (
                    "regulation_mode",
                    decoder_2.decode_16bit_uint(),
                ),  # 256
                ("fan_mode", decoder_2.decode_16bit_uint()),  # 257
                ("night_cooling", decoder_2.decode_16bit_int()),  # 258
                (
                    "bypass_exchanger",
                    decoder_2.decode_16bit_uint(),
                ),  # 259
                (
                    "regulation_system",
                    decoder_2.decode_16bit_uint(),
                ),  # 260
                (None, decoder_2.skip_bytes(3)),  # 261-263
                ("holiday_time", decoder_2.decode_16bit_int()),  # 264
                ("kitchen_time", decoder_2.decode_16bit_int()),  # 265
                ("boost_time", decoder_2.decode_16bit_int()),  # 266
                ("filter_time", decoder_2.decode_16bit_int()),  # 267
                ("aux_time_1", decoder_2.decode_16bit_int()),  # 268 TODO validate value
                ("aux_time_2", decoder_2.decode_16bit_int()),  # 269 TODO validate value
                (None, decoder_2.skip_bytes(2)),  # 270-271
                ("extract_airflow", decoder_2.decode_16bit_int()),  # 272
                ("supply_airflow", decoder_2.decode_16bit_int()),  # 273
                ("extract_pressure", decoder_2.decode_16bit_int()),  # 274
                ("supply_pressure", decoder_2.decode_16bit_int()),  # 275
                ("extract_speed", decoder_2.decode_16bit_int()),  # 276
                ("supply_speed", decoder_2.decode_16bit_int()),  # 277
                ("extract_supply_ratio", decoder_2.decode_16bit_int()),  # 278
                (None, decoder_2.skip_bytes(3)),  # 279-281
                ("temperature_summer_comfort", decoder_2.decode_16bit_int()),  # 282
                ("u1_value", decoder_2.decode_16bit_int()),  # 284
                ("u2_value", decoder_2.decode_16bit_int()),  # 285
                ("supply_voltage", decoder_3.decode_16bit_uint()),  # 337
                ("voltage_0_10", decoder_3.decode_16bit_uint()),  # 338
                ("switch_state", decoder_3.decode_16bit_uint()),  # 339
                ("usb_state", decoder_3.decode_16bit_uint()),  # 340
                ("radio_state", decoder_3.decode_16bit_uint()),  # 341
                ("ibus_receptions", decoder_3.decode_16bit_uint()),  # 342
                ("ibus_auxiliary", decoder_3.decode_16bit_uint()),  # 343
                ("hmi_installer", decoder_3.decode_16bit_uint()),  # 344
                ("hmi_user", decoder_3.decode_16bit_uint()),  # 345
                ("filter_condition", decoder_3.decode_16bit_uint()),  # 346
                ("filter_condition_time", decoder_3.decode_16bit_uint()),  # 347
                (
                    "bypass_position",
                    decoder_3.decode_16bit_uint(),
                ),  # 348
                ("bypass_consumption", decoder_3.decode_16bit_uint()),  # 349
                (
                    "outdoor_air_temperature",
                    decoder_3.decode_16bit_uint() * 0.01,
                ),  # 350
                ("indoor_air_temperature", decoder_3.decode_16bit_uint() * 0.01),  # 351
                (None, decoder_3.skip_bytes(32)),  # 352-383
                ("error_code", decoder_3.decode_16bit_uint()),  # 384
                (None, decoder_3.skip_bytes(7)),  # 385-391
                ("error_code_2", decoder_3.decode_16bit_uint()),  # 392
            ]
            if k is not None
        }
    )
