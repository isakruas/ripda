Introdução
==========

O quão fácil pode ser implementar um sistema baseado em blockchain?

Quando me propus a desenvolver este mini framework, estava buscando uma maneira simples e rápida de implementar uma solução baseada em blockchain, que fosse o mais personalizável possível, e que fosse em uma linguagem  de programação flexível.

A ideia inicial era criar a estrutura base de uma criptomoeda, inteiramente com Python, mas no decorrer da estruturação, percebi que poderia estender este projeto para qualquer sistema que necessite de salvar dados em uma estrutura de blockchain.

Você irá notar que parte da estrutura da Ripda segue o princípio de algumas criptomoedas, como a necessidade de mineração dos dados para salvá-los em uma cadeia de blocos, transações, etc. Uma das grandes diferenças é que aqui, você tem total controle sobre o quão difícil pode ser este processo de organização dos dados.

Por debaixo dos panos, Ripda utiliza o FastAPI para servir os dados de maneira mais performática possível, e fornece uma estrutura para que facilmente, você possa estender a estrutura do mini framework e adicionar mais funcionalidades.

Apesar de utilizar o FastAPI para servir os dados, você notará que grande parte da estruturação dos comandos, são inspirados no Django. Trabalhei com Djando por muitos anos, e gosto da maneira em que são utilizados os comandos no terminal, me inspirei grande parte na estrutura do Django para montar a forma como são organizados os comandos por aqui.

Respondendo a pergunta inicial: fácil, muito fácil utilizando Ripda.
