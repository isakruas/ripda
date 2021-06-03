from ripda.node.core import Node
from ripda.node.wallet import NodeWallet
from ripda.node.miner import NodeMiner
from ripda.settings import getc
import websockets


async def node():
    server = Node()
    await websockets.serve(server.ws_handler, str(getc('ripda_node', 'core_host')), int(
        getc('ripda_node', 'core_port')))


async def wallet():
    server = NodeWallet()
    await websockets.serve(server.ws_handler, str(getc('ripda_node', 'wallet_host')), int(
        getc('ripda_node', 'wallet_port')))


async def miner():
    server = NodeMiner()
    await websockets.serve(server.ws_handler, str(getc('ripda_node', 'miner_host')), int(
        getc('ripda_node', 'miner_port')))
