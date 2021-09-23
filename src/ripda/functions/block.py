from datetime import datetime
from ripda.functions.miner import sha256


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
    nonce_start = 0.0
    nonce_stop = 100.0
    nonce_step = 0.001
    while data == tuple():
        data = sha256(block, nonce_start=nonce_start,
                      nonce_stop=nonce_stop, nonce_step=nonce_step, difficulty=4)
        nonce_start = nonce_stop + nonce_step
        nonce_stop = 2 * nonce_stop
    return data[0]
