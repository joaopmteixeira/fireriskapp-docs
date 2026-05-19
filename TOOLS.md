# Scripts Locais — Referência

Scripts em `tools/` estão **gitignored** — existem apenas na máquina local e nunca são commitados.
Este ficheiro documenta o que cada um faz e como o correr.

---

## `tools/backup_db.py` — Backup da base de dados

Exporta as tabelas `users` e `access_log` para ficheiros JSON em `tools/backups/<timestamp>/`.

**Quando usar:** antes de qualquer migração de schema, semanalmente em desenvolvimento ativo, antes de demos.

**Pré-requisitos:** `DATABASE_URL` definido, ou passar `--url` diretamente.

```powershell
# PowerShell — com URL explícito (recomendado)
python tools/backup_db.py --url "postgresql://postgres.[ref]:[password]@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"

# PowerShell — com variável de ambiente
$env:DATABASE_URL = "postgresql://..."
python tools/backup_db.py
```

```bash
# bash
DATABASE_URL="postgresql://..." python tools/backup_db.py
```

**Output gerado** em `tools/backups/YYYY-MM-DD_HH-MM-SS/`:

- `users.json` — todos os campos (inclui hashes bcrypt, emails)
- `access_log.json` — log de acessos
- `meta.json` — timestamp, contagem de linhas, host

**Segurança:** os ficheiros contêm e-mails (PII). Não partilhar em locais públicos.

**Backup automático:** o workflow `.github/workflows/backup-db.yml` corre este script de 3 em 3 dias via GitHub Actions e guarda o resultado como artifact (90 dias de retenção). Requer o secret `DATABASE_URL` configurado no repositório GitHub → Settings → Secrets and variables → Actions.

---

## `tools/create_test_user.py` — Criar utilizador de teste

Cria um utilizador de teste na base de dados local (SQLite) sem passar pelo fluxo de verificação de e-mail.

**Pré-requisitos:** nenhum (usa SQLite local por omissão).

```powershell
python tools/create_test_user.py
```

Cria: `username=test`, `password=test`, `email=test@local.dev`, `verified=1`.

**Nota:** não usar com `DATABASE_URL` apontado para produção.

---

## `tools/dev-backend.ps1` — Arrancar backend em desenvolvimento

Arranca o FastAPI em modo desenvolvimento com reload automático (porta 8000).
Contém variáveis de ambiente locais — por isso está gitignored.

```powershell
.\tools\dev-backend.ps1
```

Equivalente a:

```powershell
$env:DATABASE_URL = "..."   # SQLite local ou Supabase dev
uvicorn main:app --reload --port 8000 --app-dir app/backend
```

---

## `tools/migrate_neon_to_supabase.py` — Migração Neon → Supabase *(histórico)*

Script usado em DB-02 (2026-05-15) para migrar os dados de Neon para Supabase.
Mantido para referência; a migração já foi concluída.

**Pré-requisitos:** `NEON_DATABASE_URL` e `SUPABASE_DATABASE_URL`.

```powershell
python tools/migrate_neon_to_supabase.py
python tools/migrate_neon_to_supabase.py --with-logs   # inclui access_log
```

---

## `tools/pdf_to_ai_markdown.py` — PDF → Markdown para IA

Converte PDFs de investigação (tese, artigos) para markdown otimizado para leitura por IA.
Usado para gerar os ficheiros em `docs/research/`.

**Pré-requisitos:** `pypdf` instalado (`pip install pypdf`).

```powershell
python tools/pdf_to_ai_markdown.py caminho/para/ficheiro.pdf
```

---

## `tools/fix_fences.py` — Corrigir fences em markdown *(utilitário interno)*

Processa ficheiros markdown em `docs/plans/` e corrige caracteres Unicode mal formatados
resultantes de cópias de editores externos.

```powershell
python tools/fix_fences.py
```

---

## `tools/fix_markdown_lint.ps1` — Corrigir violações markdownlint em docs/

Corre `markdownlint-cli2 --fix` em todos os ficheiros `.md` dentro de `docs/`,
corrigindo automaticamente as violações fixable e listando as que requerem
atenção manual. Usa o ficheiro de configuração `.markdownlint.json` da raiz.

`docs/research/` é excluído — ficheiros gerados automaticamente a partir de PDFs.

**Pré-requisitos:** Node.js / npx instalado.

```powershell
.\tools\fix_markdown_lint.ps1
```

```bash
# bash
pwsh tools/fix_markdown_lint.ps1
```

**Output esperado:**

```text
[fix]  A corrigir docs/**/*.md ...
[lint] A verificar violacoes restantes ...
[ok]   Todos os ficheiros limpos.
```

Se existirem violações não auto-fixable, são listadas com ficheiro e linha.
