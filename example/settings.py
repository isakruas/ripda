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
