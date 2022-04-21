from ripda import __version__
from ripda.conf import settings

import json
import asyncio
import hashlib
from datetime import datetime
from uuid import UUID
from tqdm import tqdm

from sqlmodel.ext.asyncio.session import AsyncSession

from ripda.db.models import Block
from ripda.db.session import create as create_session

from ecutils import ECDSA, ECK
from typing import List
from sqlmodel import select

from ripda.db.models import Transaction


async def _main(**kwargs) -> None:
    """
    organiza as transações em blocos
    :param kwargs:
    """
    if kwargs.get('display_information', True):
        print(datetime.now().strftime("%B %d, %Y - %H:%M:%S"))
        print(f"Ripda version {__version__}, using settings '{settings.SETTINGS_MODULE}'")

    maker = kwargs.get('maker', None)

    if maker is None:
        print(f"ValueError maker {maker}")
        return

    try:
        UUID(maker, version=5)
    except ValueError:
        print(f"ValueError maker {maker}")
        return

    if kwargs.get('display_information', True):
        print(f"Miner maker at {maker}")

    session: AsyncSession = create_session()

    """
    selecione as primeiras 100 transações que ainda não possuem blocos
    """

    query = select(
        Transaction
    ).where(
        Transaction.blocks == None
    ).offset(0).limit(100).order_by(
        Transaction.timestamp.asc()
    )

    results = await session.exec(query)  # Objeto iterável
    results: List[Transaction] = results.unique().all()  # Lista

    await session.close()

    if len(results) == 100:

        transactions = list()
        transactions_invalid = list()

        for _transaction in tqdm(results, desc='verify_signature         ', colour='WHITE'):

            ecdsa = ECDSA(curve='secp521r1')
            eck = ECK(curve='secp521r1')

            data = f'{_transaction.send}{_transaction.receive}{_transaction.data}{_transaction.timestamp}'.encode(
                'utf-8')
            data = eck.encode(hashlib.sha256(data).hexdigest())
            data = data[0] - data[2]

            r, s = _transaction.signature.split(',')
            x, y = _transaction.public_key.split(',')

            # a assinatura digital da transação é válida?
            verify_signature = ecdsa.verify_signature(data, int(r, 16), int(s, 16), (int(x, 16), int(y, 16)))

            if verify_signature:
                transactions.append(_transaction)
            else:
                transactions_invalid.append(_transaction)

        """
        obter o hash do último bloco
        """
        session: AsyncSession = create_session()

        query = select(Block.hash).offset(0).limit(1).order_by(
            Block.id.desc()
        )

        results = await session.exec(query)
        results: List[Block] = results.unique().all()

        last_hash = None
        if results:
            last_hash = results[0]

        await session.close()

        block: Block = Block()

        block.last_hash = last_hash
        block.maker = maker

        for transaction in tqdm(transactions, desc='block.transactions.append', colour='WHITE'):
            block.transactions.append(transaction)

        _block = dict()
        _block['last_hash'] = block.last_hash
        _block['transactions'] = [
            {
                'id': trans.id,
                'send': trans.send,
                'receive': trans.receive,
                'data': trans.data,
                'timestamp': trans.timestamp,
                'public_key': trans.public_key,
                'signature': trans.signature,
            } for trans in block.transactions
        ]
        _block['timestamp'] = int(datetime.timestamp(datetime.now()))
        _block['maker'] = block.maker

        """
        crie o hash para o bloco coletado.
        """
        hash = str()
        nonce = settings.MINER_NONCE_START
        while not hash.startswith('0' * int(settings.HASH_DIFFICULTY)):
            _block['nonce'] = round(nonce, 9)
            hash = hashlib.sha256(f'{json.dumps(_block)}'.encode('utf-8')).hexdigest()
            nonce += settings.MINER_NONCE_STEP
            if nonce >= settings.MINER_NONCE_STOP:
                kwargs['display_information'] = False
                return await _main(**kwargs)
            print(hash, end='\r')
        _block['hash'] = hash

        block.timestamp = _block['timestamp']
        block.nonce = _block['nonce']
        block.hash = _block['hash']

        """
        adicionar o bloco a lista
        """
        session: AsyncSession = create_session()
        session.add(block)
        await session.commit()
        await session.close()

    await asyncio.sleep(1)
    kwargs['display_information'] = False
    return await _main(**kwargs)


def main(**kwargs) -> None:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main(**kwargs))
