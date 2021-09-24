# Em testes preliminares, usando ProcessPoolExecutor obtém melhor desempenho.
from concurrent.futures.process import ProcessPoolExecutor as Executor
# from concurrent.futures.thread import ThreadPoolExecutor as Executor
import hashlib
import json
import multiprocessing
from typing import Generator
from ripda import settings

def frange(start: float = 0.0, stop: float = 10.0, step: float = 0.1) -> Generator[float, None, None]:
    """
    Gera uma lista de números do tipo float, do start ao stop, com um intervalo de step entre números
    """
    while True:
        if start > stop:
            return
        yield start
        start = start + step


def _sha256(data: dict, sample: tuple, difficulty: int = settings.HASH_DIFFICULTY) -> str:
    """
    Ele pega os dados e uma amostra de todos os nonces
    possíveis e tenta encontrar o hash válido com a amostra recebida.
    """
    hash = str()
    for nonce in sample:
        data['nonce'] = nonce
        if not hash.startswith('0' * difficulty):
            hash = hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()
        else:
            return nonce, hash
    return hash


def sha256(data: dict = {}, nonce_start: float = settings.MINER_NONCE_START, nonce_stop: float = settings.MINER_NONCE_STOP, nonce_step: float = settings.MINER_NONCE_STEP, difficulty: int = settings.HASH_DIFFICULTY) -> tuple:
    """
    Ele pega os dados, cria uma representação dos possíveis nonces, separa os possíveis nonces em blocos, 
    de preferência igualitários, e equilibra o processamento de dados em todos os núcleos de processador disponíveis.
    """
    cpu_count = multiprocessing.cpu_count()
    sample = tuple(i for i in frange(nonce_start, nonce_stop, nonce_step))
    breaks = list()
    for i in range(1, cpu_count + 1):
        j = int(len(sample) * (i - 1) / cpu_count)
        k = int(len(sample) * i / cpu_count)
        breaks.append((j, k))
    with Executor() as executor:
        futures = list()
        for i in breaks:
            j, k = i
            futures.append(executor.submit(
                _sha256, data, sample[j:k], difficulty))
        for result in tuple(future.result() for future in futures):
            if len(result) == 2:
                nonce, hash = result
                data['nonce'] = nonce
                data['hash'] = hash
                return data,
        return tuple()
