import json
from block.core import Block
from blockchain.utils import Utils
from random import randrange

class Miner:
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

            while not Block().is_hash_valid(self.hash):
                block = {
                    'count': self.block['count'],
                    'transactions': self.block['transactions'],
                    'last_hash': self.block['last_hash'],
                    'timestamp': self.block['timestamp'],
                    'nonce': self.nonce,
                    'forging': self.wallet
                }

                self.hash = Utils.sha256(json.dumps(block))

                self.nonce += 1

            block['hash'] = self.hash

            return block
