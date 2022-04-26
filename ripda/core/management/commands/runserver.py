from ripda import __version__
from ripda.conf import settings
from ripda.db.session import create as create_session

import hashlib
import importlib
import logging
from datetime import datetime

from ecutils import (
    ECK,
    ECDSA,
)

import uvicorn
from fastapi import FastAPI

from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncEngine

__async_engine: Optional[AsyncEngine] = None

app = FastAPI(docs_url=None, redoc_url=None)

from sqlmodel.sql.expression import Select, SelectOfScalar
from typing import List
from sqlmodel import select

from ripda.db.models import Block
from ripda.db.models.transaction import Transaction

SelectOfScalar.inherit_cache = False  # type: ignore
Select.inherit_cache = False  # type: ignore

"""
Conjunto de endpoints básicos para funcionamento do sistema.
"""


@app.get('/blocks')
async def blocks(offset: int = 0, limit: int = 10):
    """
    retorna lista de blocos validados
    :param offset:
    :param limit:
    :return: List[Block]
    """
    async with create_session() as session:
        query = select(Block).offset(offset).limit(limit)
        results = await session.exec(query)
        results: List[Block] = results.unique().all()
        if results:
            _results = list()
            for item in results:
                _results.append({
                    'id': item.id,
                    'last_hash': item.last_hash,
                    'transactions': item.transactions,
                    'nonce': item.nonce,
                    'timestamp': item.timestamp,
                    'maker': item.maker,
                    'hash': item.hash,
                })
            return _results
        return [
            {
                'id': None,
                'last_hash': None,
                'transactions': None,
                'nonce': None,
                'timestamp': None,
                'maker': None,
                'hash': None,
            }
        ]


@app.get('/blocks/{id}/')
async def blocks_by_id(id: int):
    """
    retorna bloco validado
    :param id:
    :return: Block
    """
    async with create_session() as session:
        query = select(Block).where(Block.id == id)
        results = await session.exec(query)
        results: List[Block] = results.first()
        if results:
            _results = list()
            _results.append({
                'id': results.id,
                'last_hash': results.last_hash,
                'transactions': results.transactions,
                'nonce': results.nonce,
                'timestamp': results.timestamp,
                'maker': results.maker,
                'hash': results.hash,
            })
            return _results
        return [
            {
                'id': None,
                'last_hash': None,
                'transactions': None,
                'nonce': None,
                'timestamp': None,
                'maker': None,
                'hash': None,
            }
        ]


@app.get('/transactions')
async def transactions(offset: int = 0, limit: int = 100, merged: bool = False):
    """
    todas as transações de todos os blocos
    :param merged:
    :param offset:
    :param limit:
    :return: List[Transaction]
    """
    async with create_session() as session:
        query = select(
            Transaction
        )
        if merged is False:
            query = query.where(
                Transaction.blocks == None # lgtm [py/test-equals-none]
            )
        query = query.offset(offset).limit(limit).order_by(
            Transaction.timestamp.asc()
        )
        results = await session.exec(query)  # Objeto iterável
        results: List[Transaction] = results.unique().all()  # Lista
        if results:
            return results
        return Transaction()


@app.post('/transactions')
async def transactions(transaction: Transaction):
    """
    verifica se a transação é válida e, em caso afirmativo, adiciona-a à fila de transações
    :param transaction: Transaction
    :return: Transaction
    """
    try:

        ecdsa = ECDSA(curve='secp521r1')
        eck = ECK(curve='secp521r1')

        data = eck.encode(
            hashlib.sha256(f'{transaction.send}{transaction.receive}{transaction.data}{transaction.timestamp}'.encode('utf-8')).hexdigest()
        )

        data = data[0] - data[2]

        r, s = transaction.signature.split(',')
        x, y = transaction.public_key.split(',')

        # a assinatura digital da transação é válida?
        verify_signature = ecdsa.verify_signature(data, int(r, 16), int(s, 16), (int(x, 16), int(y, 16)))

        if not verify_signature:
            raise ValueError('invalid transaction')

        # enviar a transação para o banco
        async with create_session() as session:

            session.add(transaction)

            await session.commit()
            await session.refresh(transaction)

            return transaction

    except Exception as exc:
        """
        se a transação já existir, ou se houver erro na verificação, retorne o erro.
        """
        logging.info(exc)

        return {
            'detail': [
                {
                    'msg': 'invalid transaction',
                    'type': "validation_error"
                }
            ]
        }


@app.get('/transactions/{id}/')
async def transactions_by_id(id: int):
    """
    retorna uma transação específica realizada
    :param id:
    :return:
    """
    async with create_session() as session:
        query = select(Transaction).where(Transaction.id == id)
        results = await session.exec(query)
        results: List[Transaction] = results.first()
        if results:
            return results
        return Transaction()


"""
importe todas as funções suplementares para a rotina principal.
"""
md = settings.HANDLER_MODULE
if md:
    importlib.import_module(md)


def main(**kwargs):
    """
    executa o aplicativo
    :param kwargs:
    """
    host = settings.NODE_HOST
    port = settings.NODE_PORT

    if 'host' in kwargs and 'port' in kwargs:
        host = kwargs['host']
        port = int(kwargs['port'])

    print(datetime.now().strftime("%B %d, %Y - %H:%M:%S"))
    print(f"Ripda version {__version__}, using settings '{settings.SETTINGS_MODULE}'")
    uvicorn.run(f'{__name__}:app', host=host, port=port, log_level='info', reload=True, workers=2)
