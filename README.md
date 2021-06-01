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
> Este módulo possui uma série de funcionalidades que facilitam a integração das aplicações ao núcleo da Ripda. São APIs que permitem a criação de uma rede P2P através de websockets, bem como o envio de ordens através de qualquer dispositivo compatível com websockets para a rede. Você pode usar os recursos das APIs, usando websockets, como no exemplo abaixo. As portas definidas neste exemplo são portas padrão na rede Ripda.

```python
import asyncio
import websockets
from ripda.node.core import Node
from ripda.node.wallet import NodeWallet
from ripda.node.miner import NodeMiner


async def node():
    server = Node()
    await websockets.serve(server.ws_handler, 'localhost', 1140)

async def node_wallet():
    server = NodeWallet()
    await websockets.serve(server.ws_handler, 'localhost', 1050)

async def node_miner():
    server = NodeMiner()
    await websockets.serve(server.ws_handler, 'localhost', 1120)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    node(),
    node_wallet(),
    node_miner()
))
loop.run_forever()
``` 


