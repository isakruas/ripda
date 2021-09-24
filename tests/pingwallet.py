from ripda import settings
from ripda.core.network import Network
from uuid import uuid4


class PINGWallet:
    """
    Envia uma requisição para Wallet
    """
    network = Network()

    def __init__(self) -> None:
        self.network.nodes = [(settings.WALLET_HOST, settings.WALLET_PORT)]

    def ping(self, **kwds):
        return self.network.ping(**kwds)


if __name__ == '__main__':
    
    pingwallet = PINGWallet()
    print(pingwallet.ping(**{
        'kwds': {
            'def': 'echo',
            'kwds': {
                'uid': uuid4().hex
            }
        }
    }))
