import json
from ripda.manages.singleton import Singleton


class Block(metaclass=Singleton):
    def __init__(self, **kwds) -> None:
        for k, v in kwds.items():
            setattr(self, f'__{k}', v)

    def repr(self) -> dict:
        return {
            # Hash do último bloco
            'last_hash': str(),
            # Resumos
            'abstract': {
                # Resumos das transações realizadas
                'transactions': {
                    # Número de transações realizadas no bloco
                    'count': int(),
                    # Valor total transacionado no bloco
                    'amount': float(),
                }
            },
            # Lista de transações realizadas
            'transactions': [
                {
                    # Hash da ultima transação
                    'last_hash': str(),
                    # Número de ordenação da transação
                    'count': int(),
                    # Dados da transação
                    'data': {
                        # Remetente  da ordem
                        'sender': str(),
                        # Chave pública usada para assinar a transação
                        'sender_public_key': str(),
                        # Destinatário da ordem
                        'receiver': str(),
                        # Valor transacionado
                        'amount': float(),
                        # Tempo da assinatura da transação
                        'timestamp': int(),
                        # Assinatura da transação
                        'signature': str(),
                        # Hash da ultima transação
                        'last_hash': str(),
                        # Hash do último bloco
                        'last_block_hash': str(),
                    },
                    # Parâmetro arbitrário usado para obtenção do hash
                    'nonce': float(),
                    # Hash da transação
                    'hash': str(),
                },
            ],
            # Endereço responsável por organizar as informações no bloco
            'forging': str(),
            # Hora em que o bloco foi criado
            'timestamp': int(),
            # Número de ordem do bloco
            'count': int(),
            # Parâmetro arbitrário usado para obtenção do hash
            'nonce': float(),
            # Hash do bloco
            'hash': str(),
        }

if __name__ == '__main__':

    b = Block()

    print(json.dumps(b.repr(), indent=4))
