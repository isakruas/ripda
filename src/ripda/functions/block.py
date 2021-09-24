from datetime import datetime
from ripda.functions.miner import sha256
from ripda import settings

def create_genesis(forging: str) -> dict:
    """
    Crie o bloco gênesis da rede
    """
    block = {
        'last_hash': None,
        'count': 0,
        'abstract': {
            'transactions': {
                'count': 0,
                'amount': 0
            }
        },
        'transactions': [],
        'timestamp': datetime.utcnow().timestamp(),
        'forging': forging
    }
    data = tuple()
    nonce_start = settings.MINER_NONCE_START
    nonce_stop = settings.MINER_NONCE_STOP
    nonce_step = settings.MINER_NONCE_STEP
    while data == tuple():
        data = sha256(block, nonce_start=nonce_start,
                      nonce_stop=nonce_stop, nonce_step=nonce_step, difficulty=settings.HASH_DIFFICULTY)
        nonce_start = nonce_stop + nonce_step
        nonce_stop = 2 * nonce_stop
    return data[0]
