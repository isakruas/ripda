from datetime import datetime
from ripda.functions.signature import create as create_signature
from ripda.manages.singleton import Singleton
from uuid import uuid4


class Transaction(metaclass=Singleton):
    """
    Modelo de gerenciamento de dados do aplicativo Transaction
    """

    # Transações preparadas e prontas para envio à rede.
    transactions = dict()

    def repr(self) -> dict:
        """
        Retorna uma representação de todas as transações preparadas.
        """
        return self.transactions

    def get(self, **kwds) -> dict:
        """
        Retorna uma transação, da lista de preparados, cujo uid é definido
        """
        if 'uid' in kwds:
            uid = kwds['uid']
            return self.transactions.get(uid, dict())
        return dict()

    def abort(self, **kwds) -> bool:
        """
        Remover da lista de transações preparadas a transação cujo uid é definido
        """
        if 'uid' in kwds:
            try:
                uid = kwds['uid']
                del self.transactions[uid]
                return True
            except:
                return False
        return False

    def prepare(self, **kwds) -> dict:
        """
        Prepara uma transação para enviar à rede.
        """
        if 'sender' and 'receiver' and 'amount' and 'private_key' in kwds:
            sender: str = kwds['sender']
            receiver: str = kwds['receiver']
            amount: float = kwds['amount']
            private_key: str = kwds['private_key']
            timestamp: float = datetime.utcnow().timestamp()
        else:
            return dict()
        transaction: dict = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'timestamp': timestamp
        }
        signature = create_signature(transaction, private_key)
        if signature == str():
            return dict()
        transaction['signature'] = signature
        while True:
            uid = uuid4().hex
            if self.transactions.get(uid, False) is False:
                self.transactions[uid] = transaction
                transaction['uuid4'] = uid
                return transaction

    def push(self):
        """
        Envia para a rede uma transação preparada cujo id é uid e 
        remove esse uid da lista de transações preparadas.
        """
        pass
