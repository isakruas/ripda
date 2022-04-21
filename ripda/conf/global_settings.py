"""import pathlib"""
"""
todas as configurações aceitas
"""

HANDLER_MODULE: str = str()

MODELER_MODULE: str = str()

# Diretório raiz do projeto
"""BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()"""

# Nó em que a carteira será servida
NODE_HOST: str = 'localhost'
NODE_PORT: int = 1050

# Dificuldade em encontrar um hash; é medido pela quantidade de zeros no início do hash.
HASH_DIFFICULTY: int = 4

# Valor inicial padrão de nonce para testar
MINER_NONCE_START: float = 0.0

# Valor final padrão de nonce para testar
MINER_NONCE_STOP: float = 100.0

# Variação numérica entre nonces
MINER_NONCE_STEP: float = 0.001

ENGINE_HOST: str = str()
ENGINE_PORT: int = int()
ENGINE_USER: str = str()
ENGINE_PASSWORD: str = str()
ENGINE_DB: str = 'ripda'
