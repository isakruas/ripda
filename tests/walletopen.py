from pingwallet import PINGWallet

if __name__ == '__main__':

    walletopen = PINGWallet()
    print(walletopen.ping(**{
        'kwds': {
            'def': 'wallet.open',
            'kwds': {
                'pem': '-----BEGIN EC PRIVATE KEY-----\nMIHcAgEBBEIA5JRmiOV140EzHhJG72MUCqgAe49SwcNZyspqpYssiMgXCMZ5wE4Z\ny3WfkSs2hziTyTO63oeALsKUF8F2a1f09X6gBwYFK4EEACOhgYkDgYYABAEPgVH9\nLrqnyEMEZ0D+AsoOa9oic81UA4x9wFEtvDJYpp4yktQtjTNpPEQgkW662ApYmlVm\nnx5KKdWxwzqjHDAB3ABR9gdVuqg6GYnH/HihLGm0klXqdb+e+kymC2x3wpZOmg8P\nPG6AUMFZdKalEFiDbm+qLEsN7MAigu/4HE6fFQlv0Q==\n-----END EC PRIVATE KEY-----\n'
            }
        }
    }))
