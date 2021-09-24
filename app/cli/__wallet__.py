from ripda.core.wallet import Wallet

__all__ = ['__wallet__']


def __wallet__(method, *args, **kwds):
    """
    Wallet CLI
    """

    if method == 'create':
        return Wallet().create(**kwds)
    else:
        pass
