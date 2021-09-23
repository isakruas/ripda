from ripda.manages.factory import FACServer
from websockets import WebSocketServerProtocol
import json


def echo(**kwds):
    return kwds


class Blockchain(FACServer):

    methods = 'echo',

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
