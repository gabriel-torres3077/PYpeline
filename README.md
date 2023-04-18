# PYpiline
## Requisitos

- [Python 3.11.1](https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/)


## Instalação

- Crie um ambiente e instale as bibliotecas necessárias
```python
>>> python -m venv venv
```
```python
(venv) >>> pip install -r requirements.txt
```

- Altere as configurações de conexão ao banco de dados em [utils.py](./src/utils.py)


## Utilização do projeto

- Rode o script [pipeline.py](./src/pipeline.py) para realizar o download, tratamento e upload dos dados necessários **ESSE PROCESSO PODE LEVAR UM TEMPO PARA FINALIZAR DEVIDO A QUANTIDADE DE DADOS ENTÃO PARA FACILITAR A AVALIAÇÃO É POSSÍVEL CANCELAR O PROCESSO A QUALQUER MOMENTO E CONTINUAR COM PARTE DOS DADOS SALVOS**
```python
(venv) >>> python .\export.py
```

- Execute o script [export.py](./src/export.py) para exportar os dados requisitados em csv e xlsx

## Observações gerais

- Caso algum bug seja encontrado, por favor me informe para que seja feita a correção imediata
