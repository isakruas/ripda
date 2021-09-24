from pingwallet import PINGWallet

if __name__ == '__main__':

    walletcreate = PINGWallet()
    print(walletcreate.ping(**{
        'kwds': {
            'def': 'wallet.create',
            # Pode-se passar parâmetros de entropia
            'kwds': {}
        }
    }))
