# Projeto desenvolvido no Evento da DIO: Community Week - AI Agentes

# <div align="center">
  <img src="https://img.shields.io/static/v1?label=AGENTE%20SQL%20SUPABASE&message=DIOBANK%20IA&color=36BCF7&style=for-the-badge&logo=supabase"/>
</div>

<div align="center">
  <h2>🛠️ Assistente de Consultas SQL com IA + PostgreSQL no Supabase</h2>
</div>

---

### **Tela do App**
![delta](img/tela_app.png)

- Link do App no Streamlit: https://auladioagentessq-wghwgk7esvbt6jm4ti8dt7.streamlit.app/

## 🔌 **Configuração Inicial**

### 1. Variáveis de Ambiente (`.env`)

```bash
# Supabase
POSTGRE_DB_HOST=aws-0-..
POSTGRE_DB_NAME=postgres
POSTGRE_DB_USER=postgres...
POSTGRE_DB_PASSWORD=****
POSTGRE_DB_PORT=6543
```

* Acesse as configurações do Postgres na pasta baco de dados.

```bash
# OpenAI
OPENAI_API_KEY=sk-...

2. Estrutura de Pastas

├── aula_dio_agentes_sq/
│   ├── agentes/scripts          
│   ├── streamlit_agente.py 
    └── terminal_agente.py 
```

🚀 Como Executar

# Instalar dependências
```bash
pip install -r requirements.txt
```
# Iniciar aplicação
```bash
streamlit run agente/scripts/streamlit_agent.py
```
## 📦 Dependências do Projeto

O projeto utiliza as seguintes bibliotecas Python:

```python
streamlit==1.29.0          # Framework para interface web
openai==0.28.0             # Integração com a API da OpenAI
python-dotenv==1.0.0       # Gerenciamento de variáveis de ambiente
faker==19.6.2              # Geração de dados fictícios para testes
psycopg2-binary==2.9.9     # Adaptador PostgreSQL para Supabase (versão leve)
```
<p align="left"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" title="Python"/> <img src="https://supabase.com/images/logo-light.png" width="200" title="Supabase"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="50" title="PostgreSQL"/> <img src="https://img.icons8.com/nolan/64/chatgpt.png" width="50" color=wait title="OpenAI"/> </p>



# Objetivo do Projeto:

- Construa um Agente que entende e responde com consultas SQL perfeitas, usando linguagem natural, sem precisar digitar queries complexas!
Nesta live com Maycon Cipriano, especialista de IA, você vai desenvolver um Agente de IA que irá otimizar seu tempo, simplificando consultas em bancos MySQL(adaptei para postgreSQL), gerando insights poderosos sem escrever códigos longos e demorados.

# Referências:

##  Professor:

### Maycon Cipriano

Especialista em IA

Especialista em IA generativa e PLN com foco em WatsonX. Lidera a maior comunidade técnica da IBM no Brasil (OIC Brazil Chapter).


### Pefil: [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/mayconbatestin/)
### Link da aula: [![YouTube](https://img.shields.io/badge/-YouTube-FF0000?style=flat-square&logo=YouTube&logoColor=white)](https://www.youtube.com/watch?v=336Zf7XfG2U&t=4701s)

Link Da DIO: https://www.dio.me/
##  Meus Contatos:

### Pefil: [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/mayconbatestin/)

[![WhatsApp](https://img.shields.io/badge/-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/5577999272367)
