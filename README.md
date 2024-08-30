# PyIntelbras

**PyIntelbras** é um módulo Python para trabalhar com a [API Intelbras V3.35](https://botminio.apps.intelbras.com.br/sdk-api/HTTP%20API%20V3.35_Intelbras.pdf).

_Obs:_ Caso o link da documentação esteja _offline_, a mesma também está disponível no diretório [docs](docs) do repositório.

## Requisitos

- Testado com a API `V3.35` de um `iNVD 9116 PE FT`.

## Documentação

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
