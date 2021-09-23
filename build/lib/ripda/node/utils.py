import json


class Utils:
    """
        Conjunto de funções úteis que são usadas nos arquivos core.py, miner.py e wallet.py
    """

    @staticmethod
    async def sender(m, f, r=None, e=None, d=None):
        """
            Prepare a mensagem de retorno no formato adequado
        """
        """
        sender = {
            'm': 'module: str',
            'f': 'function: str',
            'r': 'return: object',
            'e': 'error: str'
            'd': 'return: object',
        }
        """
        if e is None:
            if r is None:
                sender = {
                    'm': m,
                    'f': f,
                    'd': d,
                }
            else:
                sender = {
                    'm': m,
                    'f': f,
                    'r': r,
                }
        else:
            sender = {
                'm': m,
                'f': f,
                'e': e,
            }
        return json.dumps(sender)
