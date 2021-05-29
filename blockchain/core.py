import json
from typing import List, Any

from transaction.utils import Utils
from blockchain.utils import Utils

try:
    from transaction.pool import Pool
except ImportError:
    pass

blockchain: List[Any] = []


class Blockchain:
    global blockchain

    def __init__(self):
        self.blockchain = blockchain
        self.difficulty = '0' * 4

    def view(self):
        return self.blockchain

    def add_block(self, block):
        _block = {
            'count': block['count'],
            'transactions': block['transactions'],
            'last_hash': block['last_hash'],
            'timestamp': block['timestamp'],
            'nonce': block['nonce'],
        }

        if Utils.sha256(json.dumps(_block)) == block['hash']:
            if Utils().is_hash_valid(block['hash']):
                if Pool().clear():
                    self.blockchain.append(block)
                return True
            return False
        return False
