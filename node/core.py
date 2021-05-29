import asyncio
import json
from websockets import WebSocketServerProtocol
from block.core import Block
from blockchain.core import Blockchain
from wallet.core import Wallet

nodes = set()

class Node:


    def __init__(self):
        self.private_key = None
        self.nodes = nodes
        Block().view()

    def view(self):
        return len(self.nodes)

    async def notify(self, message: str) -> None:
        if self.nodes:
            await asyncio.wait([node.send(message) for node in self.nodes])

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.nodes.add(ws)
        _notify = {
            'u': 'register'
        }
        await self.notify(json.dumps(_notify))

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.nodes.remove(ws)
        _notify = {
            'u': 'unregister'
        }
        await self.notify(json.dumps(_notify))

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            _dir = {
                'ripda': 'v1.0.0b'
            }
            await ws.send(json.dumps(_dir))
            async for message in ws:
                order = json.loads(message)

                if 'm' and 'f' and 'd' in order:

                    if order['m'] == 'block':
                        callback = await self.block(order)
                        await ws.send(callback)

                    if order['m'] == 'blockchain':
                        callback = await self.blockchain(order)
                        await ws.send(callback)

                    if order['m'] == 'wallet':
                        callback = await self.wallet(order)
                        await ws.send(callback)
        finally:
            await self.unregister(ws)

    async def block(self, order):
        if order['f'] == 'view':
            return json.dumps(Block().view())
        if order['f'] == 'is_hash_valid':
            if 'hash' in order['d']:
                if Block().is_hash_valid(order['d']['hash']):
                    return json.dumps({'is_hash_valid': 'True'})
                else:
                    return json.dumps({'is_hash_valid': 'False'})
            return json.dumps({'is_hash_valid': 'False'})
    async def blockchain(self, order):
        if order['f'] == 'view':
            return json.dumps(Blockchain().view())
        if order['f'] == 'add_block':
            pass

    async def wallet(self, order):
        if order['f'] == 'create_wallet':
            if 'email' and 'password' in order['d']:
                process = Wallet().create_wallet(
                    email=order['d']['email'],
                    password=order['d']['password']
                )
                _wallet = {
                    'private_key': process['private_key'].hex(),
                    'public_key': process['public_key'],
                    'wallet': process['wallet']
                }
                return json.dumps(_wallet)
            else:
                process = Wallet().create_wallet()
                _wallet = {
                    'private_key': process['private_key'].hex(),
                    'public_key': process['public_key'],
                    'wallet': process['wallet']
                }
                return json.dumps(_wallet)
            _notify = {
                'e': 'Não foi possível criar carteira'
            }
            return json.dumps(_notify)
        if order['f'] == 'open_wallet':
            if 'private_key' in order['d']:
                process = Wallet(private_key=bytes.fromhex(str(order['d']['private_key'])))
                wallet = process.view()
                _wallet = {
                    'private_key': str(wallet['private_key']),
                    'public_key': wallet['public_key'],
                    'wallet': wallet['wallet']
                }
                return json.dumps(_wallet)
            _notify = {
                'e': 'Não foi possível abrir carteira'
            }
            return json.dumps(_notify)
