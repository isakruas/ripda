from ripda.manages.factory import FACServer
from ripda.core.blockchain import Blockchain as B
from websockets import WebSocketServerProtocol
import json

# Instância o modelo Blockchain para conexão entre o mesmo e a API
blockchain = B()


def echo(**kwds):
    """
    Retorna um eco para a chamada na API
    """
    return kwds


class Blockchain(FACServer):

    # Métodos aceitos pela API
    methods = 'echo', 'blockchain.verify', 'blockchain.add',

    # Métodos em que ao receber uma mensagem, ela deve ser acionada para os nós conectados.
    methods_to_notify = 'blockchain.add',

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
                            # Notificar os nós conectados se não for uma mensagem de retorno
                            if rdef in self.methods_to_notify and not 'return' in receiver:
                                await self.notify(json.dumps(receiver))
                            receiver['return'] = eval(f'{rdef}(**{kwds})')
                            
                            if rdef == 'blockchain.add':
                                await socket.send(json.dumps(receiver['return']))
                            else:
                                await socket.send(json.dumps(receiver))
                    else:
                        pass
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            await self.unregister(socket)
