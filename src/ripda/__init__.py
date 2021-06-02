import os
from .config import default
from .config import getc

if not os.path.isfile('config.ini'):
    default()
    if not os.path.isdir(str(getc('ripda', 'path'))):
        os.mkdir(str(getc('ripda', 'path')))
        os.mkdir(str(getc('ripda', 'path_blocks')))
    pass

__all__ = [
    'block',
    'blockchain',
    'miner',
    'node',
    'transaction',
    'wallet'
]
