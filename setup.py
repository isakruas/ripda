from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

"""
    Considerações sobre controle de versão:
    
        As versões de lançamento definidas por P.M.N
        Versão P quando você faz alterações de API incompatíveis,
        Versão M quando você adiciona funcionalidade de maneira compatível com versões anteriores, e
        Versão N quando você faz correções de bug compatíveis com versões anteriores.
        Versões dev (denotadas com um sufixo '.devN')
        Versões alfa (denotados com um sufixo '.aN')
        Versões beta (denotado com um sufixo '.bN')
        Versões candidatas a lançamento (denotados com um sufixo '.rcN')
        Versões pós lançamento (denotados com um sufixo '.postN')
    
    Histórico de lançamento:
        1.0.0.dev1
        1.0.0.dev2
        
    Expectativa das próximas versões:
    
        1.0.0.a1
        1.0.0.a2
        1.0.0.b1
        1.0.0.b2
        1.0.0.rc1
        1.0.0.rc2
        1.0.0
        1.0.0.post1
        1.0.0.post2
        1.0.0.post2
        1.0.1.dev1
        1.0.1.dev2
        ...
    
"""
setup(

    name='ripda',
    version='0.0.1.dev1',
    description='Integração do núcleo Ripda',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/isakruas/ripda',
    author='Isak Paulo de Andrade Ruas',
    license='MIT',
    author_email='isakruas@gmail.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ripda, ripda coin, coin module',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=['base58==2.1.0', 'ecdsa==0.17.0', 'websockets==9.1', 'python-dateutil==2.8.1'],
    project_urls={
        'Bug Reports': 'https://github.com/isakruas/ripda/issues',
        'Source': 'https://github.com/isakruas/ripda/',
    },
)
