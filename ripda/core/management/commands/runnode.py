import asyncio
import importlib
import websockets
from ripda import __version__
from ripda.conf import settings
from datetime import datetime

"""
    Cria um endpoint para que outros se conectem a ele.
    Todas as comunicações entre os outros nós e estes serão feitas através deste endpoint.
"""


async def __main(**kwargs):
    if settings.HANDLER_MODULE is not None:
        md = importlib.import_module(settings.HANDLER_MODULE)

        # classe Node esperada no aplicativo do usuário.
        class HandlerNode(md.Node):
            pass

        handler_node = HandlerNode()

        host = settings.BLOCKCHAIN_HOST
        port = settings.BLOCKCHAIN_PORT

        if 'host' in kwargs and 'port' in kwargs:
            host = kwargs['host']
            port = kwargs['port']

        server = await websockets.serve(handler_node.handler, host, port)

        print(datetime.now().strftime("%B %d, %Y - %H:%M:%S"))
        print(f"Ripda version {__version__}, using settings '{settings.SETTINGS_MODULE}'")
        print(f'Starting server at ws://{host}:{port}/')
        print(f'Quit the server with CTRL-BREAK.')

        await server.server.serve_forever()


def main(**kwargs):
    return asyncio.run(__main(**kwargs))
