import asyncio
import json
from websockets import WebSocketServerProtocol
from ..block.core import Block
from ..blockchain.core import Blockchain

nodes = set()


class Node:
    global nodes

    def __init__(self):
        self.private_key = None
        self.nodes = nodes
        Block().view()

    def view(self):
        return len(self.nodes)

    async def notify(self, message: str, ignore=None) -> None:
        if self.nodes:
            if ignore is not None:
                n = self.nodes.copy()
                n.remove(ignore)
                await asyncio.wait([node.send(message) for node in n])
            else:
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

    async def ws_handler(self, node: WebSocketServerProtocol, uri: str) -> None:
        await self.register(node)
        try:
            _dir = {
                'h': {
                    'n': 'Ripda Core',
                    'v': '1.0.0.dev1',
                }
            }
            await node.send(json.dumps(_dir))
            async for message in node:
                try:
                    receiver = json.loads(message)
                    """
                    receiver = {
                        'm': 'module: str',
                        'f': 'function: str',
                        'd': 'data: object'
                    }
                    """
                    if 'm' and 'f' and 'd' in receiver:
                        if receiver['m'] == 'block':
                            callback = await self.block(receiver, node)
                            await node.send(callback)
                        if receiver['m'] == 'blockchain':
                            callback = await self.blockchain(receiver, node)
                            await node.send(callback)
                        if receiver['m'] == 'transaction':
                            callback = await self.transaction(receiver, node)
                            await node.send(callback)
                except:
                    pass
        finally:
            await self.unregister(node)

    async def sender(self, m, f, r=None, e=None, d=None):
        """
        sender = {
            'm': 'module: str',
            'f': 'function: str',
            'r': 'return: object',
            'e': 'error: str'
            'd': 'return: object',
        }
        """
        if e is None:
            if r is None:
                sender = {
                    'm': m,
                    'f': f,
                    'd': d,
                }
            else:
                sender = {
                    'm': m,
                    'f': f,
                    'r': r,
                }
        else:
            sender = {
                'm': m,
                'f': f,
                'e': e,
            }
        return json.dumps(sender)

    async def transaction(self, receiver, node):
        if receiver['f'] == 'create':
            sender = {
                'm': 'transaction',
                'f': 'create',
                'd': receiver['d'],
            }
            await self.notify(message=json.dumps(sender), ignore=node)
            return True

    async def block(self, receiver, node):
        if receiver['f'] == 'view':
            return await self.sender(m='block', f='view', r=Block().view())
        if receiver['f'] == 'is_hash_valid':
            if 'hash' in receiver['d']:
                if Block().is_hash_valid(receiver['d']['hash']):
                    return await self.sender(m='block', f='is_hash_valid', r='True')
                else:
                    return await self.sender(m='block', f='is_hash_valid', r='False')
            return await self.sender(m='block', f='is_hash_valid', e='Parâmetros incompletos para usar esta função')
        return await self.sender(m='block', f=receiver['f'], e='Não foi possível identificar o comando')

    async def blockchain(self, receiver, node):
        if receiver['f'] == 'view':
            return await self.sender(m='blockchain', f='view', r=Blockchain().view())
        if receiver['f'] == 'add_block':
            add_block = Blockchain().add_block(
                block=receiver['d']
            )
            if not add_block:
                r = await self.sender(m='blockchain', f='add_block', e='Bloco não pôde ser adicionado')
                return r
            r = await self.sender(m='blockchain', f='add_block', d=add_block)
            await self.notify(message=r, ignore=node)
            return r
        return await self.sender(m='blockchain', f=receiver['f'], e='Não foi possível identificar o comando')
