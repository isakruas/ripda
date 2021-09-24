from ripda.functions.miner import sha256
from ripda import settings
from ripda.core.block import Block


if __name__ == '__main__':
    block: dict = Block().repr()
    del block['hash']
    del block['nonce']
    data = tuple()
    nonce_start = settings.MINER_NONCE_START
    nonce_stop = settings.MINER_NONCE_STOP
    nonce_step = settings.MINER_NONCE_STEP
    while data == tuple():
        data = sha256(block, nonce_start=nonce_start,
                      nonce_stop=nonce_stop, nonce_step=nonce_step, difficulty=settings.HASH_DIFFICULTY)
        nonce_start = nonce_stop + nonce_step
        nonce_stop = 2 * nonce_stop
    print(data[0])
