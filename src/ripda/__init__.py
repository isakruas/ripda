import os
from pathlib import Path
from .settings import default
import logging

try:
    if os.path.isdir(str(Path.home()) + '/ripda/'):

        if not os.path.isdir(str(Path.home()) + '/ripda/blocks/'):
            os.mkdir(str(Path.home()) + '/ripda/blocks/')
            pass

        if not os.path.isfile(str(Path.home()) + '/ripda/config.ini'):
            default()
            pass
    else:
        os.mkdir(str(Path.home()) + '/ripda/')
        os.mkdir(str(Path.home()) + '/ripda/blocks/')
        default()
except Exception as e:
    logging.exception(e)

__all__ = [
    'block',
    'blockchain',
    'miner',
    'node',
    'transaction',
    'wallet'
]
