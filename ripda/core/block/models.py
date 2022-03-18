import json
from abc import ABCMeta, abstractmethod
from typing import Type


class BlockModel(metaclass=ABCMeta):

    def __init__(self, count=int(), last_hash=str(), transactions=None, maker=str()) -> None:
        if transactions is None:
            transactions = list()
        self.__count = count
        self.__last_hash = last_hash
        self.__transactions = transactions
        self.__timestamp = float()
        self.__maker = maker
        self.__hash = str()

    def __repr__(self) -> dict:
        return {
            'count': self.__count,
            'last_hash': self.__last_hash,
            'transactions': self.__transactions,
            'timestamp': self.__timestamp,
            'maker': self.__maker,
            'hash': self.__hash,
        }

    def __str__(self) -> str:
        return json.dumps(self.__repr__())

    def get_count(self) -> int:
        return self.__count

    def set_count(self, value) -> None:
        if isinstance(value, int):
            self.__count = value
        else:
            raise ValueError(
                "Couldn't set count"
            )

    def get_last_hash(self) -> str:
        return self.__last_hash

    def set_last_hash(self, value) -> None:
        if isinstance(value, str):
            self.__last_hash = value
        else:
            raise ValueError(
                "Couldn't set last_hash"
            )

    def get_transactions(self) -> Type[list]:
        return self.__transactions

    def set_transactions(self, value) -> None:
        if isinstance(value, list):
            self.__transactions = value
        else:
            raise ValueError(
                "Couldn't set transactions"
            )

    def get_timestamp(self) -> float:
        return self.__timestamp

    def set_timestamp(self, value) -> None:
        if isinstance(value, float):
            self.__timestamp = value
        else:
            raise ValueError(
                "Couldn't set timestamp"
            )

    def get_maker(self) -> str:
        return self.__maker

    def set_maker(self, value) -> None:
        if isinstance(value, str):
            self.__maker = value
        else:
            raise ValueError(
                "Couldn't set maker"
            )

    def get_hash(self) -> str:
        return self.__last_hash

    def set_hash(self, value) -> None:
        if isinstance(value, str):
            self.__hash = value
        else:
            raise ValueError(
                "Couldn't set hash"
            )

    @abstractmethod
    def make(self):
        pass
