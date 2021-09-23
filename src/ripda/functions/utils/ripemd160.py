import hashlib


def ripemd160(data: bytes) -> bytes:
    __ripemd160 = hashlib.new('ripemd160')
    __ripemd160.update(data)
    return __ripemd160.digest()
