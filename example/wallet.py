"""
    Vamos supor que services.py esteja em execução ou que o nó esteja disponível.
    É possível construir vários outros exemplos de aplicativos que se comunicam com
    a API e realizam a solicitação de transação. Para realizar a assinatura,
    recomendamos que você envie a solicitação de protocolo a um Pool confiável.
"""
import json
from ripda.wallet.core import Wallet
import asyncio
import websockets
from ripda.settings import getc

"""
    Criando uma carteira sem entropia
"""
wallet_1 = Wallet().create_wallet()
print(wallet_1)

"""
    Criando uma carteira com entropia
    Carteiras criadas com entropia sempre retornam as mesmas chaves.
"""
wallet_2 = Wallet().create_wallet(email='email', password='password')
print(wallet_2)

"""

"""
frame = {
    'm': 'wallet',  # módulo de destino
    'f': 'create_transaction',  # função a ser executada
    'd': {
        'receiver': '18QT6s1zek1ZFaBMMENCfonwTkVfSxjuzZ',  # endereço da carteira do destinatário
        'amount': 10,  # quantidade de ripdas a serem enviadas
        'private_key': wallet_1['private_key'].hex(),  # chave privada do endereço da carteira; ele será usado para
        # assinar a transação.
    }
}


async def wallet():
    """
        Para que uma transação seja efetivada, é necessário que haja saldo na carteira.
    """
    global frame
    while True:
        uri = 'ws://' + str(getc('ripda_node', 'wallet_host')) + ':' + str(
            getc('ripda_node', 'wallet_port'))
        async with websockets.connect(uri) as node:
            await node.send(json.dumps(frame))
            """
                Tornou-se necessário aguardar 0,5s entre o envio da solicitação e a espera pela resposta.
            """
            await asyncio.sleep(0.5)
            async for message in node:
                receiver = json.loads(message)
                if 'm' and 'f' in receiver:
                    if receiver['m'] == 'wallet' and receiver['f'] == 'create_transaction':
                        if 'e' in receiver:
                            print(receiver['e'])
                            await node.close()
                        else:
                            if receiver['r'] == frame:
                                """
                                    O pedido de transação foi realizado com sucesso.
                                    É necessário aguardar a confirmação da rede.
                                """
                                print('O pedido de transação foi realizado com sucesso.\nÉ necessário aguardar a '
                                      'confirmação da rede.\n')
                                await node.close()
                            else:
                                """
                                    Uma transação foi criada, mas não por este algoritmo.
                                """
                                print('Uma transação foi criada, mas não por este algoritmo.')
                                await node.close()

        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    wallet()
))
loop.run_forever()
