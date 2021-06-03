import configparser
import logging
from pathlib import Path
import sys


def getc(module=None, key=None):
    config = configparser.ConfigParser()
    config.read(str(Path.home()) + '/ripda/config.ini')
    return config[module][key]


def setc(module=None, key=None, value=None):
    config = configparser.ConfigParser()
    config.read(str(Path.home()) + '/ripda/config.ini')
    config[module][key] = value
    with open(str(Path.home()) + '/ripda/config.ini', 'w') as configfile:
        config.write(configfile)
    return True


def default():
    config = configparser.ConfigParser()

    config['ripda'] = {
        'path': str(Path.home()) + '/ripda/',
        'path_blocks': str(Path.home()) + '/ripda/blocks/',
    }

    config['ripda_node'] = {
        'core_host': 'localhost',
        'core_port': '1140',
        'wallet_host': 'localhost',
        'wallet_port': '1050',
        'miner_host': 'localhost',
        'miner_port': '1120'
    }

    config['ripda_transaction'] = {
        'pool_block_limit': '25',
    }

    config['ripda_block'] = {
        'core_difficulty': '4',
    }

    with open(str(Path.home()) + '/ripda/config.ini', 'w') as configfile:
        config.write(configfile)

    # print('Arquivo de configuração padrão criado\n')

    return True


def custom():
    print('Arquivo de configuração personalizado\n')
    exit()


if __name__ == '__main__':

    parameters = sys.argv[1:]

    if '--default' in parameters:
        default()

    dash = '-' * 70
    print(dash)
    print(20 * ' ' + 'Arquivo de configuração Ripda')
    print(dash)
    option = None
    while True:
        try:
            option = int(input(
                '[0] - Usar configuração padrão\n[1] - Personalizar arquivo de configuração\n[2] - Cancelar '
                'configuração\n'))
        except Exception as e:
            logging.exception(e)
        if option is not None:
            if option == 0:
                default()
                break
            elif option == 1:
                custom()
                break
            elif option == 2:
                exit()
                break
            else:
                pass
        pass
