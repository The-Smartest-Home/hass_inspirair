import asyncio
import importlib
import logging
from typing import AsyncGenerator, Awaitable, Callable, List, Optional

import pymodbus.client as ModbusClient
from aiomqtt import Client
from pymodbus import Framer
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.pdu import ExceptionResponse, ModbusResponse

from hass_inspirair.config import DEFAULT_CONFIG, Config
from hass_inspirair.env_config import EnvConfig
from hass_inspirair.modbus.model import AldesModbusResponse, fan_mode_mapping
from hass_inspirair.mqtt.client import publish

logger = logging.getLogger(__name__)

lock = asyncio.Lock()


def get_async_serial_client(framer: Framer = Framer.RTU) -> ModbusClient:
    return ModbusClient.AsyncModbusSerialClient(
        framer=framer,
        port=EnvConfig.HI_MODBUS_SERIAL_DEVICE,
        baudrate=115200,
        bytesize=8,
        parity="E",
        stopbits=1,
        timeout=1.5,
        reconnect_delay=500,
    )


def get_async_tcp_client(framer: Framer = Framer.SOCKET) -> ModbusClient:
    return AsyncModbusTcpClient(
        EnvConfig.HI_MODBUS_TCP_HOST,
        port=EnvConfig.HI_MODBUS_TCP_PORT,
    )


async def get_async_client() -> ModbusClient:
    try:
        _module_name, _function = DEFAULT_CONFIG.modbus.client.rsplit(".", 1)
        _module = importlib.import_module(_module_name)
        _get_client = getattr(_module, _function)
        client = _get_client()
    except ModuleNotFoundError:
        logger.exception("Could not create client")
        logger.warning("Will use default serial client")
        client = get_async_serial_client()

    return client


async def _interact_with_client(
    *actions: Callable[[ModbusClient], Awaitable[ModbusResponse]]
) -> AsyncGenerator[None, ModbusResponse]:
    async with lock:
        async with await get_async_client() as client:
            logger.debug("connecting modbus client")
            assert client.connected

            logger.debug("executing actions")
            for action in actions:
                try:
                    rr = await action(client)
                except ModbusException as exc:
                    logger.error(f"Received ModbusException({exc}) from library")
                    yield None
                if rr.isError():
                    logger.error(f"Received Modbus library error({rr})")
                    yield None
                if isinstance(rr, ExceptionResponse):
                    logger.error(f"Received Modbus library exception ({rr})")
                    yield None
                yield rr


WORD_SIZE = 2


async def change_fan_mode(mode: int) -> bool:
    if mode in fan_mode_mapping:
        async for result in _interact_with_client(
            lambda client: client.write_registers(
                257, mode, slave=EnvConfig.HI_MODBUS_SLAVE_ID
            )
        ):
            return result is not None
        return True

    logger.error(f"Tried to set unknown fan mode {mode}")
    return False


class ModbusDecodingError(Exception):
    pass


async def poll_values() -> AldesModbusResponse:
    logger.debug("polling values...")

    responses: List[Optional[ModbusResponse]] = []
    async for response in _interact_with_client(
        lambda client: client.read_holding_registers(
            1, count=12, slave=EnvConfig.HI_MODBUS_SLAVE_ID
        ),
        lambda client: client.read_holding_registers(
            256, count=30, slave=EnvConfig.HI_MODBUS_SLAVE_ID
        ),
        lambda client: client.read_holding_registers(
            337, count=56, slave=EnvConfig.HI_MODBUS_SLAVE_ID
        ),
    ):
        responses.append(response)

    request1, request2, request3 = responses

    if request1 is None:
        raise ModbusDecodingError("Register 1-12 could not be read.")
    if request2 is None:
        raise ModbusDecodingError("Register 256-286 could not be read.")
    if request3 is None:
        raise ModbusDecodingError("Register 337-392 could not be read.")
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
    mqtt_client: Client,
    callback: Callable[[str, str, Optional[Client]], Awaitable[None]] = publish,
) -> AldesModbusResponse:
    config = Config()
    response = await poll_values()
    topic = config.get_state_topic(response.serial_id.value)
    await callback(topic, response.model_dump_json(), mqtt_client)
    return response


async def modbus_polling_loop(
    mqtt_client: Client,
    callback: Callable[[str, str, Optional[Client]], Awaitable[None]] = publish,
    interval: int = DEFAULT_CONFIG.modbus.polling_intervall,
) -> None:
    logger.info("starting modbus loop")
    while True:
        try:
            await poll_push(mqtt_client, callback)
            await asyncio.sleep(interval)
        except ModbusDecodingError as e:
            logger.exception("An error while fetching modbus data occurred.", e)
