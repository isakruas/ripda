import asyncio
import json
from websockets import WebSocketServerProtocol
from abc import ABCMeta, abstractclassmethod


class Factory(metaclass=ABCMeta):
    pass


class FACClient(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.__connect = None

    async def notify(self, message: dict) -> bool:
        while self.__connect is None:
            await asyncio.sleep(0.5)
        try:
            await self.__connect.send(json.dumps(message))
            return True
        except:
            return False

    async def register(self, connect: WebSocketServerProtocol) -> None:
        self.__connect = connect

    async def unregister(self, connect: WebSocketServerProtocol) -> None:
        self.__connect = None

    @abstractclassmethod
    async def handler(self, recv) -> None:
        pass


class FACServer(metaclass=ABCMeta):

    sockets = set()

    async def notify(self: object, message: str, ignore: WebSocketServerProtocol = None) -> None:
        if len(self.sockets) >> 0:
            if ignore is not None:
                try:
                    await asyncio.wait([socket.send(message) for socket in self.sockets if socket != ignore])
                except ValueError:
                    pass
            else:
                await asyncio.wait([socket.send(message) for socket in self.sockets])

    async def register(self, socket: WebSocketServerProtocol) -> None:
        self.sockets.add(socket)

    async def unregister(self, socket: WebSocketServerProtocol) -> None:
        self.sockets.remove(socket)

    @abstractclassmethod
    async def handler(self, socket: WebSocketServerProtocol, uri: str) -> None:
        pass
