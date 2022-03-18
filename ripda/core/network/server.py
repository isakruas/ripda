import asyncio
from websockets import WebSocketServerProtocol
from abc import abstractmethod

from ripda.manages.factory import Factory


class Server(Factory):
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

    async def callback(self, socket: WebSocketServerProtocol, receiver: str) -> str:
        return f'callback {receiver}'

    @abstractmethod
    async def handler(self, socket: WebSocketServerProtocol, uri: str) -> None:
        pass
