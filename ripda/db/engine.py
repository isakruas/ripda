from typing import Optional

from sqlmodel import create_engine as _create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine

__async_engine: Optional[AsyncEngine] = None


def create(**kwargs) -> bool | AsyncEngine:
    """

    :param kwargs:
    :return:
    """

    global __async_engine

    if __async_engine:
        return False

    if 'engine_host' in kwargs\
            and 'engine_port' in kwargs\
            and 'engine_user' in kwargs\
            and 'engine_password' in kwargs\
            and 'engine_db' in kwargs:

        url = f'postgresql+asyncpg://{kwargs["engine_user"]}:{kwargs["engine_password"]}@{kwargs["engine_host"]}:{kwargs["engine_port"]}/{kwargs["engine_db"]}'
        __async_engine = AsyncEngine(_create_engine(url=url, echo=False))

        return __async_engine
    return False
