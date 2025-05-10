import csv
import random
import mysql.connector
from faker import Faker
from datetime import datetime
import os
from dotenv import load_dotenv
import psycopg2

# Carregar credenciais do MYSQL e declarar variaveis
load_dotenv()
n = 100  # Número de registros a serem gerados
database=os.getenv("SUPABASE_DB_NAME")
conn = psycopg2.connect(
    host=os.getenv("SUPABASE_DB_HOST"),
    port=os.getenv("SUPABASE_DB_PORT"),
    database=os.getenv("SUPABASE_DB_NAME"),
    user=os.getenv("SUPABASE_DB_USER"),
    password=os.getenv("SUPABASE_DB_PASSWORD")
)

cursor = conn.cursor()
cursor.execute("SELECT 1;")
print("Conexão com o Supabase bem-sucedida!")

# Criar as tabelas no banco de dados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        cliente_id SERIAL PRIMARY KEY,
        nome VARCHAR(100),
        cpf VARCHAR(11),
        email VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS enderecos (
        endereco_id SERIAL PRIMARY KEY,
        cliente_id INT,
        rua VARCHAR(255),
        cidade VARCHAR(100),
        estado VARCHAR(50),
        cep VARCHAR(8),
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos (
        pagamento_id SERIAL PRIMARY KEY,
        cliente_id INT,
        valor DECIMAL(10, 2),
        data_pagamento DATE,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        movimentacao_id SERIAL PRIMARY KEY,
        cliente_id INT,
        tipo_movimentacao VARCHAR(50),
        valor DECIMAL(10, 2),
        data_movimentacao DATE,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    )
""")
conn.commit()
# Inicializar o Faker para gerar dados fictícios
fake = Faker()

# Função para exportar os dados para CSV
def export_to_csv(query, filename, headers):
    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Exportado para {filename}")
    else:
        print(f"Sem dados para exportar na consulta: {query}")

# Gerar dados e inserir no banco de dados
for linha in range(n):
    nome = fake.name()
    cpf = random.randint(11111111111,99999999999)
    email = fake.email()

    cursor.execute("""
        INSERT INTO clientes (nome, cpf, email)
        VALUES (%s, %s, %s)
    """, (nome, cpf, email))
    conn.commit()
    cliente_id = cursor.lastrowid
    cursor.execute("SELECT MAX(cliente_id) FROM clientes")

    # Recuperando o resultado da consulta
    cliente_id = cursor.fetchone()[0]
    
    # Gerar endereço
    rua = fake.street_address()
    cidade = fake.city()
    estado = fake.state()
    cep = fake.zipcode()

    cursor.execute("""
        INSERT INTO enderecos (cliente_id, rua, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s)
    """, (cliente_id, rua, cidade, estado, cep))
    conn.commit()
    # Gerar movimentação bancária
    tipo_movimentacao = random.choice(['depósito', 'saque', 'transferência'])
    valor = round(random.uniform(50.0, 5000.0), 2)
    data_movimentacao = fake.date_this_year()

    cursor.execute("""
        INSERT INTO movimentacoes (cliente_id, tipo_movimentacao, valor, data_movimentacao)
        VALUES (%s, %s, %s, %s)
    """, (cliente_id, tipo_movimentacao, valor, data_movimentacao))
    conn.commit()
    # Gerar pagamento
    valor_pagamento = round(random.uniform(20.0, 1000.0), 2)
    data_pagamento = fake.date_this_year()

    cursor.execute("""
        INSERT INTO pagamentos (cliente_id, valor, data_pagamento)
        VALUES (%s, %s, %s)
    """, (cliente_id, valor_pagamento, data_pagamento))

    # Commit as mudanças no banco
    conn.commit()

# Exportar os dados das tabelas para CSV
export_to_csv("SELECT * FROM clientes", 'banco_de_dados/datasets/clientes.csv', ['cliente_id', 'nome', 'cpf', 'email'])
export_to_csv("SELECT * FROM enderecos", 'banco_de_dados/datasets/enderecos.csv', ['endereco_id', 'cliente_id', 'rua', 'cidade', 'estado', 'cep'])
export_to_csv("SELECT * FROM movimentacoes", 'banco_de_dados/datasets/movimentacoes.csv', ['movimentacao_id', 'cliente_id', 'tipo_movimentacao', 'valor', 'data_movimentacao'])
export_to_csv("SELECT * FROM pagamentos", 'banco_de_dados/datasets/pagamentos.csv', ['pagamento_id', 'cliente_id', 'valor', 'data_pagamento'])

# Fechar a conexão com o banco de dados
cursor.close()
conn.close()
