from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint

from ripda.db.models.block_transaction import BlockTransaction


class Transaction(SQLModel, table=True):
    __tablename__ = 'transactions'

    __table_args__ = UniqueConstraint('signature'),

    id: Optional[int] = Field(default=None, primary_key=True)

    # cada transação só pode fazer parte de um único bloco
    blocks: Optional[List['Block']] = Relationship(
        link_model=BlockTransaction,
        sa_relationship_kwargs={
            'lazy': 'joined',
            # 'cascade': 'delete',
        },
        back_populates='transactions',
    )

    send: str = Field(default=None, nullable=False)

    receive: Optional[str] = Field(default=None)

    data: str = Field(default=None, nullable=False)

    timestamp: int = Field(default=None, nullable=False)

    public_key: str = Field(default=None, nullable=False)

    # só pode haver uma transação com a mesma assinatura digital.
    signature: str = Field(default=None, nullable=False)
