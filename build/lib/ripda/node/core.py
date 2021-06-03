import asyncio
import json
import logging

from websockets import WebSocketServerProtocol, WebSocketException
from ripda.block.core import Block
from ripda.blockchain.core import Blockchain
from ripda.node.utils import Utils

nodes = set()


class Node:
    """
        Este módulo possui uma série de funcionalidades que facilitam a integração das aplicações ao núcleo
        da Ripda. São APIs que permitem a criação de uma rede P2P através de websockets, bem como o envio de
        ordens através de qualquer dispositivo compatível com websockets para a rede. Você pode usar os recursos
        das APIs, usando websockets.
    """
    global nodes

    def __init__(self):
        self.private_key = None
        self.nodes = nodes
        Block().view()

    def view(self):
        return len(self.nodes)

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
                    'n': 'Ripda Core',
                    'v': '1.0.0.dev3',
                }
            }
            await node.send(json.dumps(_dir))
            async for message in node:
                try:
                    receiver = json.loads(message)
                    """
                    Formato de dados aceitos
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
                        if receiver['m'] == 'block':
                            callback = await self.block(receiver, node)
                            await node.send(callback)
                        if receiver['m'] == 'blockchain':
                            callback = await self.blockchain(receiver, node)
                            await node.send(callback)
                        if receiver['m'] == 'transaction':
                            callback = await self.transaction(receiver, node)
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

    async def transaction(self, receiver, node):
        """
            Envie uma mensagem para todos os conectados ao Pool de que uma nova transação foi realizada nele. Isso serve
            para sincronizar transações entre todos os Pools conectados.
        """
        if receiver['f'] == 'create':
            sender = {
                'm': 'transaction',
                'f': 'create',
                'd': receiver['d'],
            }
            await self.notify(message=json.dumps(sender), ignore=node)
            return json.dumps(sender)

    async def block(self, receiver, node):
        """
            Retorna a estrutura do bloco no Pool. Isso é para verificações de sincronização entre pols conectados.
        """
        if receiver['f'] == 'view':
            return await Utils().sender(m='block', f='view', r=Block().view())
        """
            Verifique se um determinado hash está no formato aceito pela rede
        """
        if receiver['f'] == 'is_hash_valid':
            if 'hash' in receiver['d']:
                if Block().is_hash_valid(receiver['d']['hash']):
                    return await Utils().sender(m='block', f='is_hash_valid', r='True')
                else:
                    return await Utils().sender(m='block', f='is_hash_valid', r='False')
            return await Utils().sender(m='block', f='is_hash_valid', e='Parâmetros incompletos para usar esta função')
        return await Utils().sender(m='block', f=receiver['f'], e='Não foi possível identificar o comando')

    async def blockchain(self, receiver, node):
        """
            Ver todos os blocos salvos na memória Pool
        """
        if receiver['f'] == 'view':
            return await Utils().sender(m='blockchain', f='view', r=Blockchain().view())
        """
            Recebe um novo bloco em um dos mineradores conectados ao Pool, e tenta adicionar a cadeia de blocos, 
            se conseguir adicionar, envia o bloco adicionado para todos os outros Pools conectados a ele.
        """
        if receiver['f'] == 'add_block':
            add_block = Blockchain().add_block(
                block=receiver['d']
            )
            if not add_block:
                r = await Utils().sender(m='blockchain', f='add_block', e='Bloco não pôde ser adicionado')
                return r
            r = await Utils().sender(m='blockchain', f='add_block', d=add_block)
            await self.notify(message=r, ignore=node)
            return r
        return await Utils().sender(m='blockchain', f=receiver['f'], e='Não foi possível identificar o comando')
