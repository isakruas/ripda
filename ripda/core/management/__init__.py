import sys
from argparse import ArgumentParser
from ripda.core.management.commands import *


class Management:
    """
    API de comandos do módulo e/ou aplicativo.
    """

    def __init__(self, argv=None):
        """
        obtenha os argumentos do módulo ou do aplicativo.
        :param argv:
        """
        self.argv = argv or sys.argv[:]

    def execute(self):
        """
        execute os comandos usados pelo argumento
        :return:
        """
        try:
            parser = ArgumentParser()
            args = list()

            # o comando a ser executado está sempre na posição 1 de argv
            command = self.argv[1]

            """
            pegue todos os argumentos extras passados. deve ser usado como: chave valor
            """
            for i in [self.argv[2:][i:i + 2] for i in range(0, len(self.argv[2:]), 2)]:
                __i = '--' + i[0]
                args.append(__i)
                args.append(i[1])
                parser.add_argument(__i)

            kwargs = vars(parser.parse_args(args))

            # todas as funções que podem ser chamadas devem ser listadas aqui.
            FN_MAP = {
                'runserver': runserver.main,
                'migrate': migrate.main,
                'populate': populate.main,
                'miner': miner.main,
            }

            if command in FN_MAP:
                fn = FN_MAP[command]
                fn(**kwargs)

        except Exception as exc:
            raise Exception(
                "Couldn't execute Ripda"
            ) from exc


def execute_from_command_line(argv=None):
    utility = Management(argv)
    utility.execute()
