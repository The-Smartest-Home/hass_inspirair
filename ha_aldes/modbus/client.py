import asyncio
import importlib
import logging
from typing import Awaitable, Callable, Optional

import pymodbus.client as ModbusClient
from aiomqtt import Client
from pymodbus import Framer
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.client.base import ModbusBaseClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.pdu import ModbusResponse

from ha_aldes.config import DEFAULT_CONFIG, Config
from ha_aldes.env_config import EnvConfig
from ha_aldes.modbus.model import AldesModbusResponse, fan_mode_mapping
from ha_aldes.mqtt.client import publish

logger = logging.getLogger(__name__)


def get_async_serial_client(framer: Framer = Framer.SOCKET) -> ModbusClient:
    return ModbusClient.AsyncModbusSerialClient(
        framer=framer,
        port=EnvConfig.HA_ALDES_MODBUS_SERIAL_DEVICE,
        baudrate=115200,
        bytesize=8,
        parity="E",
        stopbits=1,
    )


def get_async_tcp_client(framer: Framer = Framer.SOCKET) -> ModbusClient:
    return AsyncModbusTcpClient(
        EnvConfig.HA_ALDES_MODBUS_TCP_HOST,
        port=EnvConfig.HA_ALDES_MODBUS_TCP_PORT,
    )


async def get_async_client() -> ModbusClient:
    try:
        _module_name, _function = DEFAULT_CONFIG.modbus.client.rsplit(".", 1)
        _module = importlib.import_module(_module_name)
        _get_client = getattr(_module, _function)
        return _get_client()
    except ModuleNotFoundError as e:
        logger.exception("Could create client", e)
        logger.warning("Will use default serial client")
    return get_async_serial_client()


WORD_SIZE = 2


async def change_fan_mode(mode: int, modbus_client: ModbusClient) -> bool:
    if mode in fan_mode_mapping:
        try:
            logger.debug(f"writing to register= 257 value = {mode}")
            request: ModbusResponse = await modbus_client.write_register(257, mode, 2)
            if request.isError():
                raise RuntimeError("Could not wirte to register 257")
            return True
        except ModbusIOException as e:
            raise RuntimeError from e

    logger.error(f"Tried to set unknown fan mode {mode}")
    return False


async def poll_values(modbus_client: ModbusClient) -> AldesModbusResponse:
    logger.debug("polling values...")
    try:
        request1: ModbusResponse = await modbus_client.read_holding_registers(1, 12, 2)
        if request1.isError():
            raise RuntimeError("Register 1-12 could not be read.")
        request2 = await modbus_client.read_holding_registers(256, 30, 2)
        if request2.isError():
            raise RuntimeError("Register 256-286 could not be read.")
        request3 = await modbus_client.read_holding_registers(337, 56, 2)
        if request3.isError():
            raise RuntimeError("Register 337-392 could not be read.")
    except ModbusIOException as e:
        raise RuntimeError from e
    decoder_1 = BinaryPayloadDecoder.fromRegisters(
        request1.registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )
    decoder_2 = BinaryPayloadDecoder.fromRegisters(
        request2.registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )
    decoder_3 = BinaryPayloadDecoder.fromRegisters(
        request3.registers,
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
    )

    logger.debug("decoding values...")

    response = AldesModbusResponse(
        **{
            k: v
            for k, v in [
                ("id", str(decoder_1.decode_32bit_uint())),  # 1-2
                ("serial_id", str(decoder_1.decode_64bit_uint())),  # 3-6;
                (None, decoder_1.skip_bytes(5 * WORD_SIZE)),  # 7-11
                ("sw_version", str(decoder_1.decode_16bit_uint())),  # 12
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
                (None, decoder_2.skip_bytes(3 * WORD_SIZE)),  # 261-263
                ("holiday_time", decoder_2.decode_16bit_int()),  # 264
                ("kitchen_time", decoder_2.decode_16bit_int()),  # 265
                ("boost_time", decoder_2.decode_16bit_int()),  # 266
                ("filter_time", decoder_2.decode_16bit_int()),  # 267
                ("aux_time_1", decoder_2.decode_16bit_int()),  # 268 TODO validate value
                ("aux_time_2", decoder_2.decode_16bit_int()),  # 269 TODO validate value
                (None, decoder_2.skip_bytes(2 * WORD_SIZE)),  # 270-271
                ("extract_airflow", decoder_2.decode_16bit_int()),  # 272
                ("supply_airflow", decoder_2.decode_16bit_int()),  # 273
                ("extract_pressure", decoder_2.decode_16bit_int()),  # 274
                ("supply_pressure", decoder_2.decode_16bit_int()),  # 275
                ("extract_speed", decoder_2.decode_16bit_int()),  # 276
                ("supply_speed", decoder_2.decode_16bit_int()),  # 277
                ("extract_supply_ratio", decoder_2.decode_16bit_int()),  # 278
                (None, decoder_2.skip_bytes(3 * WORD_SIZE)),  # 279-281
                ("temperature_summer_comfort", decoder_2.decode_16bit_int()),  # 282
                (None, decoder_2.skip_bytes(1 * WORD_SIZE)),  # 283
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
                    round(decoder_3.decode_16bit_uint() * 0.01, 2),
                ),  # 350
                (
                    "indoor_air_temperature",
                    round(decoder_3.decode_16bit_uint() * 0.01, 2),
                ),  # 351
                (None, decoder_3.skip_bytes(32 * WORD_SIZE)),  # 352-383
                ("error_code", decoder_3.decode_16bit_uint()),  # 384
                (None, decoder_3.skip_bytes(7 * WORD_SIZE)),  # 385-391
                ("error_code_2", decoder_3.decode_16bit_uint()),  # 392
            ]
            if k is not None
        }
    )
    return response


async def poll_push(
    modbus_client: ModbusBaseClient,
    mqtt_client: Client,
    callback: Callable[[str, str, Optional[Client]], Awaitable[None]] = publish,
) -> AldesModbusResponse:
    config = Config()
    response = await poll_values(modbus_client)
    topic = config.get_state_topic(response.serial_id.value)
    await callback(topic, response.model_dump_json(), mqtt_client)
    return response


# TODO Configurable interval
async def modbus_polling_loop(
    modbus_client: ModbusBaseClient,
    mqtt_client: Client,
    callback: Callable[[str, str, Optional[Client]], Awaitable[None]] = publish,
    interval: int = DEFAULT_CONFIG.modbus.polling_intervall,
) -> None:
    logger.info("starting modbus loop")
    while True:
        await poll_push(modbus_client, mqtt_client, callback)
        await asyncio.sleep(interval)
