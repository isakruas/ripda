import json
import time
from wallet.core import Wallet
import asyncio
import websockets

_wallet = Wallet().create_wallet()

send: bool = True

frame = {
    'm': 'wallet',
    'f': 'create_transaction',
    'd': {
        'receiver': '18QT6s1zek1ZFaBMMENCfonwTkVfSxjuzZ',
        'amount': 10,
        'private_key': _wallet['private_key'].hex(),
    }
}


async def core(order):
    global send
    if 'r' in json.loads(order):
        await asyncio.sleep(2.5)
        send = True
    else:
        send = False


async def wallet():
    global send
    global _wallet
    uri = 'ws://localhost:1050'
    try:
        async with websockets.connect(uri) as node:
            while True:
                try:
                    if send:
                       
                        await node.send(json.dumps(frame))
                    order = await node.recv()
                    await core(order=order)
                except:
                    pass
    except:
        await asyncio.sleep(5)
        wallet()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    wallet()
))
loop.run_forever()
