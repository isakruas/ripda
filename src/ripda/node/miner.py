import asyncio
import json
from websockets import WebSocketServerProtocol
from ..miner.core import Miner

node_miners = set()


class NodeMiner:
    global node_miners

    def __init__(self):
        self.private_key = None
        self.nodes = node_miners

    async def notify(self, message: str) -> None:
        if self.nodes:
            await asyncio.wait([node.send(message) for node in self.nodes])

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.nodes.add(ws)
        """
        _notify = {
            'u': 'register'
        }
        await self.notify(json.dumps(_notify))
       """

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.nodes.remove(ws)
        """
        _notify = {
            'u': 'unregister'
        }
        await self.notify(json.dumps(_notify))
       """
    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            _dir = {
                'h': {
                    'n': 'Ripda Miner',
                    'v': '1.0.0.dev2',
                }
            }
            await ws.send(json.dumps(_dir))
            async for message in ws:
                try:
                    order = json.loads(message)

                    if 'm' and 'f' and 'd' in order:
                        if order['m'] == 'miner':
                            callback = await self.forger(order)
                            await ws.send(callback)
                except:
                    pass
        finally:
            await self.unregister(ws)

    async def forger(self, order):
        if order['f'] == 'forger':
            if 'wallet' and 'block' in order['d']:
                forger = Miner(
                    wallet=order['d']['wallet'],
                    block=order['d']['block'],
                ).ripda()
                print(forger)

        _notify = {
            'e': 'Não foi possível identificar o comando'
        }
        return json.dumps(_notify)
