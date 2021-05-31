from node.core import Node
from node.wallet import NodeWallet
from node.miner import NodeMiner
import asyncio
import websockets


async def node():
    server = Node()
    await websockets.serve(server.ws_handler, 'localhost', 1140)


async def node_wallet():
    server = NodeWallet()
    await websockets.serve(server.ws_handler, 'localhost', 1050)


"""
    Descontinuado
"""
async def node_miner():
    server = NodeMiner()
    await websockets.serve(server.ws_handler, 'localhost', 1120)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    node(),
    node_wallet(),
    node_miner()
))
loop.run_forever()
