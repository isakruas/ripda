import json
from ripda.block.core import Block
from ripda.blockchain.utils import Utils
from random import randrange


class Miner:
    """
        Miner fornece um conjunto de ferramentas que tornam possível minerar um bloco para posterior
        adição ao blockchain.
    """

    def __init__(self, block=None, wallet=None):
        self.hash = ''
        self.nonce = randrange(1000)
        self.wallet = wallet
        if block is not None:
            self.block = block
        else:
            self.block = Block().view()

    def forging(self):
        return self.block['forger']

    def ripda(self):
        if len(self.block) == 0:
            return False

        if self.wallet is None:
            return False

        if self.forging():

            self.hash = ''
            self.nonce = 1
            block = {}

            while not Utils().is_hash_valid(self.hash):
                block = {
                    # hash do último bloco
                    'last_hash': self.block['last_hash'],
                    # número do índice do bloco
                    'count': self.block['count'],
                    # resumo do bloco
                    'abstract': {
                        'transactions': {
                            'count': self.block['abstract']['transactions']['count'],
                            'amount': self.block['abstract']['transactions']['amount']
                        }
                    },
                    # transações realizadas no bloco
                    'transactions': self.block['transactions'],
                    # hora em que o bloco foi obtido
                    'timestamp': self.block['timestamp'],
                    # valor de verificação de hash de bloco
                    'nonce': self.nonce,
                    # carteira do minerador responsável por organizar o bloco
                    'forging': self.wallet
                }

                self.hash = Utils.sha256(json.dumps(block))

                self.nonce += 1

            block['hash'] = self.hash

            return block
