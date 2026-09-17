import os
import random
import string
import smtplib
from datetime import datetime
from email.message import EmailMessage
from functools import wraps

import mysql.connector
from dotenv import load_dotenv
from flask import (
    Flask, flash, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "troque-esta-chave-em-producao")

STATUS_VALIDOS = ["Pedido feito", "Pedido em produção", "Pedido entregue"]


def get_db():
    """Cria uma conexão nova com o MySQL."""
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", os.getenv("DB_HOST", "localhost")),
        port=int(os.getenv("MYSQLPORT", os.getenv("DB_PORT", "3306"))),
        user=os.getenv("MYSQLUSER", os.getenv("DB_USER", "root")),
        password=os.getenv("MYSQLPASSWORD", os.getenv("DB_PASSWORD", "")),
        database=os.getenv("MYSQLDATABASE", os.getenv("DB_NAME", "doacao_oculos")),
        autocommit=False,
    )


def gerar_protocolo(cursor):
    cursor.execute("""
        SELECT COALESCE(
            MAX(CAST(SUBSTRING(protocolo, 7) AS UNSIGNED)),
            0
        ) AS ultimo
        FROM pedidos
        WHERE protocolo LIKE 'pedido%'
    """)

    resultado = cursor.fetchone()
    proximo_numero = resultado[0] + 1

    return f"pedido{proximo_numero}"


def enviar_email(assunto, corpo):
    """
    Envia aviso para o e-mail do responsável.
    Se as variáveis SMTP não estiverem configuradas, apenas ignora o envio.
    A solicitação continua sendo salva normalmente no banco.
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_APP_PASSWORD")
    destino = os.getenv("CONTACT_EMAIL", "vitorlepesqueur@gmail.com")

    if not smtp_email or not smtp_password:
        app.logger.warning("SMTP não configurado. E-mail não enviado.")
        return False

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = smtp_email
    msg["To"] = destino
    msg.set_content(corpo)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:
            servidor.starttls()
            servidor.login(smtp_email, smtp_password)
            servidor.send_message(msg)
        return True
    except Exception as erro:
        app.logger.exception("Falha ao enviar e-mail: %s", erro)
        return False


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logado"):
            flash("Faça login para acessar a área administrativa.", "erro")
            return redirect(url_for("admin_login"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solicitar", methods=["POST"])
def solicitar():
    nome = request.form.get("nome", "").strip()
    endereco = request.form.get("endereco", "").strip()
    telefone = request.form.get("telefone", "").strip()
    rg = request.form.get("rg", "").strip()
    data_nascimento = request.form.get("data_nascimento", "").strip()
    crianca = request.form.get("crianca", "").strip()

    if not all([nome, endereco, telefone, rg, data_nascimento, crianca]):
        flash("Preencha todos os campos da solicitação.", "erro")
        return redirect(url_for("index") + "#solicitacao")

    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        protocolo = gerar_protocolo(cursor)

        cursor.execute(
            """
            INSERT INTO pedidos
            (protocolo, nome_solicitante, endereco, telefone, rg,
             data_nascimento, nome_crianca, status, data_pedido)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                protocolo, nome, endereco, telefone, rg,
                data_nascimento, crianca, "Pedido feito"
            ),
        )
        conn.commit()

        enviar_email(
            f"Nova solicitação de doação - {protocolo}",
            f"""Uma nova solicitação foi registrada.

Protocolo: {protocolo}
Solicitante: {nome}
Criança beneficiada: {crianca}
Telefone: {telefone}
Endereço: {endereco}
Status inicial: Pedido feito

Os documentos pessoais permanecem somente no banco de dados e não são enviados por e-mail.
""",
        )

        return render_template(
            "confirmacao.html",
            protocolo=protocolo,
            nome=nome,
            crianca=crianca,
        )
    except mysql.connector.Error:
        if conn:
            conn.rollback()
        app.logger.exception("Erro ao salvar solicitação.")
        flash("Não foi possível registrar a solicitação. Tente novamente.", "erro")
        return redirect(url_for("index") + "#solicitacao")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/acompanhar", methods=["GET", "POST"])
def acompanhar():
    pedido = None
    protocolo = ""

    if request.method == "POST":
        protocolo = request.form.get("protocolo", "").strip().upper()

        if not protocolo:
            flash("Informe o protocolo.", "erro")
            return render_template("acompanhar.html", pedido=None, protocolo="")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT protocolo, nome_crianca, status, data_pedido, atualizado_em
            FROM pedidos
            WHERE protocolo = %s
            """,
            (protocolo,),
        )
        pedido = cursor.fetchone()
        cursor.close()
        conn.close()

        if not pedido:
            flash("Protocolo não encontrado.", "erro")

    return render_template("acompanhar.html", pedido=pedido, protocolo=protocolo)


@app.route("/contato", methods=["POST"])
def contato():
    nome = request.form.get("nome_contato", "").strip()
    email = request.form.get("email_contato", "").strip()
    telefone = request.form.get("telefone_contato", "").strip()
    tipo = request.form.get("tipo_contato", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    if not all([nome, email, tipo, mensagem]):
        flash("Preencha nome, e-mail, tipo de contato e mensagem.", "erro")
        return redirect(url_for("index") + "#parcerias")

    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO mensagens
            (nome, email, telefone, tipo, mensagem, data_envio)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """,
            (nome, email, telefone, tipo, mensagem),
        )
        conn.commit()

        enviar_email(
            f"Novo contato pelo site - {tipo}",
            f"""Novo contato recebido pelo sistema.

Nome: {nome}
E-mail: {email}
Telefone: {telefone or "Não informado"}
Tipo: {tipo}

Mensagem:
{mensagem}
""",
        )

        flash("Mensagem enviada com sucesso. Obrigado pelo interesse!", "sucesso")
        return redirect(url_for("index") + "#parcerias")
    except mysql.connector.Error:
        if conn:
            conn.rollback()
        app.logger.exception("Erro ao salvar mensagem.")
        flash("Não foi possível enviar a mensagem. Tente novamente.", "erro")
        return redirect(url_for("index") + "#parcerias")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logado"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH", "")

        senha_ok = False
        if admin_password_hash:
            senha_ok = check_password_hash(admin_password_hash, senha)
        else:
            # Apenas para facilitar o primeiro teste local.
            senha_ok = senha == os.getenv("ADMIN_PASSWORD", "admin123")

        if usuario == admin_user and senha_ok:
            session["admin_logado"] = True
            return redirect(url_for("admin"))

        flash("Usuário ou senha incorretos.", "erro")

    return render_template("admin_login.html")


@app.route("/admin")
@admin_required
def admin():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, protocolo, nome_solicitante, telefone, nome_crianca,
               status, data_pedido, atualizado_em
        FROM pedidos
        ORDER BY data_pedido DESC
        """
    )
    pedidos = cursor.fetchall()

    cursor.execute(
        """
        SELECT id, nome, email, telefone, tipo, mensagem, data_envio
        FROM mensagens
        ORDER BY data_envio DESC
        """
    )
    mensagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin.html",
        pedidos=pedidos,
        mensagens=mensagens,
        status_validos=STATUS_VALIDOS,
    )


@app.route("/admin/pedido/<int:pedido_id>/status", methods=["POST"])
@admin_required
def atualizar_status(pedido_id):
    novo_status = request.form.get("status", "")

    if novo_status not in STATUS_VALIDOS:
        flash("Status inválido.", "erro")
        return redirect(url_for("admin"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE pedidos
        SET status = %s, atualizado_em = NOW()
        WHERE id = %s
        """,
        (novo_status, pedido_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Status atualizado com sucesso.", "sucesso")
    return redirect(url_for("admin"))


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/saude")
def saude():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
