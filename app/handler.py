from ripda.core.network.server import Server


class Node(Server):
    async def handler(self, socket, uri) -> None:
        await self.register(socket)
        try:
            async for receiver in socket:
                callback = await self.callback(socket, receiver)
                print(callback)
                await self.notify(receiver, ignore=socket)
        except Exception as exc:
            print(exc)
        finally:
            await self.unregister(socket)
