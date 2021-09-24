from ripda import settings, services
import asyncio
import multiprocessing
import json


class RUNNodes:
    """
    Inicia localmente os nós (nós fakes) aos quais o nó se conectará
    """

    def __init__(self) -> None:
        for node in settings.BLOCKCHAIN_NODES:
            _, port = node
            setattr(self, f'__node_{port}', multiprocessing.Process(
                target=self.__run, args=(port,)))

    def __run(self, port: int):
        asyncio.run(services.blockchain(settings.BLOCKCHAIN_HOST, port))

    def start(self):
        for i in self.__dict__:
            self.__dict__[i].start()

    def join(self):
        for i in self.__dict__:
            self.__dict__[i].join()


if __name__ == '__main__':

    runnodes = RUNNodes()
    runnodes.start()

    print(runnodes.__dict__)
