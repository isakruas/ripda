from ripda.db.engine import create as create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from typing import Optional
from ripda.conf import settings

__async_engine: Optional[AsyncEngine] = None


def create(**kwargs) -> AsyncSession:
    """

    :param kwargs:
    :return:
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

    session: AsyncSession = AsyncSession(__async_engine)

    return session

