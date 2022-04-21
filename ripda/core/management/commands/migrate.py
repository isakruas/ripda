import asyncio
import importlib
from sqlmodel import SQLModel
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncEngine

from ripda import __version__
from ripda.conf import settings
from datetime import datetime

"""
importa quaisquer modelos extras para a rotina ser executada.
"""
md = settings.MODELER_MODULE
if md:
    importlib.import_module(md)

from ripda.db.engine import create as create_engine

__async_engine: Optional[AsyncEngine] = None


async def _main(**kwargs) -> None:
    """
    cria ou recria todas as tabelas do banco de dados.
    :param kwargs:
    """

    global __async_engine

    if not __async_engine:
        __async_engine = create_engine(**{
            'engine_host': settings.ENGINE_HOST,
            'engine_port': settings.ENGINE_PORT,
            'engine_user': settings.ENGINE_USER,
            'engine_password': settings.ENGINE_PASSWORD,
            'engine_db': settings.ENGINE_DB,
        })

    async with __async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    url = f'postgresql://{settings.ENGINE_USER}:{settings.ENGINE_PASSWORD}@{settings.ENGINE_HOST}:{settings.ENGINE_PORT}/{settings.ENGINE_DB}'

    print(datetime.now().strftime("%B %d, %Y - %H:%M:%S"))
    print(f"Ripda version {__version__}, using settings '{settings.SETTINGS_MODULE}'")
    print(f'Migrate at {url}')

    return None


def main(**kwargs) -> None:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main(**kwargs))
