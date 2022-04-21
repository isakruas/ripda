Configurações
=============




Como configurar um aplicativo na utilizando a estrutura do Ripda?


O aplicativo Ripda modelo possui quatro arquivos, ``manage.py`` que é utilizado para execução dos comandos principais, ``models.py`` no qual você pode definir novos modelos a serem criados no banco de dados, para extender a aplicação, ``urls.py``, que você pode utilizar para criar novas rotas ou adicionar novos protocolos as rotas já existentes e ``settings.py`` que você definirar todas as configurações a serem usadas pela aplicação.

``models.py``::

    from sqlmodel import Field, SQLModel

    """
    crie seus modelos aqui
    """

``urls.py``::

    from ripda import __version__
    from ripda.core.management.commands.runserver import app

    from models import *

    """
    crie suas rotas aqui
    """


    @app.get('/')
    async def root():
        return {
            'ripda': __version__
        }


``settings.py``::

    import pathlib

    HANDLER_MODULE: str = 'urls'

    MODELER_MODULE: str = 'models'

    # Diretório raiz do projeto
    BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

    # Nó em que a carteira será servida
    NODE_HOST: str = 'localhost'
    NODE_PORT: int = 1050

    # Dificuldade em encontrar um hash; é medido pela quantidade de zeros no início do hash.
    HASH_DIFFICULTY: int = 4

    # Valor inicial padrão de nonce para testar
    MINER_NONCE_START: float = 0.0

    # Valor final padrão de nonce para testar
    MINER_NONCE_STOP: float = 100.0

    # Variação numérica entre nonces
    MINER_NONCE_STEP: float = 0.001

    # PostgreSQL
    ENGINE_HOST: str = str()
    ENGINE_PORT: int = int()
    ENGINE_USER: str = str()
    ENGINE_PASSWORD: str = str()
    ENGINE_DB: str = 'ripda'


``manage.py``::

    import os
    import sys


    def main():
        os.environ.setdefault('RIPDA_SETTINGS_MODULE', 'settings')
        try:
            from ripda.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Ripda"
            ) from exc
        execute_from_command_line(sys.argv)


    if __name__ == '__main__':
        main()


Salvos estes arquivos dentro de um módulo Python, você terá à sua disposição toda estrutura blockchain montada, ponta para utilização.