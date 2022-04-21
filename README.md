### *Integração do núcleo Ripda*

[![Documentation Status](https://readthedocs.org/projects/ripda/badge/?version=latest)](https://ripda.readthedocs.io/en/latest/?badge=latest)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/isakruas/ecutils.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/isakruas/ripda/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/isakruas/ripda.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/isakruas/ripda/alerts/)
[![Latest Version](https://img.shields.io/pypi/v/ripda.svg?style=flat)](https://pypi.python.org/pypi/ripda/)

> *Ripda* é um mini *framework* que visa facilitar a implementação de qualquer sistema baseado em blockchain.

Introdução
==========

O quão fácil pode ser implementar um sistema baseado em blockchain?

Quando me propus a desenvolver este mini framework, estava buscando uma maneira simples e rápida de implementar uma solução baseada em blockchain, que fosse o mais personalizável possível, e que fosse em uma linguagem  de programação flexível.

A ideia inicial era criar a estrutura base de uma criptomoeda, inteiramente com Python, mas no decorrer da estruturação, percebi que poderia estender este projeto para qualquer sistema que necessite de salvar dados em uma estrutura de blockchain.

Você irá notar que parte da estrutura da Ripda segue o princípio de algumas criptomoedas, como a necessidade de mineração dos dados para salvá-los em uma cadeia de blocos, transações, etc. Uma das grandes diferenças é que aqui, você tem total controle sobre o quão difícil pode ser este processo de organização dos dados.

Por debaixo dos panos, Ripda utiliza o FastAPI para servir os dados de maneira mais performática possível, e fornece uma estrutura para que facilmente, você possa estender a estrutura do mini framework e adicionar mais funcionalidades.

Apesar de utilizar o FastAPI para servir os dados, você notará que grande parte da estruturação dos comandos, são inspirados no Django. Trabalhei com Djando por muitos anos, e gosto da maneira em que são utilizados os comandos no terminal, me inspirei grande parte na estrutura do Django para montar a forma como são organizados os comandos por aqui.

Respondendo a pergunta inicial: fácil, muito fácil utilizando Ripda.


Configurações
=============


Como configurar um aplicativo na utilizando a estrutura do Ripda?


O aplicativo Ripda modelo possui quatro arquivos, ``manage.py`` que é utilizado para execução dos comandos principais, ``models.py`` no qual você pode definir novos modelos a serem criados no banco de dados, para extender a aplicação, ``urls.py``, que você pode utilizar para criar novas rotas ou adicionar novos protocolos as rotas já existentes e ``settings.py`` que você definirar todas as configurações a serem usadas pela aplicação.

``models.py``

    from sqlmodel import Field, SQLModel

    """
    crie seus modelos aqui
    """

``urls.py``

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


``settings.py``

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


``manage.py``

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

Comandos
========

São no total quatro comandos principais para se iniciar a aplicação, o primeiro é o ``migrate``, este comando irá criar todas as tabelas necessárias para funcionamento da Ripda em seu banco de dados. Atenção, este comando irá apagar todas as tabelas e dados caso já existam no banco de dados.

    python manage.py runserver

O segundo comando é o ``populate``, este comando é utilizado quando se deseja popular o banco de dados com algumas transações faker para testar ou validar alguma nova funcionalidade. Serão criadas no total 1000 transações no banco, com dados quase aleatórios, para que você possa utilizar.

    python manage.py populate

O terceiro comando é o ``miner``, este comando, ao contrário dos anteriores, requer a passagem de um argumento adicional, o ``maker``. Como o nome sugere, este comando é o responsável pela mineração dos dados, ou seja, sua organização em uma estrutura de blockchain.

    python manage.py miner maker 1fd840bb7bad535ba1e8f587b41e5b27

O último comando é o ``runserver``, este comando é responsável por servir os endpoints publicamente. São criados dois depois, ``\blocks`` e ``\transactions`` , no qual ``transactions`` aceita os protocolos ``GET`` e ``POST`` e ``blocks`` somente ``GET``.

    python manage.py runserver
