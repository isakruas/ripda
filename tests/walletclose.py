from pingwallet import PINGWallet

if __name__ == '__main__':

    walletclose = PINGWallet()
    print(walletclose.ping(**{
        'kwds': {
            'def': 'wallet.close',
            'kwds': {}
        }
    }))
