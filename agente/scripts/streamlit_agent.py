import psycopg2
import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# --- CONFIGURAÇÃO DA PÁGINA STREAMLIT ---
st.set_page_config(page_title="DIOBANK AI", page_icon="🏛️🤖")
st.title("🏛️🤖 DioBank AI - Consultas SQL")

# --- CONFIGURAÇÃO DA SIDEBAR (INSERÇÃO DE CREDENCIAIS) ---
st.sidebar.header("🔐 Configurações")
openai_api_key = st.sidebar.text_input("Chave da API OpenAI", type="password", value=os.getenv("OPENAI_API_KEY"))
db_host = st.sidebar.text_input("PostgreSQL Host", value=os.getenv("POSTGRE_DB_HOST"))
db_user = st.sidebar.text_input("Usuário PostgreSQL", value=os.getenv("POSTGRE_DB_USER"))
db_password = st.sidebar.text_input("Senha PostgreSQL", type="password", value=os.getenv("POSTGRE_DB_PASSWORD"))
db_name = st.sidebar.text_input("Nome do Banco de Dados", value=os.getenv("POSTGRE_DB_NAME"))
db_port = st.sidebar.text_input("Porta", value="5432")  # Porta padrão do PostgreSQL

# --- MEIO: INTERAÇÃO COM O USUÁRIO E ENTRADA DA PERGUNTA ---
if "pergunta" not in st.session_state:
    st.session_state.pergunta = ""

# Sugestões de perguntas
st.markdown("### 💬 Sugestões de perguntas")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📋 Clientes"):
        st.session_state.pergunta = "Me mostre todos os clientes"
with col2:
    if st.button("💸 Pagamentos"):
        st.session_state.pergunta = "Me mostre todos os pagamentos"
with col3:
    if st.button("🏠 Endereços"):
        st.session_state.pergunta = "Me mostre todos os endereços"
with col4:
    if st.button("📈 Movimentações"):
        st.session_state.pergunta = "Me mostre todas as movimentações"

# Campo de pergunta
st.markdown("### ✍️ Pergunta personalizada")
pergunta = st.text_input("Digite sua pergunta em linguagem natural:", 
                         value=st.session_state.pergunta, 
                         key="input_pergunta")

# --- FUNÇÕES AUXILIARES ---
def carregar_prompt():
    try:
        with open("protocolos/prompt.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar o contexto do prompt: {e}")
        return {}

def obter_estruturas_tabelas():
    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            sslmode='require'
        )
        cursor = conn.cursor()
        
        # Obter tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE';
        """)
        tabelas = [t[0] for t in cursor.fetchall()]

        colunas = {}
        for tabela in tabelas:
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{tabela}'
                ORDER BY ordinal_position;
            """)
            colunas_tabela = {c[0]: c[1] for c in cursor.fetchall()}
            colunas[tabela] = colunas_tabela

        cursor.close()
        conn.close()
        return colunas
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return {}

def gerar_query_sql(pergunta, colunas):
    if not openai_api_key:
        st.error("🔑 Por favor, insira sua chave da API OpenAI na sidebar")
        return ""

    openai.api_key = openai_api_key
    prompt = carregar_prompt()

    instrucoes_adicionais = "\n- " + "\n- ".join(prompt.get("instrucoes_sql", []))

    contexto = f"""
Sistema: {prompt.get('system_name', 'Desconhecido')}
Função do modelo: {prompt.get('model_role', '')}
Perfil do usuário: {prompt.get('user_profile', {})}
Restrições: {'; '.join(prompt.get('restricoes', []))}

Instruções adicionais para gerar SQL corretamente:
{instrucoes_adicionais}

Estrutura do banco de dados:
{json.dumps(colunas, indent=2, ensure_ascii=False)}

Pergunta do usuário:
{pergunta}

Gere uma consulta SQL PostgreSQL correspondente:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt.get('model_role', "Você é um assistente de SQL especializado em PostgreSQL.")},
                {"role": "user", "content": contexto}
            ],
            max_tokens=300,
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        return query.replace("```sql", "").replace("```", "").strip()
    except Exception as e:
        st.error(f"Erro ao gerar a query SQL: {e}")
        return ""

def executar_query(query):
    if not query:
        st.warning("⚠️ A consulta SQL está vazia. Verifique sua pergunta ou o contexto.")
        return [], []

    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            sslmode='require'
        )
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return colunas, resultados
    except Exception as e:
        st.error(f"Erro ao executar a query SQL: {e}")
        return [], []

def salvar_historico(pergunta, query, resultado):
    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            sslmode='require'
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_interacoes (
                id SERIAL PRIMARY KEY,
                pergunta TEXT,
                query_gerada TEXT,
                resultado TEXT,
                feedback VARCHAR(10),
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.execute("""
            INSERT INTO historico_interacoes (pergunta, query_gerada, resultado)
            VALUES (%s, %s, %s)
        """, (pergunta, query, str(resultado)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao salvar histórico: {e}")

def salvar_feedback(pergunta, feedback):
    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            sslmode='require'
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE historico_interacoes
            SET feedback = %s
            WHERE pergunta = %s
            ORDER BY data DESC LIMIT 1;
        """, (feedback, pergunta))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Feedback salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar feedback: {e}")

# --- EXECUÇÃO PRINCIPAL ---
if pergunta:
    estrutura = obter_estruturas_tabelas()
    if estrutura:
        query = gerar_query_sql(pergunta, estrutura)

        # Botão para exibir ou não a query SQL
        mostrar_sql = st.toggle("👁️ Mostrar consulta SQL")
        if mostrar_sql:
            st.code(query, language="sql")

        if st.button("Executar consulta"):
            colunas, resultados = executar_query(query)

            if resultados:
                st.success("✅ Consulta realizada com sucesso!")
                st.dataframe([dict(zip(colunas, row)) for row in resultados])
                salvar_historico(pergunta, query, resultados)
            else:
                st.warning("Nenhum resultado encontrado.")

            feedback = st.radio("Essa resposta foi útil?", ("👍 Sim", "👎 Não"), key="feedback")
            if st.button("Enviar feedback"):
                salvar_feedback(pergunta, feedback.split()[1])