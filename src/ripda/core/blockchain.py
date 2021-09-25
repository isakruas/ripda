from concurrent.futures import process
from ripda.manages.singleton import Singleton
from ripda.core.network import Network
from ripda.core.database import Database
import json

"""
from functools import wraps
def run(fn):
    @wraps(fn)
    def run(self, **kwds):
        if 'def' in kwds and 'kwds' in kwds:
            # def -> Método a ser executado
            # kwds -> Parâmetros a serem passados para o método
            __def__ = kwds['def']
            __kwds__ = kwds['kwds']
            try:
                return eval(f'__{__def__}__(self, **{__kwds__})')
            except:
                pass
        return fn(self, **kwds)
    return run
"""


class Blockchain(metaclass=Singleton):

    network = Network()

    database = Database()

    def add(self, **kwds) -> bool:
        """
        Adicionar um novo bloco:
            Verifique na rede se o bloco ainda não foi adicionado.
            Se não foi adicionado, adicione o bloco e propague-o na rede.
            Acione a sincronização após o bloco ser adicionado.
        """

        def __block__(self, **kwds):
            #---------------------------------------------------------#
            if 'def' in kwds and 'kwds' in kwds:

                __def__ = kwds['def']
                __kwds__ = kwds['kwds']

                #---------------------------------------------------------#
                if __def__ == 'local' and 'block' in __kwds__:
                    """
                    Adicione um novo bloco, gerado localmente.
                    """
                    __block__ = __kwds__['block']

                    # Verifica se o bloco ainda não existe em algum dos nós conectados.
                    has_block: list = self.network.ping(**{
                        'kwds': {
                            'def': 'blockchain.verify',
                            'kwds': {
                                'def': 'block',
                                'kwds': {
                                    'def': 'is_available_locally',
                                    'kwds': {
                                        'id': int(__block__['count'])
                                    }
                                }
                            }
                        }
                    })

                    # Coleta a resposta fornecida pelos nós
                    has_block = tuple(map(lambda x: json.loads(
                        x)['return'] if isinstance(x, str) else x, has_block))

                    # Se o bloco não existe em nenhum dos outros nós
                    if not any(has_block):

                        # Salvar bloco no banco de dados localmente
                        __id__: int = int(__block__['count'])
                        __hash__: str = __block__['hash']

                        while True:
                            if self.database.cwrite(__id__, __hash__, __block__):
                                break

                        # Envia o bloco recém-adicionado localmente à rede.
                        notify: list = self.network.ping(**{
                            'kwds': {
                                'def': 'blockchain.add',
                                'kwds': {
                                    'def': 'block',
                                    'kwds': {
                                        'def': 'network',
                                        'kwds': {
                                            'block': __block__
                                        }
                                    }
                                }
                            }
                        })

                        # Invoca a sincronização.
                        self.sync()

                        return True
                    else:
                        # O bloco já existe em nenhum dos outros nós
                        return False

                if __def__ == 'network' and 'block' in __kwds__:
                    """
                    Adicione um novo bloco, recebido da rede.
                    """
                    __block__ = __kwds__['block']
                    return True  # MÉTODO NÃO IMPLEMENTADO
                #---------------------------------------------------------#
            #---------------------------------------------------------#
            return False
        #---------------------------------------------------------#
        if 'def' in kwds and 'kwds' in kwds:
            __def__ = kwds['def']
            __kwds__ = kwds['kwds']
            try:
                return eval(f'__{__def__}__(self, **{__kwds__})')
            except:
                pass
        #---------------------------------------------------------#

    def verify(self, **kwds) -> bool:
        """
        Verificar a integridade de um bloco:
            Analisar o hash, soma das transações, assinaturas das transações e etc.

        Verificar se um bloco está disponível localmente.
            Analisar no banco de dados.
        """

        def __block__(self, **kwds):
            #---------------------------------------------------------#
            if 'def' in kwds and 'kwds' in kwds:
                __def__ = kwds['def']
                __kwds__ = kwds['kwds']
                #---------------------------------------------------------#
                if __def__ == 'is_available_locally' and 'id' in __kwds__:
                    """
                    Verificar se um bloco está disponível localmente
                    """
                    # Incapaz de implementar uma verificação assíncrona do banco de dados
                    __id__ = __kwds__['id']
                    __query__ = self.database.cquery(__id__, __id__)
                    if len(__query__[__id__]) > 0:
                        return True
                    return False

                if __def__ == 'is_valid_block' and 'block' in __kwds__:
                    """
                    Verifica se o hash do esqueleto do bloco é idêntico ao hash
                    relatado pelo minerador, caso contrário, retorne false.
                    """
                    return True  # MÉTODO NÃO IMPLEMENTADO
                #---------------------------------------------------------#
            #---------------------------------------------------------#
            return False
        #---------------------------------------------------------#
        if 'def' in kwds and 'kwds' in kwds:
            __def__ = kwds['def']
            __kwds__ = kwds['kwds']
            try:
                return eval(f'__{__def__}__(self, **{__kwds__})')
            except:
                pass
        #---------------------------------------------------------#
        return False

    def fetch(self, **kwds) -> bool:
        """
        Verificar se um bloco está disponível na rede:
            Disparar ping nos nodes e captura de informações.
        """

    def repr(self) -> dict:
        """
        Crie uma representação do blockchain:
            Lista com os endereços dos últimos 1000 blocos salvos no banco de dados.

        Crie uma representação segmentada do blockchain:
            Obtenha um intervalo inicial e final de blocos e crie uma lista se os encontrar.
        """
        pass

    def sync(self) -> None:
        """
        Sincroniza o estado do banco de dados no nó com os nós conectados
        e resolve os conflitos, se houver:
            Buscar a representação dos nós conectados.
            Analise se os hashs são os mesmos.
                Se não for, escolher o mais antigo.
                Propagar o bloco válido na rede.

            Atualizar saldos nas carteiras.
            Baixe e salve os blocos que faltam.
        """
        pass

    def merge(self) -> None:
        """
        Baixe todos os blocos da rede até o bloco atual.
        Sincroniza todas as informações com o banco de dados.
        """


if __name__ == '__main__':

    blockchain = Blockchain()
    from ripda.core.block import Block

    # Verifique se um bloco está disponível localmente
    is_available_locally = blockchain.verify(**{
        'def': 'block',
        'kwds': {
            'def': 'is_available_locally',
            'kwds': {
                'id': 0  # Bloco 0
            }
        }
    })
    print(is_available_locally)

    # Verifique a integridade de um bloco
    is_valid_block = blockchain.verify(**{
        'def': 'block',
        'kwds': {
            'def': 'is_valid_block',
            'kwds': {
                'block': Block().repr()
            }
        }
    })
    print(is_valid_block)

    # Verifique a integridade de um bloco
    new_block_local = blockchain.add(**{
        'def': 'block',
        'kwds': {
            'def': 'local',
            'kwds': {
                'block': Block().repr()
            }
        }
    })

    print(new_block_local)

    new_block_network = blockchain.add(**{
        'def': 'block',
        'kwds': {
            'def': 'network',
            'kwds': {
                'block': Block().repr()
            }
        }
    })

    print(new_block_network)
