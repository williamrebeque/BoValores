# BoValores

Projeto desafio proposto pela Inoa.

O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, ele deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

Os seguintes requisitos funcionais são necessários:
- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável, para consulta posterior
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo
- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior

## Setup

A primeira coisa a fazer é instalar as dependências:

```sh
(env)$ pip install -r requirements.txt
```
O `(env)` na frente assume que você ja esteja em seu ambiente de desenvolvimento

Depois de instalado as dependências, adicione o cron para pesquisa dos preços dos ativos:
```sh
(env)$ python manage.py crontab add
```
Isso irá ativar a pesquisa dos preços e o disparo de email quando o ativo atingir seus limites.

Agora, rode o servidor:
```sh
(env)$ python manage.py runserver
```

Navegue para `http://127.0.0.1:8000`.

## Email

Para simular o envio de email, foi utilizado um servidor `teste` na porta 1025

Execute em um novo terminal:
```sh
$ python -m smtpd -n -c DebuggingServer localhost:1025
```
Todas as requisições de envio de email irá aparecer como log no terminal.

As configurações de email se encontram no arquivo `settings.py`:
```py
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'informativo@bovalores.com'
```

## Login

Foi criado um usuário padrão no qual já existem alguns ativos cadastrados e com históricos.

Para logar no sistema utilize as seguintes informações:
```
Login: inoa
Senha: 1n04515t3m45
```

## Cron

Para desativar o cron e não ficar buscando os ativos em background utilize o comando:
```sh
(env)$ python manage.py crontab remove
```