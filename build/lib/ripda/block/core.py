import json
from datetime import datetime
from ..transaction.pool import Pool
from ..transaction.utils import Utils
from ..blockchain.core import Blockchain


class Block:

    def __init__(self):
        self.difficulty = '0' * 4
        self.count = len(Blockchain().view())
        self.transactions = Pool().view()
        self.timestamp = datetime.utcnow().timestamp()
        self.forger = Pool().forging_required()
        self.nonce = None
        self.hash = None
        self.block = {}
        if len(Blockchain().view()) == 0:
            self.last_hash = 0
            self.transactions = []
            self.create_genesis_block()
        else:
            self.last_hash = Blockchain().view()[-1]['hash']

    def view(self):
        block = {
            'count': self.count,
            'transactions': self.transactions,
            'last_hash': self.last_hash,
            'timestamp': self.timestamp,
            'forger': self.forger,
        }
        self.block = block

        return block

    def create_genesis_block(self):

        self.hash = ''
        self.nonce = 1
        block = {}

        while not self.is_hash_valid(self.hash):
            block = {
                'count': self.count,
                'transactions': self.transactions,
                'last_hash': self.last_hash,
                'timestamp': self.timestamp,
                'nonce': self.nonce,
                'forging': '1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU'
            }

            self.hash = Utils.sha256(json.dumps(block))

            self.nonce += 1

        block['hash'] = self.hash

        return Blockchain().add_block(block)

    def is_hash_valid(self, _hash):
        return _hash.startswith(self.difficulty)
