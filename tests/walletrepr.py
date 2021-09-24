from pingwallet import PINGWallet

if __name__ == '__main__':

    walletrepr = PINGWallet()
    print(walletrepr.ping(**{
        'kwds': {
            'def': 'wallet.repr',
            'kwds': {}
        }
    }))
