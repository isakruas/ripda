import asyncio
import json
import logging
import websockets
from websockets import WebSocketServerProtocol
from ripda.wallet.core import Wallet
from ripda.settings import getc
from ripda.node.utils import Utils

node_wallets = set()


class NodeWallet:
    """
        Conjunto de recursos que permitem a manipulação de carteiras entre vários dispositivos.
        A principal vantagem é que os usuários poderão criar uma carteira em um pool e realizar
        transações em outro pool.
    """
    global node_wallets

    def __init__(self):
        self.private_key = None
        self.nodes = node_wallets

    async def notify(self, message: str, ignore=None) -> None:
        """
            Notificar todos os clientes conectados ao soquete
        """
        if self.nodes:
            if ignore is not None:
                n = self.nodes.copy()
                n.remove(ignore)
                await asyncio.wait([node.send(message) for node in n])
            else:
                await asyncio.wait([node.send(message) for node in self.nodes])

    async def register(self, ws: WebSocketServerProtocol) -> None:
        """
            Registre um novo cliente no soquete
        """
        self.nodes.add(ws)
        """
        _notify = {
            'u': 'register'
        }
        await self.notify(json.dumps(_notify))
        """

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        """
           Remover um cliente do soquete
        """
        self.nodes.remove(ws)
        """
        _notify = {
            'u': 'unregister'
        }
        await self.notify(json.dumps(_notify))
        """

    async def ws_handler(self, node: WebSocketServerProtocol, uri: str) -> None:
        """
            Gerenciar entradas e saídas de dados de soquete
        """
        await self.register(node)
        try:
            """
                Cabeçalho de confirmação de conexão
            """
            _dir = {
                'h': {
                    'n': 'Ripda Wallet',
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
                    """
                        Verifique se os dados estão no formato adequado, em caso afirmativo,
                        chame a função correspondente e passe os dados para ela.
                    """
                    if 'm' and 'f' and 'd' in receiver:
                        if receiver['m'] == 'wallet':
                            callback = await self.wallet(receiver, node)
                            await node.send(callback)
                    else:
                        """
                            Retorna uma mensagem de erro se a API não suportar a solicitação feita.
                        """
                        e = await Utils().sender(m=receiver['m'], f=receiver['f'], e='Não há suporte para o '
                                                                                     'método que você solicitou')
                        await node.send(e)
                except Exception as e:
                    logging.exception(e)

        except Exception as e:
            logging.exception(e)

        finally:
            await self.unregister(node)

    async def wallet(self, receiver, node):
        """
            Criar uma nova carteira
        """
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
                r = await Utils().sender(m='wallet', f='create_wallet', r=_wallet)
                return str(r)
            else:
                process = Wallet().create_wallet()
                _wallet = {
                    'private_key': process['private_key'].hex(),
                    'public_key': process['public_key'],
                    'wallet': process['wallet']
                }
                r = await Utils().sender(m='wallet', f='create_wallet', r=_wallet)
                return str(r)
        """
            Criar uma nova transação
        """
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
                        r = await Utils().sender(m='wallet', f='create_transaction', e='Não foi possível criar '
                                                                                       'transação')
                        await self.notify(message=r)
                        return str(r)
                    else:
                        sender = {
                            'm': 'transaction',
                            'f': 'create',
                            'd': create_transaction,
                        }
                        """
                            Cadastrar a transação no Pool e aguardar a confirmação do cadastro.
                        """
                        uri = 'ws://' + str(getc('ripda_node', 'core_host')) + ':' + str(
                            getc('ripda_node', 'core_port'))
                        async with websockets.connect(uri) as n:
                            await n.send(json.dumps(sender))
                            async for message in n:
                                receiver = json.loads(message)
                                if 'm' and 'f' and 'd' in receiver:
                                    if receiver['m'] == 'transaction' and receiver['f'] == 'create' \
                                            and receiver['d'] == create_transaction:
                                        await n.close()
                        r = await Utils().sender(m='wallet', f='create_transaction', r=create_transaction)
                        await self.notify(message=r)
                        return str(r)
                except Exception as e:
                    logging.exception(e)
                    return await Utils().sender(m=receiver['f'], f=receiver['f'], e=str(e))
            return await Utils().sender(m='wallet', f='create_transaction',
                                        e='Dados incompletos para realizar a transação')
        return await Utils().sender(m='wallet', f=receiver['f'], e='Não foi possível identificar o comando')
