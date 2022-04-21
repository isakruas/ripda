import pathlib

HANDLER_MODULE: str = 'urls'

MODELER_MODULE: str = 'models'

# Diretório raiz do projeto
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

# Nó em que a carteira será servida
NODE_HOST: str = '127.0.0.1'
NODE_PORT: int = 1050

# Dificuldade em encontrar um hash; é medido pela quantidade de zeros no início do hash.
HASH_DIFFICULTY: int = 4

# Valor inicial padrão de nonce para testar
MINER_NONCE_START: float = 0.0

# Valor final padrão de nonce para testar
MINER_NONCE_STOP: float = 100.0

# Variação numérica entre nonces
MINER_NONCE_STEP: float = 0.001

ENGINE_HOST: str = 'localhost'
ENGINE_PORT: int = 5432
ENGINE_USER: str = 'user'
ENGINE_PASSWORD: str = 'password'
ENGINE_DB: str = 'ripda'
