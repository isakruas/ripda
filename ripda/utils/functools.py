import os
import hashlib
from uuid import UUID
from ecutils import ECDSA


async def random_address() -> tuple:
    """
    cria uma chave privada e um endereço de carteira de maneira quase aleatória.
    :return: private_key, address
    """

    private_key = int.from_bytes(os.urandom(65), byteorder='little')

    ec = ECDSA(curve='secp521r1', private_key=private_key)

    public_key = int(f'{ec.public_key[0]}{ec.public_key[1]}')

    if len(hex(ec.public_key[0])) != len(hex(ec.public_key[1])):
        return await random_address()

    ripemd160 = hashlib.new('ripemd160')

    ripemd160.update(hashlib.sha256(f'{public_key}'.encode('utf-8')).digest())

    uuid = hashlib.sha256(hashlib.sha256(ripemd160.digest()).digest()).digest()[:16]

    return hex(private_key)[2:], UUID(bytes=uuid, version=5).hex
