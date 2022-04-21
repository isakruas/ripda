from sqlmodel import Field, SQLModel


class BlockTransaction(SQLModel, table=True):
    __tablename__ = 'blocks_transactions'

    id: int = Field(default=None, primary_key=True)

    id_block: int = Field(foreign_key='blocks.id')

    id_transaction: int = Field(foreign_key='transactions.id')

