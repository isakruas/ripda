from ripda.manages.singleton import Singleton
from ripda.core.network import Network


class Blockchain(metaclass=Singleton):

    network = Network()

    def add(self) -> bool:
        """
        Adicionar um novo bloco:
            Verifique na rede se o bloco ainda não foi adicionado.
            Se não foi adicionado, adicione o bloco e propague-o na rede.
            Acione a sincronização após o bloco ser adicionado.
        """
        pass

    def verify(self):
        """
        Verificar a integridade de um bloco:
            Analisar o hash, soma das transações, assinaturas das transações e etc.
        
        Verificar se um bloco está disponível localmente.
            Analisar no banco de dados.
        """

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
