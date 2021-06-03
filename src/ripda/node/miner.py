"""
    Esta API ainda está em construção, não é possível utilizar seus recursos nesta versão do sistema.
"""
import asyncio
import json
import logging

from websockets import WebSocketServerProtocol

from ripda.node.utils import Utils
from ripda.miner.core import Miner

node_miners = set()


class NodeMiner:
    """
        Conjunto de recursos para mineradores de Ripdas
    """
    global node_miners

    def __init__(self):
        self.private_key = None
        self.nodes = node_miners

    async def notify(self, message: str) -> None:
        """
            Notificar todos os clientes conectados ao soquete
        """
        if self.nodes:
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
                    'n': 'Ripda Miner',
                    'v': '1.0.0.dev3',
                }
            }
            await node.send(json.dumps(_dir))
            async for message in node:
                try:
                    receiver = json.loads(message)
                    """
                        Verifique se os dados estão no formato adequado, em caso afirmativo,
                        chame a função correspondente e passe os dados para ela.
                    """
                    if 'm' and 'f' and 'd' in receiver:
                        if receiver['m'] == 'miner':
                            callback = await self.forger(receiver)
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

    async def forger(self, receiver):
        """
            Receber um bloco e então validá-lo
        """
        if receiver['f'] == 'forger':
            if 'wallet' and 'block' in receiver['d']:
                forger = Miner(
                    wallet=receiver['d']['wallet'],
                    block=receiver['d']['block'],
                ).ripda()
        _notify = {
            'e': 'Não foi possível identificar o comando'
        }
        return json.dumps(_notify)
