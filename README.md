# PyIntelbras

[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/pyintelbras.svg)](https://pypi.org/project/pyintelbras/)
[![PyPI Package Version](https://img.shields.io/pypi/v/pyintelbras.svg)](https://pypi.org/project/pyintelbras/)
![GitHub Issues](https://img.shields.io/github/issues/wiltonsr/pyintelbras)
![GitHub commit activity (branch)](https://img.shields.io/github/last-commit/wiltonsr/pyintelbras/main)
![GitHub License](https://img.shields.io/github/license/wiltonsr/pyintelbras?link=https%3A%2F%2Fgithub.com%2Fwiltonsr%2FPyIntelbras%2Fblob%2Fmain%2FLICENSE)

**PyIntelbras** é um módulo Python para trabalhar com a [API Intelbras V3.59](https://botminio.apps.intelbras.com.br/dvr/HTTP_API_V3_59_Intelbras.pdf).

_Obs:_ Caso o link da documentação esteja _offline_, a mesma também está disponível no diretório [docs](docs) do repositório.

## Requisitos

- Testado com a API `2.84` de um `iNVD 9116 PE FT`.

### Iniciando

Instale PyIntelbras usando pip:

```bash
pip install pyintelbras
```

Agora é possível importar e usar o PyIntelbras da seguinte forma:

```python
from pyintelbras import IntelbrasAPI

intelbras = IntelbrasAPI("http://device-server.example.com")
intelbras.login("api-user", "api-pass")

response = intelbras.configManager(action='getConfig', name='ChannelTitle')
```

## Documentação

O **PyIntelbras** utiliza a biblioteca [_requests_](https://requests.readthedocs.io/en/master/) para HTTP. Todos os _paths_ existentes na API da Intelbras podem ser utilizados como métodos e seus respectivos parâmetros também podem ser passados como parâmetros das funções.

```python
from pyintelbras import IntelbrasAPI

intelbras = IntelbrasAPI("http://device-server.example.com")
intelbras.login("api-user", "api-pass")

response = intelbras.configManager(action='getConfig', name='ChannelTitle')
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

intelbras = IntelbrasAPI("http://device-server.example.com")
intelbras.login("api-user", "api-pass")

# Mesmo efeito para ambas as requisições
response = intelbras.configManager(action='getConfig', name='ChannelTitle')
response = intelbras.configManager.get(action='getConfig', name='ChannelTitle')
```

#### POST

```python
from pyintelbras import IntelbrasAPI

intelbras = IntelbrasAPI("http://device-server.example.com")
intelbras.login("api-user", "api-pass")

response = intelbras.api.LogicDeviceManager.getCameraState.post(body={ 'uniqueChannels': [-1] })
```

O exemplo acima irá realizar uma requisição `POST` para o endereço:

`http://device-server.example.com/cgi-bin/api/LogicDeviceManager/getCameraState.cgi`.

E enviar o conteúdo da variável `body` como corpo da requisição.

### Diferenciação entre Maiúsculas e Minúsculas

A API da Intelbrás é _case sensitive_, ou seja, faz diferenciação entre maiúsculas e minúsculas. Por conta disto, a URL de requisição é montada exatamente conforme os métodos e parâmetros são passados.

Sendo assim, a requisição abaixo deverá retornar o código de status HTTP `200`:

<pre>
intelbras.config<b>M</b>anager(action='getConfig', name='ChannelTitle')
</pre>

Enquanto isso, a requisição abaixo retornará o código de status HTTP `400`:

<pre>
intelbras.config<b>m</b>anager(action='getConfig', name='ChannelTitle')
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
response = intelbras.mediaFileFind(action='findFile', condition.Channel=1)
```

Retornará o erro:

```python
  Cell In[1], line 1
    response = intelbras.mediaFileFind(action='findFile', condition.Channel=1)
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

response = intelbras.mediaFileFind(**params)
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

intelbras = IntelbrasAPI("http://device-server.example.com")
intelbras.login("api-user", "api-pass")

response = intelbras.configManager(action='getConfig', name='ChannelTitle')
```

### Métodos Helpers

Existem alguns métodos para facilitar determinadas comunicações com a `API`.

- Verificar versão da API

```python
...
intelbras.api_version
# {'version': 2.84}
```

- Listar canais

```python
...
intelbras.channels
# [{'Name': 'Lab01'},
# {'Name': 'Lab02'},
# {'Name': 'Lab03'},
# {'Name': 'Lab04'},
# {'Name': 'Lab05'},
# {'Name': 'Lab06'},
# {'Name': 'Canal7'},
# {'Name': 'Canal8'},
# {'Name': 'Canal9'},
# {'Name': 'Canal10'},
# {'Name': 'Canal11'},
# {'Name': 'Canal12'},
# {'Name': 'Canal13'},
# {'Name': 'Canal14'},
# {'Name': 'Canal15'},
# {'Name': 'Canal16'}]
```

- Encontrar mídias

Buscar por mídias na `API` envolve `5` ações:

1. factory.create
1. findFile
1. findNextFile
1. close
1. destroy

O método `find_media_files` facilita esse procedimento, internalizando toda essa complexidade, sendo necessário informar apenas os parâmetros da busca.

```python
...
params = {
  'condition.Channel': 1,
  'condition.StartTime': '2024-8-27 12:00:00',
  'condition.EndTime': '2024-8-29 12:00:00'
}

intelbras.find_media_files(params)
# {'found': 1,
# 'items': [{'VideoStream': 'Main',
#   'Channel': 0,
#   'Type': 'dav',
#   'StartTime': datetime.datetime(2024, 8, 28, 2, 40, 49),
#   'EndTime': datetime.datetime(2024, 8, 28, 2, 41),
#   'Disk': 2,
#   'Partition': 2,
#   'Cluster': 371211,
#   'FilePath': '/mnt/dvr/2024-08-28/0/dav/02/0/2/371211/02.40.49-02.41.00[R][0@0][0].dav',
#   'Length': 3276800,
#   'Flags': ['Event'],
#   'Events': ['FaceRecognition'],
#   'CutLength': 3276800}]}
```

- Processar respostas

Algumas repostas da `API` são enviadas no formato `chave=valor` no corpo da resposta.

Nestes casos, é possível utilizar a função `parse_response` para converter a resposta em um [dicionário](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) python para facilitar a manipulação dos dados.

```python
...
from pyintelbras.helpers import parse_response
...
response = intelbras.recordManager(action='getCaps')
print(response.text)
# caps.MaxPreRecordTime=30
# caps.PacketLengthRange[0]=1
# caps.PacketLengthRange[1]=60
# caps.PacketSizeRange[0]=131072
# caps.PacketSizeRange[1]=2097152
# caps.SupportExtraRecordMode=true
# caps.SupportHoliday=true
# caps.SupportPacketType[0]=Time
# caps.SupportPacketType[1]=Size
# caps.SupportResumeTransmit=false

d = parse_response(response.text)
print(d)
# {'caps': {'MaxPreRecordTime': 30,
#   'PacketLengthRange': [1, 60],
#   'PacketSizeRange': [131072, 2097152],
#   'SupportExtraRecordMode': True,
#   'SupportHoliday': True,
#   'SupportPacketType': ['Time', 'Size'],
#   'SupportResumeTransmit': False}}

print(d.get('caps').get('PacketLengthRange')[1])
# 60
```

### Exemplos

Outros exemplos de uso da API estão disponíveis no diretório [examples](examples) do repositório.
