### *Integração do núcleo Ripda*
> *Ripda* é uma criptomoeda experimental construída com a linguagem de programação python, fácil de instalar e configurar, que permite a qualquer usuário construir seus próprios aplicativos através do núcleo do Ripda.

##### Integração
> O Ripda é construído de forma modular, de forma que o usuário, em suas aplicações, possa escolher qual dos módulos deseja importar para realizar a integração, os principais módulos são node, wallet e miner

###### Módulo block
> O módulo block é responsável por gerar o bloco de origem, bem como retornar o próximo bloco a ser validado na rede e verificar se um hash gerado é válido.

```python
>>> from ripda.block.core import Block 
>>> block_view = Block().view()
>>> print(block_view)
{'count': 28, 'transactions': [], 'last_hash': '000097a1a8f553e494a9c6f0c9edabd0d756c73e9e4819bbb439ecba011184e2', 'timestamp': 1622580679.988441, 'forger': False}
```
> block_view nos informa o número do próximo bloco na rede, as transações pendentes para validação, o hash do último bloco validado e se esse bloco precisa ou não ser validado pelos mineiros.

```python
>>> from ripda.block.core import Block 
>>> is_hash_valid = Block().is_hash_valid(_hash='000097a1a8f553e494a9c6f0c9edabd0d756c73e9e4819bbb439ecba011184e2')
>>> print(is_hash_valid)
True
``` 
> Para um hash ser válido, ele deve começar com 0000

###### Módulo blockchain

> O módulo blockchain é responsável por verificar se um bloco extraído é válido e adicionar este bloco extraído à cadeia de blocos. Este módulo também retorna todos os blocos já validados e incluídos na rede.

```python
>>> from ripda.blockchain.core import Blockchain 
>>> blockchain_view = Blockchain().view()
>>> print(blockchain_view)
``` 

###### Módulo miner
> O módulo miner fornece um conjunto de ferramentas que tornam possível minerar um bloco para posterior adição ao blockchain

```python
>>> from ripda.miner.core import Miner
>>> forging = Miner(block=None, wallet=None).ripda()
>>> print(forging)
``` 
> Você deve definir os parâmetros de block e wallet para o Miner; block é o bloco a ser minerado e wallet é o endereço da carteira do mineiro. A rede pagará a recompensa para o primeiro a minerar o bloco. Para cada bloco minerado, são gerados 0,04 ripdas, que são creditados na carteira do mineiro.

###### Módulo transaction
> O módulo transaction tem duas classes principais, Pool e Transaction. A primeira gerencia as transações da rede e a segunda é responsável por preparar adequadamente uma transação para ser adicionada à rede.

```python
>>> from ripda.transaction.core import Transaction
>>> transaction_create = Transaction(sender='18yvjn9rEBG4npnG8sZTVhUJRpkDzcws7h', receiver='14bCyrPDTbY2T5YF1mSH729PhKqzdtbg9Z', amount=0.04, sender_private_key='', sender_public_key='').create()
>>> print(transaction_create)
>>> transaction_view =Transaction(sender='18yvjn9rEBG4npnG8sZTVhUJRpkDzcws7h', receiver='14bCyrPDTbY2T5YF1mSH729PhKqzdtbg9Z', amount=0.04, sender_private_key='', sender_public_key='').create()
>>> print(transaction_view)
``` 
> Embora seja possível criar transações diretamente, é recomendado usar o módulo wallet para isso.

```python
>>> from ripda.transaction.pool import Pool
``` 
###### Módulo wallet
> O módulo wallet contém um conjunto de funções que facilitam a criação de uma carteira, verificação de assinaturas e criação de transações na rede.

```python
>>> from ripda.wallet.core import Wallet
>>> create_wallet = Wallet().create_wallet()
>>> print(create_wallet)
{'private_key': b'\x00*\xdb\x93\xfb\x9d\x93h\x87\x07\x8fv\xd8\xb58\x9fH\xeet{S;\xd2L\xaf\xfc:Pj\\\xe0m\x93}\xd9\xfb\x10\xd3\x87\xdf3\xf4#I\xba\x9a\xb3\x89EFm\xebmC\xb7\xcaAoxD\x1b\xcb>\xf9\xef\xfc', 'public_key': '030177a3142376b228ea32787ddecaf49d12d6eb1e13598e0f61cd94a1bcdae8268cb98ddda14c1179bb806a67ee3cb1afbc04b56d45ac0d5366331ecf3a2d1e9bed35', 'wallet': '123ARRoZwKbWBuXdFePkGxee1S8JDJ1v1b'}
``` 
> Uma carteira possui uma chave pública, uma chave privada e um endereço. A chave privada é usada para assinar uma transação e a chave pública é usada pelos mineiros para validar se a transação na rede é de fato verdadeira. Você pode criar uma carteira como no exemplo acima, ou pode cirar com alguns parâmetros de entropia, para isso, faça.

```python
>>> create_wallet = Wallet().create_wallet(email='', password='')
``` 
> Se ja possui uma carteira criada, para abri-la, faça:

```python
>>> wallet = Wallet(private_key='')
``` 
> Com a carteira aberta, para criar uma transação, faça:

```python
>>> wallet = Wallet(private_key='')
>>> wallet.create_transaction(receiver='', amount='')
``` 
###### Módulo node
> Este módulo possui uma série de funcionalidades que facilitam a integração das aplicações ao núcleo da Ripda. São APIs que permitem a criação de uma rede P2P através de websockets, bem como o envio de ordens através de qualquer dispositivo compatível com websockets para a rede.

##### Exemplos
> O primeiro exemplo você pode ver como usar Ripda para criar uma rede. Por padrão, as redes funcionam localmente.

###### services.py
```python
import asyncio
from ripda import services

"""
    Crie websockets para que seja possível se conectar à rede.
"""
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    # Node é o serviço principal, trata das transações e blocos da rede que se encontram em processo
    # de validação, bem como os validados. Este endpoint pode ser público.
    services.node(),
    # Wallet é um conjunto de ferramentas que permite a criação de transações, criação de carteiras,
    # validação de assinaturas,entre outras possibilidades. Não recomendamos tornar este endpoin público.
    services.wallet(),
    # Miner contém um conjunto de recursos para mineiros. Não recomendamos tornar este endpoin público.
    services.miner()
))
loop.run_forever()
``` 

> O segundo exemplo é como se conectar a uma rede para extrair os blocos que estão sendo gerados, e tentar forjar esses blocos com a possibilidade de ganhar alguma recompensa em ripdas pelo trabalho realizado.

###### miner.py
```python
"""
    Vamos supor que services.py esteja em execução ou que o nó esteja disponível.
"""
import json
import websockets
from ripda.miner.core import Miner
import asyncio
from ripda.settings import getc


async def get_last_block():
    """
        Solicitando ao Pool o bloco na fila para validação.
    """
    print('Solicitando ao Pool o bloco na fila para validação.')
    uri = 'ws://' + str(getc('ripda_node', 'core_host')) + ':' + str(
        getc('ripda_node', 'core_port'))
    async with websockets.connect(uri) as node:
        await node.send(json.dumps({
            'm': 'block',
            'f': 'view',
            'd': {
            }
        }))
        """
            Tornou-se necessário aguardar 0,5s entre o envio da solicitação e a espera pela resposta.
        """
        await asyncio.sleep(0.5)
        async for message in node:
            receiver = json.loads(message)
            if 'm' and 'f' and 'r' in receiver:
                if receiver['m'] == 'block' and receiver['f'] == 'view':
                    """
                        Após obter a resposta, encerre a conexão com o Pool e retorne os dados.
                    """
                    await node.close()
                    return receiver['r']


async def add_block_on_blockchain(forger):
    """
        Tenta adicionar o bloco forjado ao Pool
    """
    print('Tenta adicionar o bloco forjado ao Pool.')
    uri = 'ws://' + str(getc('ripda_node', 'core_host')) + ':' + str(
        getc('ripda_node', 'core_port'))
    async with websockets.connect(uri) as node:
        await node.send(json.dumps({
            'm': 'blockchain',
            'f': 'add_block',
            'd': forger
        }))
        """
            Tornou-se necessário aguardar 0,5s entre o envio da solicitação e a espera pela resposta.
        """
        await asyncio.sleep(0.5)
        async for message in node:
            receiver = json.loads(message)
            if 'm' and 'f' and 'd' in receiver:
                if receiver['m'] == 'blockchain' and receiver['f'] == 'add_block':
                    """
                        Após obter a resposta, encerre a conexão com o Pool e retorne os dados.
                    """
                    if receiver['d'] == forger:
                        await node.close()
                        return receiver
                    else:
                        return False


async def miner():
    """
        Verifica periodicamente o Pool em busca de blocos para validar,
        se encontrar, tenta validar o bloco e adicioná-lo à cadeia de blocos.
    """
    while True:
        block = await get_last_block()
        if block['forger']:
            """
                O bloco recebido já pode ser forjado; tentando forjar o bloco.
            """
            print('O bloco recebido já pode ser forjado; tentando forjar o bloco.')
            """
                É necessário inserir o endereço de sua carteira corretamente, para que o prêmio seja pago.
            """
            forger = Miner(
                block=block,
                wallet='1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU'
            ).ripda()
            receiver = await add_block_on_blockchain(forger)
            if 'd' in receiver:
                """
                    O bloco que você minerou foi adicionado ao Pool com sucesso.
                """
                print('O bloco que você minerou foi adicionado ao Pool com sucesso.')
            elif receiver is False:
                """
                    Um novo bloco foi adicionado, mas não aquele que você minerou.
                """
                print('Um novo bloco foi adicionado, mas não aquele que você minerou.')
        await asyncio.sleep(0.5)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    miner()
))
loop.run_forever()

``` 
###### wallet.py
> O terceiro exemplo é como conectar a API Wallet da Ripda para gerar e criar uma transação. Também mostra como criar uma carteira com ou sem entropia.

```python
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

``` 

###### settings.py

>  O quarto exemplo é como as configurações padrão do Ripada são alteradas para personalizar algumas de suas funcionalidades.

```python
from ripda.settings import getc, setc
"""
    getc() busca o valor de uma variável de um arquivo de configuração
    setc() modifica o valor de uma variável de um arquivo de configuração

    Variáveis de configuração padrão
    
    config['ripda'] = {
        'path': str(Path.home()) + '/ripda/',
        'path_blocks': str(Path.home()) + '/ripda/blocks/',
    }

    config['ripda_node'] = {
        'core_host': 'localhost',
        'core_port': '1140',
        'wallet_host': 'localhost',
        'wallet_port': '1050',
        'miner_host': 'localhost',
        'miner_port': '1120'
    }

    config['ripda_transaction'] = {
        'pool_block_limit': '25',
    }

    config['ripda_block'] = {
        'core_difficulty': '4',
    }
"""


core_difficulty_before = getc('ripda_block', 'core_difficulty')

print(core_difficulty_before)

setc('ripda_block', 'core_difficulty', '6')

core_difficulty_after = getc('ripda_block', 'core_difficulty')

print(core_difficulty_after)

``` 

##### Notas
> Se o Ripda não criar diretórios de forma altamântica, você precisará criá-los manualmente. Os diretórios são usados para fazer backup de dados. 

