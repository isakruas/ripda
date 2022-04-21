Comandos
========

São no total quatro comandos principais para se iniciar a aplicação, o primeiro é o ``migrate``, este comando irá criar todas as tabelas necessárias para funcionamento da Ripda em seu banco de dados. Atenção, este comando irá apagar todas as tabelas e dados caso já existam no banco de dados.

    python manage.py runserver

O segundo comando é o ``populate``, este comando é utilizado quando se deseja popular o banco de dados com algumas transações faker para testar ou validar alguma nova funcionalidade. Serão criadas no total 1000 transações no banco, com dados quase aleatórios, para que você possa utilizar.::

    python manage.py populate

O terceiro comando é o ``miner``, este comando, ao contrário dos anteriores, requer a passagem de um argumento adicional, o ``maker``. Como o nome sugere, este comando é o responsável pela mineração dos dados, ou seja, sua organização em uma estrutura de blockchain.::

        python manage.py miner maker 1fd840bb7bad535ba1e8f587b41e5b27

O último comando é o ``runserver``, este comando é responsável por servir os endpoints publicamente. São criados dois depois, ``\blocks`` e ``\transactions`` , no qual ``transactions`` aceita os protocolos ``GET`` e ``POST`` e ``blocks`` somente ``GET``.::

    python manage.py runserver