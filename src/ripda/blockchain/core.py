import codecs
import json
from typing import List, Any
import os
import ecdsa
from ..transaction.utils import Utils
from ..blockchain.utils import Utils
from ..config import getc
try:
    from ..transaction.pool import Pool
except ImportError:
    pass

blockchain: List[Any] = []
wallet = {}


def is_signature_valid(transaction, signature, sender_public_key):
    try:
        signature = bytearray.fromhex(signature)
        transaction_sha256_ripemd160 = Utils.ripemd160(Utils.sha256(json.dumps(transaction)))
        transaction = codecs.decode(transaction_sha256_ripemd160.encode('utf-8'), 'hex')
        public_key = ecdsa.VerifyingKey.from_string(bytearray.fromhex(sender_public_key), curve=ecdsa.NIST521p)
        try:
            public_key.verify(signature, transaction)
            return True
        except NameError:
            return False
    except NameError:
        return False


class Blockchain:
    global blockchain
    global wallet

    def __init__(self):
        self.blockchain = blockchain
        self.wallet = wallet
        self.difficulty = '0' * int(getc('ripda_block', 'core_difficulty'))
        self.block = []
        self.path = str(getc('ripda', 'path_blocks'))
        if len(self.blockchain) == 0:
            blocks = os.listdir(self.path)
            if 'wallets.r' in blocks:
                blocks.remove('wallets.r')
                os.remove(self.path + 'wallets.r')
                pass

            if len(blocks) >> 0:
                for block in sorted(blocks):
                    with open(self.path + block) as e:
                        r = json.loads(e.read())
                    self.add_block(r, sync=True)

    def view(self):
        return self.blockchain

    def add_block(self, block, sync=False):
        self.block = block.copy()
        if len(self.blockchain) >> 0:
            if self.block['count'] >> 3:
                if len(self.block['transactions']) == 0:
                    return False
        for transaction in self.block['transactions']:
            _transaction = {
                'sender': transaction['sender'],
                'receiver': transaction['receiver'],
                'amount': transaction['amount'],
                'timestamp': transaction['timestamp']
            }
            if is_signature_valid(_transaction, transaction['signature'], transaction['sender_public_key']) is False:
                return False
        _block = {
            'count': self.block['count'],
            'transactions': self.block['transactions'],
            'last_hash': self.block['last_hash'],
            'timestamp': self.block['timestamp'],
            'nonce': self.block['nonce'],
            'forging': self.block['forging']
        }

        if len(self.blockchain) >> 0:
            if self.blockchain[-1]['hash'] != self.block['last_hash']:
                return False

        if Utils.sha256(json.dumps(_block)) == self.block['hash']:
            if Utils().is_hash_valid(self.block['hash']):
                self.blockchain.append(self.block)

                if len(self.block['transactions']) >> 0:
                    for transaction in self.block['transactions']:
                        self.wallet[transaction['sender']]['amount'] -= transaction['amount']
                        self.wallet[transaction['receiver']]['amount'] += transaction['amount']

                if self.block['forging'] in self.wallet:
                    self.wallet[self.block['forging']]['amount'] += 0.04
                else:
                    self.wallet[self.block['forging']] = {}
                    self.wallet[self.block['forging']]['amount'] = 0.04

                _path_wallet = self.path + 'wallets.r'
                g = open(_path_wallet, 'w')
                g.write(json.dumps(self.wallet, indent=4))
                g.close()

                _path = self.path + str(self.block['timestamp']) + '.r'

                if not sync:

                    f = open(_path, 'w')
                    """
                        Arquivo compactado
                    """

                    f.write(json.dumps(self.block))

                    """
                    f.write(json.dumps(self.block, indent=4))
                    
                    """

                    f.close()
                if Pool().clear():
                    Pool().update()
                    return self.block
                else:
                    self.blockchain.remove(self.block)
                    if os.path.exists(_path):
                        os.remove(_path)
                    return False
            return False
        return False
