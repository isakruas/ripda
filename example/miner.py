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
