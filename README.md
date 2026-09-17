# Visão para o Futuro

Sistema web acadêmico para solicitação e acompanhamento de doações de óculos para crianças.

## Tecnologias
- Python + Flask
- HTML5
- CSS3
- JavaScript
- MySQL

## Funcionalidades
- Solicitação de doação
- Geração de protocolo
- Acompanhamento de status
- Formulário de doações e parcerias
- Envio de avisos por e-mail
- Área administrativa protegida por login
- Atualização de status
- Registros demonstrativos iniciais

## Estrutura
```
sistema_doacao_oculos/
├── app.py
├── schema.sql
├── requirements.txt
├── Procfile
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── confirmacao.html
│   ├── acompanhar.html
│   ├── admin_login.html
│   └── admin.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Teste local resumido

1. Instale Python 3 e MySQL 8.
2. Crie um ambiente virtual:
   - Windows: `python -m venv venv`
3. Ative:
   - PowerShell: `.\venv\Scripts\Activate.ps1`
4. Instale:
   - `pip install -r requirements.txt`
5. Copie `.env.example` para `.env` e preencha.
6. Execute `schema.sql` no MySQL.
7. Rode:
   - `python app.py`
8. Abra:
   - `http://127.0.0.1:5000`

## Segurança para demonstração

Não use dados pessoais reais no site acadêmico público. Os registros de exemplo são fictícios.

Em produção, prefira `ADMIN_PASSWORD_HASH` em vez de senha em texto simples.

Para gerar um hash:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("SUA-SENHA-FORTE"))
```
Copie o resultado para `ADMIN_PASSWORD_HASH`.

## Railway

O projeto foi preparado para implantação via Gunicorn com `gunicorn app:app`.
O banco pode ser provisionado como MySQL no mesmo projeto Railway.
