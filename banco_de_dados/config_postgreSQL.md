Como Conectar ao PostgreSQL do Supabase com as Configurações Fornecidas
Você recebeu as credenciais do PostgreSQL no Supabase, mas sem a senha. Aqui está como conectar:

📌 Credenciais Necessárias
Host: aws-0-sa-east-1.pooler.supabase.com

Porta: 6543 (não a padrão 5432!)

Database: postgres

Usuário: postgres.fzqeuzyeamwgmauosenb (note o prefixo "postgres.")

Senha: (a que você definiu ao criar o projeto ou resetou depois)

🔧 Métodos de Conexão
1️⃣ Via psql (Linha de Comando)
bash
psql -h aws-0-sa-east-1.pooler.supabase.com -p 6543 -U postgres.fzqeuzyeamwgmauosenb -d postgres
▶ Digite a senha quando solicitado.

2️⃣ Via Cliente Gráfico (DBeaver, TablePlus, pgAdmin)
Abra seu cliente PostgreSQL.

Preencha os campos com:

Host: aws-0-sa-ea....

Port: 6543

Database: postgres

Username: postgres.fz....

Password: (sua senha)

Teste a conexão.

3️⃣ Via SQL Editor do Supabase (Recomendado para consultas rápidas)
✅ Acesse o painel do Supabase → SQL Editor
✅ Digite e execute queries diretamente (sem precisar de senha).

⚠️ Observações Importantes
Pool_mode: transaction → Indica que você está usando Connection Pooling (otimizado para aplicações).

Senha perdida? Redefina em:
Supabase Dashboard → Settings → Database → Reset Password.

Conexão bloqueada? Verifique se seu IP está na lista de permissões:
Supabase Dashboard → Settings → Database → Connection Pooling → Allowed IPs.

📚 Próximos Passos
Crie tabelas pelo Table Editor no Supabase.

Use a API REST automática (disponível em supabase.com/docs/guides/api).

Gerencie autenticação em Authentication → Settings.

Se precisar de ajuda, consulte a documentação oficial. 🚀