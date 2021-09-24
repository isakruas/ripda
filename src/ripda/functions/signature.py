from ripda.functions.utils.ripemd160 import ripemd160
from ripda.functions.utils.sha256 import sha256
import json
import codecs
import binascii
import ecdsa


def sha256_ripemd160_decode_hex(data) -> str:
    """
    Equivalente á: sha256(ripemd160(data)).hex
    """
    sha256_ripemd160 = str(binascii.hexlify(
        ripemd160(binascii.unhexlify(sha256(json.dumps(data))))), 'ascii')
    sha256_ripemd160_decode_hex = codecs.decode(
        sha256_ripemd160.encode('utf-8'), 'hex')
    return sha256_ripemd160_decode_hex


def verify(data: dict, signature: str, public_key: str) -> bool:
    """
    Verifique se uma assinatura gerada é válida.
    """
    try:
        signature = bytearray.fromhex(signature)
        key = ecdsa.VerifyingKey.from_string(
            bytearray.fromhex(public_key), curve=ecdsa.NIST521p)
        key.verify(signature, sha256_ripemd160_decode_hex(data))
        return True
    except Exception:
        return False


def create(data: dict, private_key: str) -> str:
    """
    Crie uma assinatura digital para um conjunto de dados.
    """
    try:
        key = ecdsa.SigningKey.from_string(
            bytearray.fromhex(private_key), curve=ecdsa.NIST521p)
        signature = key.sign(sha256_ripemd160_decode_hex(data))
        return signature.hex()
    except:
        return str()
