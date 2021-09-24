from pingwallet import PINGWallet


if __name__ == '__main__':

    wallettransactionrepr = PINGWallet()
    print(wallettransactionrepr.ping(**{
        'kwds': {
            'def': 'wallet.transaction.repr',
            'kwds': {}
        }
    }))
