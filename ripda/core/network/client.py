import asyncio
from websockets import WebSocketServerProtocol
from abc import abstractmethod

from ripda.manages.factory import Factory


class Client(Factory):
    def __init__(self) -> None:
        self.__connect = None

    async def notify(self, message: dict) -> bool:
        while self.__connect is None:
            await asyncio.sleep(0.5)
        try:
            await self.__connect.send(message)
            return True
        except:
            return False

    async def register(self, connect: WebSocketServerProtocol) -> None:
        self.__connect = connect

    async def unregister(self, connect: WebSocketServerProtocol) -> None:
        self.__connect = None

    @abstractmethod
    async def handler(self, recv) -> None:
        pass


