# app.py (VERSÃO FINAL COM PAINEL ADMIN)

import os
import psycopg2
import datetime
import uuid
import functools
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)

# IMPORTANTE: Mude esta chave para uma frase secreta única e complexa!
# Ela protege as sessões de login do seu painel.
app.secret_key = 'substitua-por-uma-chave-muito-longa-e-aleatoria-aqui'

# Pega a URL de conexão do banco de dados das variáveis de ambiente (configurada no Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

# SENHA DO PAINEL ADMIN (mude para uma senha forte de sua preferência)
ADMIN_PASSWORD = "admin" 

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def setup_database():
    """Cria a tabela de licenças se ela não existir."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tabela_licencas (
                id SERIAL PRIMARY KEY,
                chave_licenca TEXT UNIQUE NOT NULL,
                hardware_id TEXT,
                data_criacao DATE NOT NULL DEFAULT CURRENT_DATE,
                data_expiracao DATE NOT NULL,
                status TEXT NOT NULL DEFAULT 'DISPONIVEL' -- pode ser: DISPONIVEL, ATIVA, EXPIRADA
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao configurar o banco de dados: {e}")

# Decorator para proteger rotas que exigem login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# --- ROTAS DA API (para o seu programa desktop) ---

@app.route('/')
def home():
    """Rota simples para verificar se a API está online."""
    return "Servidor de Licenças GESTUPSYSTEM está online!"

@app.route('/api/ativar', methods=['POST'])
def api_ativar():
    dados = request.json
    chave = dados.get('chave_licenca')
    hw_id = dados.get('hardware_id')

    if not chave or not hw
