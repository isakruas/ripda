import asyncio
import hashlib
from datetime import datetime

from tqdm import tqdm
from uuid import uuid4
from sqlmodel.ext.asyncio.session import AsyncSession

from ripda.db.models.transaction import Transaction
from ripda.db.session import create as create_session

from ripda.utils.functools import random_address

from ecutils import ECDSA, ECK

"""
cria uma sequência de blocos e transações banco de dados.
função usada apenas para desenvolvimento.
"""


async def _main(**kwargs) -> None:
    """
    Popular banco de dados com dados fakes
    :param kwargs:
    """

    session: AsyncSession = create_session()

    for __ in tqdm(range(1, 1001), desc='Transaction', colour='WHITE'):
        data = int(uuid4())

        send = await random_address()
        receive = await random_address()

        timestamp = int(datetime.timestamp(datetime.now()))
        private_key = int(send[0], 16)

        ecdsa = ECDSA(curve='secp521r1', private_key=private_key)
        eck = ECK(curve='secp521r1')

        _data = eck.encode(
            hashlib.sha256(f'{send[1]}{receive[1]}{data}{timestamp}'.encode('utf-8')).hexdigest()
        )
        _data = _data[0] - _data[2]

        r, s = ecdsa.signature(_data)
        x, y = ecdsa.public_key

        transaction: Transaction = Transaction(
            send=send[1],
            receive=receive[1],
            data=str(data),
            timestamp=timestamp,
            public_key=f'{hex(x)[2:]},{hex(y)[2:]}',
            signature=f'{hex(r)[2:]},{hex(s)[2:]}',
        )

        session.add(transaction)

    await session.commit()
    await session.close()


def main(**kwargs) -> None:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main(**kwargs))
