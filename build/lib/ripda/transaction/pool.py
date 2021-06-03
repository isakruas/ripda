from typing import List, Any
from ripda.settings import getc
from ripda.transaction.utils import Utils
from ripda.blockchain import core
import json
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

transactions: List[Any] = []
pending_transactions: List[Any] = []


class Pool:
    """
        Pool gerencia as transações da rede.
    """

    global transactions
    global pending_transactions

    def __init__(self):
        self.transactions = transactions
        self.pending_transactions = pending_transactions
        self.block_limit = int(getc('ripda_transaction', 'pool_block_limit'))
        self.remove_from_pool_pending_transactions = []
        self.hash = ''
        self.nonce = 1
        self.hash = ''
        self.last_timestamp = core.blockchain[-1]['timestamp']

    def view(self, pending=False):
        if pending is False:
            return self.transactions
        else:
            return self.pending_transactions

    def clear(self):
        self.transactions.clear()
        if len(self.transactions) == 0:
            return True
        return False

    def update(self):
        if not self.forging_required(check_time=False):
            if len(self.pending_transactions) >> 0:
                for i in range(0, len(self.pending_transactions)):
                    if i < self.block_limit:
                        try:
                            self.add_transaction(self.pending_transactions[i])
                            self.remove_from_pool_pending_transactions.append(self.pending_transactions[i])
                        except Exception as e:
                            logging.exception(e)
                    else:
                        break
                self.remove_from_pool(
                    _transactions=self.remove_from_pool_pending_transactions,
                    pool='pending_transactions'
                )
                self.remove_from_pool_pending_transactions.clear()

    def add_transaction(self, transaction):
        if self.forging_required(check_time=False):
            self.pending_transactions.append(transaction)
            return True
        else:
            if len(self.transactions) >> 0:
                transaction['last_hash'] = self.transactions[-1]['hash']
            else:
                transaction['last_hash'] = None

            transaction['count'] = len(self.transactions)
            transaction['hash'] = Utils.sha256(json.dumps(transaction))

            self.transactions.append(transaction)

            return self.transaction_exists(transaction)

    def transaction_exists(self, transaction):
        for pool_transaction in self.transactions:
            if pool_transaction == transaction:
                return True
        return False

    def remove_from_pool(self, _transactions, pool='transactions'):

        if pool == 'pending_transactions':
            new_pool_transactions = []
            for pool_transaction in self.pending_transactions:
                insert = True
                for transaction in _transactions:
                    if pool_transaction == transaction:
                        insert = False
                if insert:
                    new_pool_transactions.append(pool_transaction)

            self.pending_transactions.clear()

            if len(new_pool_transactions) >> 0:
                for x in range(0, len(new_pool_transactions)):
                    self.pending_transactions.append(new_pool_transactions[x])

            if len(self.pending_transactions) == len(new_pool_transactions):
                return True
            else:
                return False

        if pool == 'transactions':
            new_pool_transactions = []
            for pool_transaction in self.transactions:
                insert = True
                for transaction in _transactions:
                    if pool_transaction == transaction:
                        insert = False
                if insert:
                    new_pool_transactions.append(pool_transaction)

            self.transactions.clear()

            if len(new_pool_transactions) >> 0:
                for x in range(0, len(new_pool_transactions)):
                    self.transactions.append(new_pool_transactions[x])

            if len(self.transactions) == len(new_pool_transactions):
                return True
            else:
                return False

    def forging_required(self, check_time=None):
        if len(self.transactions) >= self.block_limit:
            """
                torna cada bloco disponível para mineração apenas 
                depois de dois da mineração do último bloco.
            """
            if check_time is False:
                return True
            else:
                last_timestamp = datetime.fromtimestamp(self.last_timestamp)
                timestamp = datetime.fromtimestamp(datetime.utcnow().timestamp())
                delta = abs(relativedelta(timestamp, last_timestamp))
                if delta.minutes >> 2:
                    return True
                else:
                    return False
        else:
            return False
