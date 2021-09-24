import codecs
import json
from typing import List, Any
import os
import ecdsa
from ripda.blockchain.utils import Utils
from ripda.settings import getc
from ripda.transaction.pool import Pool

blockchain: List[Any] = []
wallet = {}

"""
    verifique se, dado uma assinatura e uma chave pública,
    a assinatura pertence à chave pública
"""


def is_signature_valid(transaction, signature, sender_public_key):
    try:
        signature = bytearray.fromhex(signature)
        transaction_sha256_ripemd160 = Utils.ripemd160(Utils.sha256(json.dumps(transaction)))
        transaction = codecs.decode(transaction_sha256_ripemd160.encode('utf-8'), 'hex')
        public_key = ecdsa.VerifyingKey.from_string(bytearray.fromhex(sender_public_key), curve=ecdsa.NIST521p)
        try:
            public_key.verify(signature, transaction)
            return True
        except NameError:
            return False
    except NameError:
        return False


class Blockchain:
    """
        Blockchainn é responsável por verificar se um bloco extraído é válido e adicionar este bloco extraído à
        cadeia de blocos. Esta classe também retorna todos os blocos já validados e incluídos na rede.
    """
    global blockchain
    global wallet

    def __init__(self):
        self.blockchain = blockchain
        self.wallet = wallet
        self.difficulty = '0' * int(getc('ripda_block', 'core_difficulty'))
        self.block = []
        """
            A taxa é cobrada, em porcentagem, de cada transação realizada na rede é 0.04%
        """
        self.fee = 0.04
        self.path = str(getc('ripda', 'path_blocks'))
        if len(self.blockchain) == 0:
            blocks = os.listdir(self.path)
            if 'wallets.r' in blocks:
                blocks.remove('wallets.r')
                os.remove(self.path + 'wallets.r')
                pass

            if len(blocks) >> 0:
                for block in sorted(blocks):
                    with open(self.path + block) as e:
                        r = json.loads(e.read())
                    self.add_block(r, sync=True)

    def view(self):
        """
            Retorna todos os blocos na cadeia de blocos.
            Esta função pode retornar um grande json.
        """
        return self.blockchain

    def add_block(self, block, sync=False):
        """
            Crie uma cópia do bloco recibo
        """
        self.block = block.copy()
        """
            Se houver mais de três blocos gerados,
            não permitir a adição de um novo bloco com transações nulas.
        """
        if len(self.blockchain) >> 0:
            if self.block['count'] >> 3:
                if len(self.block['transactions']) == 0:
                    return False
        abstract_transactions_amount = 0
        last_hash = None
        """
            Verificar as transações do bloco.
        """
        if len(self.block['transactions']) >> 0:
            """
                Percorrer todas as transações.
            """
            for transaction in self.block['transactions']:
                """
                    Adicionar o valor transacionado na soma total,
                    para verificaçẽo posterior.
                """
                abstract_transactions_amount += transaction['amount']
                """
                    Se houver divergencia entre os hash do block,
                    recusar o bloco
                """
                if not transaction['last_hash'] == last_hash:
                    return False
                """
                    configurar a transação no formato adequado,
                    para verificação da assinatura.
                """
                _transaction = {
                    'sender': transaction['sender'],
                    'receiver': transaction['receiver'],
                    'amount': transaction['amount'],
                    'timestamp': transaction['timestamp']
                }
                """
                    Verifica se a assinatura da transação é valida,
                    caso não seja, recusa o bloco.
                """
                if is_signature_valid(_transaction, transaction['signature'],
                                      transaction['sender_public_key']) is False:
                    """
                        Se houver alguma discrepância na assinatura,
                        recuse todo o bloco recebido.
                    """
                    return False
                last_hash = transaction['hash']

        if not self.block['abstract']['transactions']['count'] == len(self.block['transactions']):
            """
                Se o número de transações detectadas for diferente do número de
                transações informado, recuse o bloco inteiro.
            """
            return False

        if not self.block['abstract']['transactions']['amount'] == abstract_transactions_amount:
            """
                Caso haja alguma discrepância no valor da soma identificado
                com o valor da soma informada,
                recusar todo o bloco recebido.
            """
            return False
        """
            Prepara o esqueleto do bloco para verificação posterior.
        """
        _block = {
            # hash do último bloco
            'last_hash': self.block['last_hash'],
            # número do índice do bloco
            'count': self.block['count'],
            # resumo do bloco
            'abstract': {
                'transactions': {
                    'count': len(self.block['transactions']),
                    'amount': abstract_transactions_amount
                }
            },
            # transações realizadas no bloco
            'transactions': self.block['transactions'],
            # hora em que o bloco foi obtido
            'timestamp': self.block['timestamp'],
            # valor de verificação de hash de bloco
            'nonce': self.block['nonce'],
            # carteira do minerador responsável por organizar o bloco
            'forging': self.block['forging']
        }
        """
            Caso não seja o bloco de gênese,
            verifique se a corrente é válida
        """
        if len(self.blockchain) >> 0:
            if self.blockchain[-1]['hash'] != self.block['last_hash']:
                """
                    Se houver divergência na cadeia,
                    recuse todo o bloco.
                """
                return False
        """
            Verifica se o hash do esqueleto do bloco é idêntico ao hash
            relatado pelo minerador, caso contrário, recuse todo bloco.
        """
        if Utils.sha256(json.dumps(_block)) == self.block['hash']:
            """
                Verifique se o hash está no formato aceito pela padronização,
                caso contrário, recuse todo bloco.
            """
            if Utils().is_hash_valid(self.block['hash']):
                """
                    Como o bloco passou em todos os testes de verificação,
                    eu o adiciono ao blockchain.
                """
                self.blockchain.append(self.block)
                """
                    Atualizar valores de carteira salvos localmente
                """
                if len(self.block['transactions']) >> 0:
                    for transaction in self.block['transactions']:
                        self.wallet[transaction['sender']]['amount'] -= float(transaction['amount'])
                        self.wallet[transaction['sender']]['amount'] = round(self.wallet[transaction[
                            'sender']]['amount'], 8)

                        if transaction['receiver'] in self.wallet:
                            self.wallet[transaction['receiver']]['amount'] += float(transaction['amount'] * (1 - self.fee))
                            self.wallet[transaction['receiver']]['amount'] = round(self.wallet[transaction[
                                'receiver']]['amount'], 8)
                        else:
                            self.wallet[transaction['receiver']] = {}
                            self.wallet[transaction['receiver']]['amount'] = float(transaction['amount'] * (1 - self.fee))
                            self.wallet[transaction['receiver']]['amount'] = round(self.wallet[transaction[
                                'receiver']]['amount'], 8)

                        if self.block['forging'] in self.wallet:
                            self.wallet[self.block['forging']]['amount'] += float(transaction['amount'] * self.fee)
                            self.wallet[self.block['forging']]['amount'] = round(self.wallet[self.block[
                                'forging']]['amount'], 8)
                        else:
                            self.wallet[self.block['forging']] = {}
                            self.wallet[self.block['forging']]['amount'] = float(transaction['amount'] * self.fee)
                            self.wallet[self.block['forging']]['amount'] = round(self.wallet[self.block[
                                'forging']]['amount'], 8)

                """
                    Limita a quantidade à quantidade máxima de Ripdas que podem ser geradas
                    (99999999+1)*0.04 representa o limite de Ripdas que pode ser geradas
                """
                if self.block['count'] <= 99999999:
                    if self.block['forging'] in self.wallet:
                        self.wallet[self.block['forging']]['amount'] += float(0.04)
                        self.wallet[self.block['forging']]['amount'] = round(self.wallet[self.block[
                            'forging']]['amount'], 8)
                    else:
                        self.wallet[self.block['forging']] = {}
                        self.wallet[self.block['forging']]['amount'] = float(0.04)
                        self.wallet[self.block['forging']]['amount'] = round(self.wallet[self.block[
                            'forging']]['amount'], 8)

                _path_wallet = self.path + 'wallets.r'
                g = open(_path_wallet, 'w')
                g.write(json.dumps(self.wallet, indent=4))
                g.close()
                """
                    Se não for uma chamada de sincronização,
                    salvar o bloco adicionado em um arquivo localmente,
                    para facilitar a reinicialização do sistema em um momento futuro.
                """
                _path = self.path + str(self.block['timestamp']) + '.r'
                if not sync:
                    f = open(_path, 'w')
                    """
                        Arquivo compactado
                    """
                    f.write(json.dumps(self.block))
                    """
                    f.write(json.dumps(self.block, indent=4))
                    
                    """
                    f.close()
                """
                    Limpe a lista de transações que estavam no 
                    último bloco, presentes no Pool.
                """
                if Pool().clear():
                    """
                        Verifica se, enquanto este Pool estava realizando a 
                        verificação do bloco atual, novas transações foram adicionados ao Pool
                    """
                    Pool().update()
                    return self.block
                else:
                    """
                        Se ocorrer alguma falha, descartar o bloco.
                    """
                    self.blockchain.remove(self.block)
                    if os.path.exists(_path):
                        os.remove(_path)
                    return False
            return False
        return False
