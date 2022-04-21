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
