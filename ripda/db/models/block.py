from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from pydantic import condecimal

from ripda.db.models.transaction import Transaction
from ripda.db.models.block_transaction import BlockTransaction


class Block(SQLModel, table=True):
    __tablename__ = 'blocks'

    __table_args__ = UniqueConstraint('hash'),

    id: int = Field(default=None, primary_key=True)

    last_hash: Optional[str] = Field(default=None)

    # um bloco pode ter várias transações
    transactions: List[Transaction] = Relationship(
        link_model=BlockTransaction,
        sa_relationship_kwargs={
            'lazy': 'joined',
            # 'cascade': 'delete',
        },
        back_populates='blocks'
    )

    nonce: condecimal(max_digits=99, decimal_places=9) = Field(default=0)

    timestamp: int = Field(default=None)

    maker: str = Field(default=None)

    hash: str = Field(default=None)
