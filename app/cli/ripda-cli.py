import sys
import json
from __wallet__ import *
from __blockchain__ import *
from __miner__ import *
from __transaction__ import *

CLI_VERSION = '0.0.1.dev1'


# Módulos aceitos
modules = 'wallet', 'blockchain', 'miner', 'transaction'

# Métodos permitidos para cada módulo
methods = {
    'wallet': ('create',),
    'blockchain': tuple(),
    'miner': tuple(),
    'transaction': tuple()
}

if __name__ == '__main__':

    sys.argv.pop(0)

    module = str()

    method = str()

    args = list()

    kwds = dict()

    if len(sys.argv) >= 2:
        for k, v in enumerate(sys.argv):
            if k == 0:
                module = v
            elif k == 1:
                method = v
            else:
                if '=' in v:
                    i = v
                    i = i.split('=')
                    if len(i) == 2:
                        kwds[i[0]] = i[1]
                    else:
                        print(f'Parâmetros inválidos. {v} Não é reconhecido.')
                        sys.exit(0)
                else:
                    args.append(v)
    else:
        if sys.argv[0] == '--help':
            print(f"""
{'-' * 50}
{(lambda x: '-' * int((50-len(x))/2) + x + '-' * int((51-len(x))/2))(f'Ripda CLI v{CLI_VERSION}')}
{'-' * 50}
MÉTODOS PERMITIDOS:

{json.dumps(methods, indent=4)}

{'-' * 50}
ENTRADA:

ripda-cli module method arg1 arg2 arg3 ... key1=value1 key2=value2 key3=value3 ...
""""""
AVALIAÇÃO:
__module__(method, *(arg1, arg2, arg3, ...), **{'key1':'value1', 'key2':'value2', 'key3':'value3', ...})
"""f"""
{'-' * 50}
            """)
            sys.exit(1)
        else:
            print('Parâmetros insuficientes.')
            sys.exit(2)

    if not module in modules:
        print(f'O módulo {module} não é reconhecido.')
        sys.exit(3)

    if not method in methods[module]:
        print(f'O método {method} não é reconhecido.')
        sys.exit(4)

    print(eval(f'__{module}__(method, *args,**kwds)'))
