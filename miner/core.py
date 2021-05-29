import json

from block.core import Block
from blockchain.core import Blockchain
from blockchain.utils import Utils


class Miner:
    def __init__(self, block=None):
        self.hash = ''
        self.nonce = 0
        if block is not None:
            self.block = block
        else:
            self.block = Block().view()

    def forging(self):
        return self.block['forger']

    def ripda(self):

        if self.forging():

            self.hash = ''

            self.nonce = 1

            while not Block().is_hash_valid(self.hash):
                block = {
                    'count': self.block['count'],
                    'transactions': self.block['transactions'],
                    'last_hash': self.block['last_hash'],
                    'timestamp': self.block['timestamp'],
                    'nonce': self.nonce
                }

                self.hash = Utils.sha256(json.dumps(block))

                self.nonce += 1

            block['hash'] = self.hash

            return Blockchain().add_block(block)
