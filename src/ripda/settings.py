import pathlib

# Nó em que a carteira será servida
WALLET_HOST: str = 'localhost'
WALLET_PORT: int = 1050

# Nó no qual o blockchain será servido
BLOCKCHAIN_HOST: str = 'localhost'
BLOCKCHAIN_PORT: int = 8725

# Nós aos quais o host se conectará
BLOCKCHAIN_NODES: list = [('localhost', 8765), ('localhost', 8745)]

# Dificuldade em encontrar um hash; é medido pela quantidade de zeros no início do hash.
HASH_DIFFICULTY: int = 4

# Taxa cobrada, em percentual, por cada transação realizada na rede
FEE: float = 0.04

# Diretório raiz do projeto, será usado para criar pastas para organizar o cache.
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Crie os diretórios locais a serem usados pelo sistema
[x.mkdir(parents=True, exist_ok=True) for x in (BASE_DIR / 'storage/cache', BASE_DIR / 'storage/database/blocks', BASE_DIR / 'storage/database/wallets')]

# CACHE_DIR
CACHE_DIR = BASE_DIR / 'storage/cache'

# BLOCKS_DIR
BLOCKS_DIR = BASE_DIR / 'storage/database/blocks'

# WALLETS_DIR
WALLETS_DIR = BASE_DIR / 'storage/database/wallets'

"""
--------------------------------------------------
ÁRVORE DE DIRETÓRIOS CRIADOS:
BASE_DIR
|___/storage
|_______/cache
|_______/database
|___________/blocks
|___________/wallets
--------------------------------------------------
"""
# Valor inicial padrão de nonce para testar
MINER_NONCE_START: float = 0.0

# Valor final padrão de nonce para testar
MINER_NONCE_STOP: float = 100.0

# Variação numérica entre nonces
MINER_NONCE_STEP: float = 0.001
