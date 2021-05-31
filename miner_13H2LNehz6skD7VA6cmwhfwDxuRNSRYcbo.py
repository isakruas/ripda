import json
import websockets
from miner.core import Miner
import asyncio


async def get_last_block():
    async with websockets.connect('ws://localhost:1140') as node:
        try:
            await node.send(json.dumps({
                'm': 'block',
                'f': 'view',
                'd': {
                }
            }))
            while True:
                receiver = await node.recv()
                receiver = json.loads(receiver)
                if 'm' and 'f' and 'r' in receiver:
                    if receiver['m'] == 'block':
                        if receiver['f'] == 'view':
                            return receiver['r']
        finally:
            pass


async def add_block_on_blockchain(forger):
    async with websockets.connect('ws://localhost:1140') as node:
        try:
            await node.send(json.dumps({
                'm': 'blockchain',
                'f': 'add_block',
                'd': forger
            }))
            while True:
                receiver = await node.recv()
                receiver = json.loads(receiver)
                if 'm' and 'f' in receiver:
                    if receiver['m'] == 'blockchain':
                        if receiver['f'] == 'add_block':
                            return receiver
        finally:
            pass


async def main():
    print('miner_13H2LNehz6skD7VA6cmwhfwDxuRNSRYcbo')
    while True:
        block = await get_last_block()
        if block['forger']:
            forger = Miner(
                block=block,
                wallet='13H2LNehz6skD7VA6cmwhfwDxuRNSRYcbo'
            ).ripda()
            receiver = await add_block_on_blockchain(forger)
            if 'd' in receiver:
                print('Bloco adicionado com sucesso')
            if 'e' in receiver:
                print(receiver['e'])
        await asyncio.sleep(0.5)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    main()
))
loop.run_forever()
