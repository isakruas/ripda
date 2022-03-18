import sys
from argparse import ArgumentParser
from ripda.core.management.commands import *


class Management:

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]

    def execute(self):
        try:
            parser = ArgumentParser()
            args = list()

            command = self.argv[1]

            for i in [self.argv[2:][i:i + 2] for i in range(0, len(self.argv[2:]), 2)]:
                __i = '--' + i[0]
                args.append(__i)
                args.append(i[1])
                parser.add_argument(__i)

            kwargs = vars(parser.parse_args(args))

            FN_MAP = {
                'runnode': runnode.main,
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

