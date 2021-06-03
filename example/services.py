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
