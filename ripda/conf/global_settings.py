HANDLER_MODULE = None

# Nó em que a carteira será servida
WALLET_HOST: str = 'localhost'
WALLET_PORT: int = 8725

# Nó no qual o blockchain será servido
BLOCKCHAIN_HOST: str = 'localhost'
BLOCKCHAIN_PORT: int = 8735

# Nós aos quais o host se conectará
BLOCKCHAIN_NODES: list = [
    ('localhost', 8765),
    ('localhost', 8755),
    ('localhost', 8745)
]

# Dificuldade em encontrar um hash; é medido pela quantidade de zeros no início do hash.
HASH_DIFFICULTY: int = 4

# Taxa cobrada, em percentual, por cada transação realizada na rede
FEE: float = 0.004

# Valor inicial padrão de nonce para testar
MINER_NONCE_START: float = 0.0

# Valor final padrão de nonce para testar
MINER_NONCE_STOP: float = 100.0

# Variação numérica entre nonces
MINER_NONCE_STEP: float = 0.001
