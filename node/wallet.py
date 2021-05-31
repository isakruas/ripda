import asyncio
import json
import websockets
from websockets import WebSocketServerProtocol
from wallet.core import Wallet
from websocket import create_connection
node_wallets = set()


class NodeWallet:
    global node_wallets

    def __init__(self):
        self.private_key = None
        self.nodes = node_wallets

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
                    'n': 'Ripda Wallet',
                    'v': '1.0-beta.1',
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
                        if receiver['m'] == 'wallet':
                            callback = await self.wallet(receiver, node)
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

    async def wallet(self, receiver, node):
        if receiver['f'] == 'create_wallet':
            if 'email' and 'password' in receiver['d']:
                process = Wallet().create_wallet(
                    email=receiver['d']['email'],
                    password=receiver['d']['password']
                )
                _wallet = {
                    'private_key': process['private_key'].hex(),
                    'public_key': process['public_key'],
                    'wallet': process['wallet']
                }
                r = await self.sender(m='wallet', f='create_wallet', r=_wallet)
                return r
            else:
                process = Wallet().create_wallet()
                _wallet = {
                    'private_key': process['private_key'].hex(),
                    'public_key': process['public_key'],
                    'wallet': process['wallet']
                }
                r = await self.sender(m='wallet', f='create_wallet', r=_wallet)
                return r

        if receiver['f'] == 'create_transaction':
            if 'private_key' and 'receiver' and 'amount' in receiver['d']:
                try:
                    wallet = Wallet(private_key=bytes.fromhex(str(receiver['d']['private_key'])))
                    create_transaction = wallet.create_transaction(
                        receiver=receiver['d']['receiver'],
                        amount=receiver['d']['amount']
                    )
                    if create_transaction is False:
                        """
                           Não foi possível criar transação
                        """
                        r = await self.sender(m='wallet', f='create_transaction', e='Não foi possível criar transação')
                        await self.notify(message=r)
                        return False
                    else:
                        sender = {
                            'm': 'transaction',
                            'f': 'create',
                            'd': create_transaction,
                        }
                        uri = 'ws://localhost:1140'
                        async with websockets.connect(uri) as n:
                            await n.send(json.dumps(sender))
                        r = await self.sender(m='wallet', f='create_transaction', r=create_transaction)
                        await self.notify(message=r)
                        return True
                except:
                    return False
            return await self.sender(m='wallet', f='create_transaction', e='Dados incompletos para realizar a transação')
        return await self.sender(m='wallet', f=receiver['f'], e='Não foi possível identificar o comando')
