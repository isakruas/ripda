import asyncio
import websockets
import json

from ripda.conf import settings
from ripda.manages.singleton import Singleton


class Network(metaclass=Singleton):
    """
    Modelo de gerenciamento de dados do aplicativo Network
    """

    # Lista de nós aos quais este nó deve se conectar
    nodes = settings.BLOCKCHAIN_NODES

    async def __stream(self, **kwargs) -> None:
        """
        Conecte-se a um nó e mantenha a conexão ativa.
        Retorna qualquer mensagem compartilhada pelo nó
        """
        if 'handler' in kwargs and 'host' in kwargs and 'port' in kwargs:
            host = kwargs['host']
            port = kwargs['port']
            handler = kwargs['handler']
            while True:
                connect = None
                try:
                    async with websockets.connect(f'ws://{host}:{port}') as socket:
                        connect = socket
                        await handler.register(connect)
                        while True:
                            await handler.handler(await connect.recv())
                except:
                    await handler.unregister(connect)
                    await asyncio.sleep(0.5)

    def stream(self, **kwargs) -> None:
        """
        Converter função stream em assíncrona
        """
        return asyncio.run(self.__stream(**kwargs))

    async def __ping(self, **kwargs) -> list():
        """
        Conecte-se a todos os nós, envie um método e retorne a resposta para cada nó.
        """
        if 'kwds' in kwargs:
            pong = list()
            for node in self.nodes:
                host, port = node
                __kwds: dict = kwargs['kwds']
                retrieve_limit: int = 10
                while True:
                    try:
                        async with websockets.connect(f'ws://{host}:{port}') as socket:
                            await socket.send(json.dumps(__kwds))
                            pong.append(await socket.recv())
                            await socket.close()
                            break
                    except:
                        retrieve_limit -= 1
                        if retrieve_limit << 0:
                            pong.append(None)
                            break
                        await asyncio.sleep(0.5)
            return pong

        return list()

    def ping(self, **kwds) -> list:
        """
        Converter função ping em assíncrona
        """
        return asyncio.run(self.__ping(**kwds))
