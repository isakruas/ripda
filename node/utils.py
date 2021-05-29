import asyncio

import websockets


async def notify(message):
    uri = 'ws://localhost:6789'
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)


#asyncio.get_event_loop().run_until_complete(notify(''))
