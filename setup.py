from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ripda',
    version='1.0.0.dev2',
    description='Integração do núcleo Ripda',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/isakruas/ripda',
    author='Isak Paulo de Andrade Ruas',
    license='MIT',
    author_email='isakruas@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ripda, ripda coin, coin module',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=['base58==2.1.0', 'ecdsa==0.17.0', 'websockets==9.1'],
    project_urls={
        'Bug Reports': 'https://github.com/isakruas/ripda/issues',
        'Source': 'https://github.com/isakruas/ripda/',
    },
)
