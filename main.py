from node.core import Node
import asyncio
import websockets
from wallet.core import Wallet
from miner.core import Miner

_wallet = Wallet().create_wallet()


async def miner():
    while True:
        Miner().ripda()
        await asyncio.sleep(30)


async def log():
    global _wallet
    wallet = Wallet(
        private_key=_wallet['private_key']
    )

    while True:
        await asyncio.sleep(0.5)

        wallet.create_transaction(
            receiver='18QT6s1zek1ZFaBMMENCfonwTkVfSxjuzZ',
            amount=10
        )
        print('len(nodes) = ' + str(Node().view()))


async def node():
    server = Node()
    await websockets.serve(server.ws_handler, 'localhost', 6789)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    node(),
    log(),
    miner()
))
loop.run_forever()
