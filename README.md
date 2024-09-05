# PyIntelbras

[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/pyintelbras.svg)](https://pypi.org/project/pyintelbras/)
[![PyPI Package Version](https://img.shields.io/pypi/v/pyintelbras.svg)](https://pypi.org/project/pyintelbras/)
![GitHub Issues](https://img.shields.io/github/issues/wiltonsr/pyintelbras)
![GitHub commit activity (branch)](https://img.shields.io/github/last-commit/wiltonsr/pyintelbras/main)
![GitHub License](https://img.shields.io/github/license/wiltonsr/pyintelbras?link=https%3A%2F%2Fgithub.com%2Fwiltonsr%2FPyIntelbras%2Fblob%2Fmain%2FLICENSE)

**PyIntelbras** é um módulo Python para trabalhar com a [API Intelbras V3.35](https://botminio.apps.intelbras.com.br/sdk-api/HTTP%20API%20V3.35_Intelbras.pdf).

_Obs:_ Caso o link da documentação esteja _offline_, a mesma também está disponível no diretório [docs](docs) do repositório.

## Requisitos

- Testado com a API `V3.35` de um `iNVD 9116 PE FT`.

### Iniciando

Instale PyIntelbras usando pip:

```bash
$ pip install pyintelbras
```

Agora é possível importar e usar o PyIntelbras da seguinte forma:

```python
from pyintelbras import IntelbrasAPI

api = IntelbrasAPI("http://device-server.example.com")
api.login("api-user", "api-pass")

response = api.configManager(action='getConfig', name='ChannelTitle')
```

## Documentação

O **PyIntelbras** utiliza a biblioteca [_requests_](https://requests.readthedocs.io/en/master/) para HTTP. Todos os _paths_ existentes na API da Intelbras podem ser utilizados como métodos e seus respectivos parâmetros também podem ser passados como parâmetros das funções.

```python
from pyintelbras import IntelbrasAPI

api = IntelbrasAPI("http://device-server.example.com")
api.login("api-user", "api-pass")

response = api.configManager(action='getConfig', name='ChannelTitle')
```

O exemplo acima irá realizar uma requisição `GET` para o endereço:

`http://device-server.example.com/cgi-bin/configManager.cgi?action=getConfig&name=ChannelTitle`.

Note que tanto o prefixo `cgi-bin` quanto o sufixo `.cgi`, exigidos pela API, são automaticamente adicionados.

### Tipo de Requisição

É possível definir o tipo de requisição, sendo permitidos apenas 2 verbos HTTP.

Por padrão e caso seja omitido, a requisição será do tipo `GET`.

#### GET

```python
from pyintelbras import IntelbrasAPI

api = IntelbrasAPI("http://device-server.example.com")
api.login("api-user", "api-pass")

# Mesmo efeito para ambas as requisições
response = api.configManager(action='getConfig', name='ChannelTitle')
response = api.configManager.get(action='getConfig', name='ChannelTitle')
```

#### POST

```python
from pyintelbras import IntelbrasAPI

api = IntelbrasAPI("http://device-server.example.com")
api.login("api-user", "api-pass")

response = api.api.LogicDeviceManager.getCameraState.post(body={ 'uniqueChannels': [-1] })
```

O exemplo acima irá realizar uma requisição `POST` para o endereço:

`http://device-server.example.com/cgi-bin/api/LogicDeviceManager/getCameraState.cgi`.

E enviar o conteúdo da variável `body` como corpo da requisição.

### Diferenciação entre Maiúsculas e Minúsculas

A API da Intelbrás é _case sensitive_, ou seja, faz diferenciação entre maiúsculas e minúsculas. Por conta disto, a URL de requisição é montada exatamente conforme os métodos e parâmetros são passados.

Sendo assim, a requisição abaixo deverá retornar o código de status HTTP `200`:

<pre>
api.config<b>M</b>anager(action='getConfig', name='ChannelTitle')
</pre>

Enquanto isso, a requisição abaixo retornará o código de status HTTP `400`:

<pre>
api.config<b>m</b>anager(action='getConfig', name='ChannelTitle')
</pre>

Note a diferença da grafia da letra _M_. Isso irá ocorrer pelo fato de não existir a rota:

`.../cgi-bin/configmanager.cgi/...`

e sim:

`.../cgi-bin/configManager.cgi/...`.

### Uso de Parâmetros

Os componente de consulta (_query parameters_), utilizados como parâmetros das funções, devem ser tratados adequadamente quando possuírem sintaxe inválida no python. Basicamente isso será necessário quando houver
`.` ou `[]` nos parâmetros. O seguinte exemplo:

```python
...
response = api.mediaFileFind(action='findFile', condition.Channel=1)
```

Retornará o erro:

```python
  Cell In[1], line 1
    response = api.mediaFileFind(action='findFile', condition.Channel=1)
                                                    ^
SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
```

A forma correta de lidar neste caso é utilizando a [descompactação de listas de argumentos](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists).

```python
...
params = {
    'action': 'findFile',
    'condition.Channel': 1
}

response = api.mediaFileFind(**params)
```

### Habilitando Logs

Se for necessário debugar algum problema com as requisições para a API da Intelbras, é possível habilitar a saída de logs. O `pyintelbras` utiliza o sistema de _logging_ do Python, mas por padrão, ele registra para _Null_. É possível alterar esse comportamento. Segue um exemplo:

```python
import sys
import logging
from pyintelbras import IntelbrasAPI

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyintelbras')
log.addHandler(stream)
log.setLevel(logging.DEBUG)

api = IntelbrasAPI("http://device-server.example.com")
api.login("api-user", "api-pass")

response = api.configManager(action='getConfig', name='ChannelTitle')
```

### Exemplos

Outros exemplos de uso da API estão disponíveis no diretório [examples](examples) do repositório.
