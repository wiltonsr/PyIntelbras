# PyIntelbras

**PyIntelbras** é um módulo Python para trabalhar com a [API Intelbras V3.35](https://botminio.apps.intelbras.com.br/sdk-api/HTTP%20API%20V3.35_Intelbras.pdf).

*Obs:* Caso o link da documentação esteja *offline*, a mesma também está disponível no diretório [docs](docs) do repositório.

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

ibapi = IntelbrasAPI("http://device-server.example.com")
ibapi.login("api-user", "api-pass")
```
