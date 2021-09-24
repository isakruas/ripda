from ripda.manages.singleton import Singleton
from ripda.core.transaction import Transaction
from ripda.functions.wallet import derive as wallet_derive
import ecdsa
from ecdsa.util import PRNG
import json


class Wallet(metaclass=Singleton):
    """
    Modelo de gerenciamento de dados do aplicativo Wallet
    """

    # Cria uma instância no aplicativo Wallet do modelo de Transaction
    transaction = Transaction()

    def __init__(self) -> None:
        self.__public_key = None
        self.__wallet = None
        self.__private_key = None

    def repr(self) -> dict:
        """
        Cria uma representação de Wallet
        """
        return {
            'private_key': self.__private_key,
            'public_key': self.__public_key,
            'wallet': self.__wallet
        }

    def close(self) -> dict:
        """
        Se os dados de Wallet estiverem carregados, esqueça.
        Retorne a representação de Wallet
        """
        self.__public_key = None
        self.__wallet = None
        self.__private_key = None
        return self.repr()

    def open(self, pem: str) -> dict:
        """
        recebe uma chave privada e deriva dessa chave o endereço da carteira
        e sua chave pública. Salva uma representação dos dados na memória.
        """

        try:
            pem = str.encode(pem)
            key = ecdsa.SigningKey.from_pem(pem)
            self.__private_key = key.to_string().hex()
            self.__public_key = key.verifying_key.to_string('compressed').hex()
            self.__wallet = wallet_derive(self.__public_key)
            return self.repr()
        except:
            return self.close()

    def create(self, **kwds) -> bytes:
        """
        Cria uma chave privada com ou sem entropia.
        Chaves com a mesma entropia são idênticas.
        """
        if len(kwds) >> 0:
            key = ecdsa.SigningKey.generate(entropy=PRNG(
                bytes(json.dumps(kwds), 'utf-8')), curve=ecdsa.NIST521p)
        else:
            key = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)
        return key.to_pem().decode()
