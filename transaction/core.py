import ecdsa
import json
import codecs
from datetime import datetime
from .pool import Pool
from .utils import Utils
from blockchain.core import Blockchain


class Transaction:

    def __init__(self, sender, receiver, amount, sender_private_key, sender_public_key):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.sender_private_key = sender_private_key
        self.timestamp = datetime.utcnow().timestamp()
        self.signature = ''
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.transaction = {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        self.create_signature()

    def update_signature(self, signature):
        self.signature = signature
        self.transaction['signature'] = self.signature
        self.transaction['sender_public_key'] = self.sender_public_key

    def create_signature(self):
        transaction_sha256_ripemd160 = Utils.ripemd160(Utils.sha256(json.dumps(self.transaction)))

        transaction = codecs.decode(transaction_sha256_ripemd160.encode('utf-8'), 'hex')

        private_key = ecdsa.SigningKey.from_string(self.sender_private_key, curve=ecdsa.NIST521p)

        signature = private_key.sign(transaction)

        return self.update_signature(signature.hex())

    def create(self):
        if len(Blockchain().view()) == 0:
            return False

        if Pool().add_transaction(
            transaction=self.transaction
        ):
            return True

        return False

    def view(self):
        return self.transaction
