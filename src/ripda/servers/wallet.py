from ripda.manages.factory import FACServer
from ripda.core.wallet import Wallet as W
from websockets import WebSocketServerProtocol
import json

# Instância o modelo Wallet para conexão entre o mesmo e a API
wallet = W()


def echo(**kwds):
    """
    Retorna um eco para a chamada na API
    """
    return kwds


class Wallet(FACServer):
    """
    ---------------------------------------------------------------------
    Interface de programação de aplicativo Wallet
    ---------------------------------------------------------------------
    Requisição:
    {
        'def': 'method',
        'kwds': dict()
    }
    O kwds é passado para o method: method(**kwds)
    ---------------------------------------------------------------------
    Resposta:
    {
        'def': 'method',
        'kwds': dict(),
        'return': list, dict, str, int ...
    }
    Os dados de entrada são retornados com a resposta do método executado
    ---------------------------------------------------------------------
    """

    # Métodos aceitos pela API
    methods = 'echo', 'wallet.create', 'wallet.open', 'wallet.repr', 'wallet.close', 'wallet.transaction.prepare', 'wallet.transaction.push', 'wallet.transaction.get', 'wallet.transaction.abort', 'wallet.transaction.repr',

    async def handler(self, socket: WebSocketServerProtocol, uri: str) -> None:

        await self.register(socket)

        try:
            async for receiver in socket:
                try:
                    receiver = json.loads(receiver)
                    if 'def' and 'kwds' in receiver:
                        kwds = receiver['kwds']
                        rdef = receiver['def']
                        if rdef in self.methods:
                            receiver['return'] = eval(f'{rdef}(**{kwds})')
                            await socket.send(json.dumps(receiver))
                    else:
                        pass
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            await self.unregister(socket)
