
import asyncio
from ripda import services


class RUNWallet:
    """
    Inicia a API Wallet
    """

    def start(self) -> None:
        asyncio.run(services.wallet())


if __name__ == '__main__':
    runwallet = RUNWallet()
    runwallet.start()
