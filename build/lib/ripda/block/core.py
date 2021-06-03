import json
from datetime import datetime
from ripda.transaction.utils import Utils
from ripda.blockchain.core import Blockchain
from ripda.settings import getc


if not __name__ == "__main__":
    if not __name__ == 'ripda.transaction.pool':
        from ripda.transaction.pool import Pool


class Block:
    """
        Block é responsável por gerar o bloco de origem, bem como retornar o próximo bloco a ser validado na rede
        e verificar se um hash gerado é válido.
    """

    def __init__(self):
        self.difficulty = '0' * int(getc('ripda_block', 'core_difficulty'))
        self.count = len(Blockchain().view())
        self.transactions = Pool().view()
        self.timestamp = datetime.utcnow().timestamp()
        self.forger = Pool().forging_required()
        self.nonce = None
        self.hash = None
        self.block = {}
        """
            Se não houver nenhum bloco na cadeia, criar o bloco de origem.
        """
        if len(Blockchain().view()) == 0:
            self.last_hash = None
            self.transactions = []
            self.create_genesis_block()
        else:
            self.last_hash = Blockchain().view()[-1]['hash']

    def view(self):
        """
            Retorna a estrutura do bloco candidato a ser o próximo a
            ser adicionado à cadeia de blocos
        """
        abstract_transactions_amount = 0
        if len(self.transactions) >> 0:
            for transaction in self.transactions:
                abstract_transactions_amount += transaction['amount']
        block = {
            'last_hash': self.last_hash,
            'count': self.count,
            'abstract':{
                'transactions': {
                    'count': len(self.transactions),
                    'amount': abstract_transactions_amount
                }
            },
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'forger': self.forger,
        }
        self.block = block
        return block

    def create_genesis_block(self):
        """
            Cria o bloco de origem
        """
        self.hash = ''
        self.nonce = 1
        block = {}
        while not self.is_hash_valid(self.hash):
            block = {
                'last_hash': self.last_hash,
                'count': self.count,
                'abstract':{
                    'transactions': {
                        'count': 0,
                        'amount': 0
                    }
                },
                'transactions': self.transactions,
                'timestamp': self.timestamp,
                'nonce': self.nonce,
                'forging': '1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU'
            }
            self.hash = Utils.sha256(json.dumps(block))
            self.nonce += 1
        block['hash'] = self.hash
        return Blockchain().add_block(block)

    def is_hash_valid(self, _hash):
        """
            Verifica se o hash informado é valido
        """
        return _hash.startswith(self.difficulty)
