from ripda.servers.wallet import Wallet
from ripda.servers.blockchain import Blockchain
from ripda import settings
import websockets


async def wallet():
    """
    Nó em que a carteira será servida
    """
    server = await websockets.serve(Wallet().handler, settings.WALLET_HOST, settings.WALLET_PORT)
    await server.server.serve_forever()


async def blockchain(host: str = settings.BLOCKCHAIN_HOST, port: int = settings.BLOCKCHAIN_PORT):
    """
    Nó no qual o blockchain será servido
    """
    server = await websockets.serve(Blockchain().handler, host, port)
    await server.server.serve_forever()
