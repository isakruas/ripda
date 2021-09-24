from ripda import settings
from ripda.core.network import Network
from uuid import uuid4


class PINGNodes:
    """
    Envia uma requisição para os nós fakes
    """
    network = Network()

    FAKE_NODES = list()

    def __init__(self) -> None:
        for node in settings.BLOCKCHAIN_NODES:
            _, port = node
            self.FAKE_NODES.append((settings.BLOCKCHAIN_HOST, port))

    def ping(self, **kwds):
        self.network.nodes = self.FAKE_NODES
        return self.network.ping(**kwds)


if __name__ == '__main__':

    pingnodes = PINGNodes()
    print(pingnodes.ping(**{
        'kwds': {
            'def': 'echo',
            'kwds': {
                'uid': uuid4().hex
            }
        }
    }))
