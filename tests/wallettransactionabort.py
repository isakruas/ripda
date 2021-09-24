from pingwallet import PINGWallet


if __name__ == '__main__':

    wallettransactionabort = PINGWallet()
    print(wallettransactionabort.ping(**{
        'kwds': {
            'def': 'wallet.transaction.abort',
            'kwds': {
                # Precisa passar o identificador correto
                'uid': '90333fe50ca04061a928fd2a9b202c20'
            }
        }
    }))
