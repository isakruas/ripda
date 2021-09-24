import codecs
import hashlib
import logging

from base58 import b58encode
import ecdsa
from ecdsa.util import PRNG
import json
from ripda.transaction.utils import Utils
from ripda.transaction.core import Transaction
from ripda.block.core import Block


class Wallet:

    def __init__(self, private_key=None):
        Block().view()
        self.public_key = None
        self.wallet = None
        self.private_key = None
        if private_key is not None:
            if isinstance(private_key, bytes):
                try:
                    self.private_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.NIST521p)
                    self.get_public_key()
                    self.get_wallet()
                except Exception as e:
                    logging.exception(e)

    def create_transaction(self, receiver, amount):
        if self.private_key is not None:
            transaction = Transaction(
                sender=self.wallet,
                receiver=receiver,
                amount=amount,
                sender_private_key=self.get_private_key(),
                sender_public_key=self.public_key
            ).create()
            return transaction
        return False

    def create_wallet(self, email=None, password=None):
        entropy = None
        _entropy = False
        if email is not None:
            if email is not None:
                _entropy = True

        if _entropy:
            user = {
                'email': email,
                'password': password
            }
            entropy = PRNG(bytes(json.dumps(user), 'utf-8'))

        if entropy is not None:
            private_key = ecdsa.SigningKey.generate(entropy=entropy, curve=ecdsa.NIST521p)
        else:
            private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)

        self.private_key = private_key

        self.get_public_key()

        self.get_wallet()

        return self.view()

    def get_private_key(self):
        if self.private_key is not None:
            return self.private_key.to_string()
        return self.private_key

    def get_public_key(self):
        if self.private_key is not None:
            self.public_key = self.private_key.verifying_key.to_string('compressed').hex()
            return self.public_key
        return self.public_key

    def get_wallet(self):
        if self.private_key is not None:
            try:
                public_key = ecdsa.VerifyingKey.from_string(bytearray.fromhex(self.public_key), curve=ecdsa.NIST521p)
                public_key_sha256 = hashlib.sha256(public_key.to_string())
                public_key_ripemd160 = hashlib.new('ripemd160')
                public_key_ripemd160.update(public_key_sha256.digest())
                wallet_raw = '00' + public_key_ripemd160.hexdigest()
                wallet_raw_bytes = codecs.decode(wallet_raw.encode('utf-8'), 'hex')
                wallet_raw_sha256 = hashlib.sha256(hashlib.sha256(wallet_raw_bytes).digest())
                wallet_raw_check = wallet_raw_sha256.hexdigest()[:8]
                _wallet = wallet_raw + wallet_raw_check
                wallet_bytes = codecs.decode(_wallet.encode('utf-8'), 'hex')
                _wallet = b58encode(wallet_bytes).decode("utf-8")
                self.wallet = _wallet
                return self.wallet
            except ecdsa.BadSignatureError:
                return self.wallet
        return self.wallet

    def view(self):
        _wallet = {
            'private_key': self.get_private_key(),
            'public_key': self.get_public_key(),
            'wallet': self.get_wallet()
        }

        return _wallet

    def is_signature_valid(self, _object, signature):
        if self.private_key is not None:
            try:
                signature = bytearray.fromhex(signature)
                _object_sha256_ripemd160 = Utils().ripemd160(Utils().sha256(json.dumps(_object)))
                transaction = codecs.decode(_object_sha256_ripemd160.encode('utf-8'), 'hex')
                public_key = ecdsa.VerifyingKey.from_string(bytearray.fromhex(self.public_key), curve=ecdsa.NIST521p)
                try:
                    public_key.verify(signature, transaction)
                    return True
                except Exception as e:
                    logging.exception(e)
                    return False
            except Exception as e:
                logging.exception(e)
                return False
        return False
