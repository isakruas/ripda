from pingwallet import PINGWallet


if __name__ == '__main__':

    wallettransactionprepare = PINGWallet()
    print(wallettransactionprepare.ping(**{
        'kwds': {
            'def': 'wallet.transaction.prepare',
            'kwds': {
                'sender': '1Nq2RBRgs9QUvK6WDfqJpjpC6giVzJBpu9',
                'receiver': '6WDfqJpjpC6gi1Nq2RBRgs9QUvKVzJBpu9',
                'amount': 1,
                'private_key': '00e4946688e575e341331e1246ef63140aa8007b8f52c1c359caca6aa58b2c88c81708c679c04e19cb759f912b36873893c933bade87802ec29417c1766b57f4f57e'
            }
        }
    }))
