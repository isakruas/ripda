###  *Ripda* Transfer Protocol

#### HEADERS
> todas as solicitações devem conter um desses cabeçalhos
```
ORIGIN_HOST:ORIGIN_PORT|CURVE|X|Y|R|S|SHA256('ORIGIN_HOST:ORIGIN_PORT' + 'MESSAGE')
```
```
ORIGIN_HOST:ORIGIN_PORT|SHA256(REQUEST)|CURVE|X|Y|R|S|SHA256('ORIGIN_HOST:ORIGIN_PORT' + 'MESSAGE')
```

#### REQUEST
> formato de requisição a ser enviado a um nó
```
ORIGIN_HOST:ORIGIN_PORT|CURVE|X|Y|R|S|SHA256('ORIGIN_HOST:ORIGIN_PORT'+'COMMAND'+'TIMESTAMP')|COMMAND|TIMESTAMP|\r\n
```

#### RESPONSE
> resposta da requisição com as informações solicitadas
```
ORIGIN_HOST:ORIGIN_PORT|SHA256(REQUEST)|CURVE|X|Y|R|S|SHA256('ORIGIN_HOST:ORIGIN_PORT'+'SHA256(REQUEST)'+'DATA'+'TIMESTAMP')|DATA|TIMESTAMP|\r\n
```
#### CASE STUDY

Deixe **A**, **B**, **C**, **D**, nós de rede *Ripda*, de modo que (**A**, **B**), (**A**, **C**), (**C**, **D**), (**C**, **B**).

**A** prepara uma solicitação **U** e a envia para **B**, **B** recebe a solicitação **U** envia para **A** o aviso de recebimento e fecha a conexão.

**B** analisa a solicitação **U**, fazendo as seguintes perguntas, ignorando **U** se alguma delas for válida:

* **U** já foi analisado por este nó em menos de 60 segundos?
* **U** não tem um formato válido?
* O host de origem de **U** está na lista não confiável?
* A chave pública (**X**, **Y**) do usuário que assina a solicitação está na lista não confiável?
* Do timestamp da solicitação até o atual, passaram mais de 60 segundos?
* A assinatura digital de **U** não é válida?
* O comando de **U** não é válido?

Se **U** for válido, **B** analisará o comando de **U**, retornando a **A** a resposta da requisição com as informações solicitadas.

Vamos considerar o cenário em que **B** não possui as informações solicitadas em **U** e a requisição ainda é válida (não expirou).

Nesse caso, **B** envia a requisição de **A** para seus nós conhecidos, ou seja, apenas para **C**, porque **A** é o solicitante. **C** executa as mesmas validações realizadas por **B** na requisição **U**.

Vamos considerar o cenário em que **C** não possui as informações solicitadas em **U** e a requisição ainda é válida (não expirou).

Nesse caso, **C** envia a requisição de **A** para seus nós conhecidos, ou seja, apenas para **D** e **B**, porque **A** é o solicitante.

Observe que, embora **C** receba a requisição de **B**, durante a propagação, **C** enviará **U** de volta para **B**.
Observe também que, embora **B** receba a requisição **U** de **C**, nessa interação, **B** ignorará **U**.
Portanto, apenas **D** realmente receberá a requisição **U** feita por **A**.

**B** e **C** podem enviar um aviso a **A** para receber uma cópia da resposta de **U** assim que **A** a tiver.

Vamos considerar o cenário em que **D** possui as informações solicitadas em **U**, pelo nó **A** e a requisição ainda é válida (não expirou).

**D** executa as mesmas validações realizadas por **B** e **C** na requisição **U**.

**D** prepara a resposta da requisição, conecta-se a **A** e envia as informações solicitadas.

**A** recebe o conjunto de dados, envia uma cópia para **B** e **C**, e prossegue com o processamento que estava em andamento.

> Observe que, embora inicialmente **A** não tivesse uma conexão com **D**, foi possível que **D** se conectasse diretamente a **A**. Em uma requisição futura, além de **B** e **C**, **A** também poderá enviar uma requisição para **D**, pois agora ele sabe da existência do mesmo.

Observe que, se **A** envia **U** para **B** e **C**, o caminho mais próximo seria **A** -> **C** -> **D** --> **A**, e quando **C** recebesse uma cópia de **U** através de **B**, **C** ignoraria **U** porque o mesmo já havia o recebido através **A**.
