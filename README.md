# Sistema de Doação de Óculos

Projeto desenvolvido para a faculdade com o objetivo de criar um sistema web para organizar pedidos de doação de óculos para crianças.

O sistema permite que uma pessoa faça uma solicitação, receba um código de acompanhamento e consulte o andamento do pedido.

Também existe uma área administrativa onde é possível alterar o status dos pedidos e visualizar mensagens enviadas por pessoas interessadas em fazer doações ou parcerias.

## Tecnologias utilizadas

* Python
* Flask
* HTML
* CSS
* JavaScript
* MySQL

## Funcionalidades

* Cadastro de solicitação de doação
* Geração de código para acompanhamento
* Consulta do andamento do pedido
* Status de pedido feito, em produção e entregue
* Área administrativa
* Alteração do status dos pedidos
* Formulário para contato, doações e parcerias
* Envio de aviso por e-mail

## Estrutura do projeto

O arquivo `app.py` contém a parte principal do sistema em Python.

A pasta `templates` contém as páginas HTML.

A pasta `static` contém os arquivos CSS e JavaScript.

O arquivo `schema.sql` é utilizado para criar o banco de dados MySQL e inserir alguns pedidos de exemplo.

## Como executar

É necessário ter Python e MySQL instalados.

Depois de baixar o projeto, instalar as bibliotecas com:

```bash
pip install -r requirements.txt
```

Criar o banco utilizando o arquivo:

```text
schema.sql
```

Depois criar o arquivo `.env` com as configurações do banco de dados e executar:

```bash
python app.py
```

O sistema poderá ser acessado pelo navegador em:

```text
http://127.0.0.1:5000
```

## Observação

Os dados que aparecem inicialmente no banco são apenas exemplos utilizados para demonstrar o funcionamento do sistema.

Este projeto foi desenvolvido como parte de um trabalho extensionista do curso de Análise e Desenvolvimento de Sistemas.
