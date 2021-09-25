import aiofiles
import json
import pathlib
from ripda.manages.singleton import Singleton
from ripda import settings


class Database(metaclass=Singleton):
    """
    Gerencia a conexão do banco de dados.

    Permite escrever e ler.
    """

    def cquery(self: object, start: int = 0, stop: int = 100, step: int = 1) -> dict:

        if abs(start - stop) > 100 or (start > stop):
            return dict()

        __query__ = tuple(int(x.name) for x in pathlib.Path(settings.BLOCKS_DIR).glob(
            '[!_]*') if x.is_dir() and (int(x.name) >= start and int(x.name) <= stop) and (not int(x.name) % step))

        if len(__query__) == 0:
            return dict()

        __return__ = dict()

        for __id__ in __query__:
            __data__ = self.cread(__id__)
            __return__[__id__] = __data__

        return __return__

    async def query(self: object, start: int = 0, stop: int = 100, step: int = 1) -> dict:

        if abs(start - stop) > 100 or (start > stop):
            return dict()

        __query__ = tuple(int(x.name) for x in pathlib.Path(settings.BLOCKS_DIR).glob(
            '[!_]*') if x.is_dir() and (int(x.name) >= start and int(x.name) <= stop) and (not int(x.name) % step))

        if len(__query__) == 0:
            return dict()

        __return__ = dict()

        for __id__ in __query__:
            __data__ = await self.read(__id__)
            __return__[__id__] = __data__

        return __return__

    def cwrite(self: object, __id__: int, __hash__: str, __data__: dict) -> bool:
        # Cria o __id__ caso não exista
        [x.mkdir(parents=True, exist_ok=True)
         for x in (settings.BLOCKS_DIR / f'{__id__}',)]
        try:
            # Salva as informações
            with open(settings.BLOCKS_DIR / f"{__id__}/{__hash__}.json", mode='w') as __open:
                __open.write(json.dumps(__data__))
            return True
        except:
            False

    async def write(self: object, __id__: int, __hash__: str, __data__: dict) -> bool:
        # Cria o __id__ caso não exista
        [x.mkdir(parents=True, exist_ok=True)
         for x in (settings.BLOCKS_DIR / f'{__id__}',)]
        try:
            # Salva as informações
            async with aiofiles.open(settings.BLOCKS_DIR / f"{__id__}/{__hash__}.json", mode='w') as open:
                await open.write(json.dumps(__data__))

            return True
        except:
            False

    def cread(self: object, __id__: int) -> dict:
        __hash__ = tuple(x.name for x in pathlib.Path(
            settings.BLOCKS_DIR / f"{__id__}/").glob('[!_]*') if x.is_file() and x.name.endswith('.json'))

        if len(__hash__) == 0:
            return dict()

        if len(__hash__) > 1:

            # Existe um conflito entre os blocos, verifique qual é válido antes de prosseguir.
            return dict()

        __hash__ = __hash__[0]
        try:
            with open(settings.BLOCKS_DIR / f"{__id__}/{__hash__}", mode='r') as __open:
                try:
                    __json__ = json.loads(__open.read())
                except:
                    return dict()
            return __json__
        except:
            return dict()

    async def read(self: object, __id__: int) -> dict:

        __hash__ = tuple(x.name for x in pathlib.Path(
            settings.BLOCKS_DIR / f"{__id__}/").glob('[!_]*') if x.is_file() and x.name.endswith('.json'))

        if len(__hash__) == 0:
            return dict()

        if len(__hash__) > 1:

            # Existe um conflito entre os blocos, verifique qual é válido antes de prosseguir.
            return dict()

        __hash__ = __hash__[0]

        try:
            async with aiofiles.open(settings.BLOCKS_DIR / f"{__id__}/{__hash__}", mode='r') as open:
                try:
                    __json__ = json.loads(await open.read())
                except:
                    return dict()
            return __json__
        except:
            return dict()


if __name__ == '__main__':
    pass
    """
    import asyncio
    from ripda.core.block import Block
    
    for i in range (0, 10000):
        asyncio.run(db.write(i, '000097a1a8f553e494a9c6f0c9edabd0d756c73e9e4819bbb439ecba011184e2', Block().repr()))
    print(asyncio.run(db.read(1)))
    print((asyncio.run(db.query(10, 100))))

    from ripda.core.block import Block
    db = Database()
    print(db.cread(0))
    print(db.cwrite(-1, '000097a1a8f553e494a9c6f0c9edabd0d756c73e9e4819bbb439ecba011184e2', Block().repr()))
    print(db.cquery(0, 10))
    """
