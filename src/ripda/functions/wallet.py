import codecs
import binascii
from base58 import b58encode
from ripda.functions.utils.sha256 import sha256
from ripda.functions.utils.ripemd160 import ripemd160


def derive(public_key: str) -> str:
    """
    Deriva da chave pública o endereço da carteira.
    """
    public_key_sha256 = binascii.unhexlify(sha256(public_key))
    public_key_ripemd160 = str(
        b'00' + binascii.hexlify(ripemd160(public_key_sha256)), 'ascii')
    public_key_ripemd160_bytes = codecs.decode(
        public_key_ripemd160.encode('utf-8'), 'hex')
    public_key_ripemd160_bytes_sha256 = str(binascii.hexlify(sha256(
        sha256(public_key_ripemd160_bytes, is_bytes=True), is_bytes=True)), 'ascii')[:8]
    raw = public_key_ripemd160 + public_key_ripemd160_bytes_sha256
    raw_bytes = codecs.decode(raw.encode('utf-8'), 'hex')
    return b58encode(raw_bytes).decode('utf-8')
