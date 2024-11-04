import asyncio
from typing import Any, Awaitable

from pymodbus.client.mixin import ModbusClientMixin
from pymodbus.pdu import ModbusPDU
from typing_extensions import Self


class MockClient(ModbusClientMixin):
    connected = True

    async def execute(
        self,
        _no_response_expected: bool,
        request: ModbusPDU,
    ) -> ModbusPDU:
        request.registers = [1] * 100
        request.isError = lambda: False
        return request

    async def connect(self) -> Self:
        return self

    def __aenter__(self) -> Self:
        return self

    def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Self:
        return self

    def __await__(self) -> Awaitable[Self]:
        async def __mock_await__() -> Self:
            await asyncio.sleep(0.1)
            return self

        return __mock_await__().__await__()  # type: ignore[return-value]


def get_client() -> MockClient:
    return MockClient()
