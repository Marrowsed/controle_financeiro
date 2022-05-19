![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
[![CodeQL](https://github.com/Marrowsed/Desafio_Alura3/actions/workflows/codeql.yml/badge.svg)](https://github.com/Marrowsed/Desafio_Alura3/actions/workflows/codeql.yml)

# Controle Financeiro

## ✔️ Tecnologias utilizadas

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/2560px-Django_logo.svg.png" alt="Logo do Django">

- ``Python``
- ``PostgreSQL``
- ``PyCharm``

## ✔️ Técnicas utilizadas

- ``MVC``
- ``CRUD das Classes``
- ``Gráficos``

## Serviços

- Organize sua vida financeira pelas Contas de seu Banco ! Faça operações de Tranferência entre contas, Compras parceladas, Compras à vista e tenha um controle de tudo em uma só tela !
- Faça o filtro de Faturas por mês e por ano !
- Faça uma comparação em gráficos dos meses, quando gastou mais ou menos !
- Não fique mais preso em Planilhas extensas de Excel, atualize-se !

## Instalação
É necessária a Instalação mais recente do <a href="https://www.python.org/downloads/" target="_blank">Python</a>

## Dependências</h2>

````sh
pip install -r requirements.txt
````

## Configuração 
<ol>
  <li> Crie um arquivo `.env` na mesma pasta onde está o arquivo `migrate.py`.</li>
  <li>No seu terminal com o ambiente virtual ativado, execute o comando `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` para gerar uma chave secreta.</li>
  <li>Substitua a chave secreta no arquivo `.env` com a chave gerada na variável `SECRET_KEY`.</li>
  <li>Substitua o endereço do banco de dados no arquivo `.env` com o endereço do banco de dados que você deseja utilizar na variável `DATABASE_URL`.</li>
  <li>Execute o comando `python manage.py migrate` para criar as tabelas do banco de dados.</li>
</ol>

## Rodando o projeto

```sh
python manage.py runserver
```

O servidor está rodando, visite http://127.0.0.1:8000/ no seu navegador de internet
