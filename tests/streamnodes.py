from ripda.manages.factory import FACClient
from ripda.core.blockchain import Blockchain
from uuid import uuid4
from datetime import datetime
import json
import multiprocessing
from ripda import settings


class Handler(FACClient):
    """
    Lida com eventos de entrada recebidos pela conexão entre o nó e os nós
    """
    async def handler(self, recv) -> None:
        """
        Sempre que receber uma mensagem, envie outra
        """
        print(f'RECEBENDO: {recv}')
        msg = {
            'def': 'echo',
            'kwds': {
                'uid': uuid4().hex,
                'timestamp': datetime.utcnow().timestamp()
            }
        }
        print(f'ENVIANDO: {json.dumps(msg)}')
        if await self.notify(msg):
            print('MENSAGEM ENVIADA COM SUCESSO')
        else:
            print('ERRO AO ENVIAR MENSAGEM')


class STREAMNodes:
    """
    Conecte-se ao nós fakes e mantem a conexão ativa, enviando e recebendo mensagens.
    """

    blockchain = Blockchain()
    handler = Handler()

    def __init__(self) -> None:
        for node in settings.BLOCKCHAIN_NODES:
            _, port = node
            setattr(self, f'__node_{port}', multiprocessing.Process(
                target=self.__run, args=(port,)))

    def __run(self, port: int) -> None:
        self.blockchain.network.stream(**{
            'handler': self.handler,
            'host': settings.BLOCKCHAIN_HOST,
            'port': port
        })

    def start(self):
        for i in self.__dict__:
            self.__dict__[i].start()

    def join(self):
        for i in self.__dict__:
            self.__dict__[i].join()


if __name__ == '__main__':

    streamnodes = STREAMNodes()
    streamnodes.start()
    print(streamnodes.__dict__)
