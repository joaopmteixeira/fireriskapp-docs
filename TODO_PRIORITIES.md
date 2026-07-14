# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-07-13 (reorganização MODEL/FEAT — início MODEL-01, migração v4.0)

---

## Prefixos de ID

- **`REL`** — Releases e versionamento
- **`AUTH`** — Autenticação e sessões (AUTH-01…05 concluídos — ver CHANGELOG)
- **`DB`** — Base de dados e persistência
- **`SEC`** — Segurança e hardening (não-auth)
- **`UI`** — Interface e experiência do utilizador
- **`UX`** — Micro-melhorias de experiência (UX-01…08 concluídos — ver CHANGELOG)
- **`FEAT`** — Funcionalidades novas da aplicação
- **`BACK`** — Arquitetura e código backend
- **`INFRA`** — Infraestrutura, deploy e DevOps
- **`TEST`** — Testes e validação
- **`DOCS`** — Documentação
- **`MODEL`** — Modelo CHICHORRO (migração de versões v4.0 → v4.1 → v5.0)
- **`AI`** — AI tooling e knowledge graph (Graphify, Obsidian, RAG)
- **`B`** — Tarefas de manutenção/organização

---

## Por Concluir / Pendente

### Prioridade Alta

#### 🔄 MODEL-01 — v4.0 (Inês Casas) — modelo completo (MARI)

Trazer para o backend atual (`app/backend/calc/`) o trabalho da dissertação de Inês Casas
(v4.0), começando pelo modelo completo (MARI); o modelo simplificado (MAGR, MODEL-02) fica
para depois. Verificação linha-a-linha (PHP v4.0 vs Python atual vs tese cap.3) já concluída
— ver
[CHICHORRO_V4_MARI_VERIFICATION_REPORT.md](plans/main/CHICHORRO_V4_MARI_VERIFICATION_REPORT.md)
e
[CHICHORRO_V4_MARI_IMPLEMENTATION_PLAN.md](plans/main/CHICHORRO_V4_MARI_IMPLEMENTATION_PLAN.md).

Sub-tarefas identificadas (alta prioridade — bugs/gaps reais):

- MODEL-01a — `DPI_VDGF`: reimplementar como tabela cruzada fiel à Tabela 3.10 da tese.
- MODEL-01b — `DPI_OGS`: reimplementar como tabela cruzada fiel à Tabela 3.11 da tese.

### Prioridade Média

#### ❌ TEST-04 — Smoke tests Docker Compose

Suite mínima de testes pós-deploy: `/health`, `/health/db`, login, logout, sessão, CSRF, frontend build. Gate de qualidade para cada deploy.

Ver [TEST-04_UNDONE.md](plans/subplans/TEST/TEST-04_UNDONE.md).

---

#### ❌ CALC-AUDIT — Golden tests do código de cálculo

~280 testes automatizados a validar o motor CHICHORRO (POI/CTI/DPI/ESCI/RI) contra os valores da tese3.1.
**Bloqueado** até os ficheiros Excel da tese3.1 estarem disponíveis.

---

#### ❌ UI-14 — Corrigir dark mode em toda a app

Detetado durante testes de UI-13 (2026-07-02): contraste/legibilidade inconsistentes em
dark mode, não só nas páginas admin (Utilizadores, Access Log, Suporte) mas em várias
páginas da app. Precisa de revisão visual completa, não só um fix pontual.

---

### Prioridade Baixa

#### ❌ SEC-15 — CAPTCHA (Cloudflare Turnstile) no formulário de suporte

`POST /support/request` (UI-11) é público e só tem rate limiting (3/hora). Adicionar
Cloudflare Turnstile: verificação `siteverify` no backend (httpx, já dependência),
widget no `SupportModal.tsx`, novo env `TURNSTILE_SECRET_KEY` (backend) e
`VITE_TURNSTILE_SITE_KEY` (frontend). Funciona independentemente de o frontend estar
em Cloudflare Pages ou numa futura VPS — só exige domínio associado à Cloudflare
(já o caso via Cloudflare Tunnel, INFRA-09). Ver [SEC-15_UNDONE.md](plans/subplans/SEC/SEC-15_UNDONE.md).

---

#### ❌ UI-02 — Página de Documentação

Criar página de DOCS na app com documentação e manuais de utilização.

---

#### ❌ UI-03 — Página de Ajuda

Criar página HELP integrada na app com respostas rápidas às dúvidas mais comuns.

---

#### ❌ UI-04 — FAQs — Perguntas Frequentes

Criar página de perguntas frequentes integrada na app.

---

#### ❌ UI-05 — Sistema de Reporte de Bugs

Formulário de reporte de bugs na app; canal de destino a definir (email, GitHub Issues ou ClickUp).

---

#### ❌ UI-08 — Ícones de informação nos subfatores

Ícone ℹ️ em cada subfator POI/CTI/DPI/ESCI; painel com descrição detalhada do subfator (o que mede, valores esperados, como interpretar), tabela de valores e referência RT-SCIE. Torna a app autónoma para utilizadores sem formação prévia no modelo CHICHORRO.

---

#### ❌ UI-09 — Badge de lápis persistente no avatar

O ícone de câmara no avatar é apenas visível no hover (`opacity-0 group-hover:opacity-100`) — invisível em mobile. Substituir por um badge circular persistente com `mdiPencil` no canto inferior-direito, sempre visível, seguindo o padrão Gmail/LinkedIn.

Ver [UI-09_UNDONE.md](plans/subplans/UI/UI-09_UNDONE.md).

---

#### ❌ UI-10 — Sidebar direita — resumo de sessão e subfatores

Painel lateral direito persistente, colapsável, com resumo da sessão atual: valores introduzidos nos subfatores (POI/CTI/DPI/ESCI), resultado RI calculado e estado dos campos em falta. Visível durante o preenchimento e o cálculo para referência rápida sem necessidade de navegar entre páginas.

---

#### ❌ AI-03 — RAG — botão "Explicar" por subfator

pgvector + `routers/rag.py` + botão "Explicar" em cada subfator POI/CTI/DPI/ESCI. Permite ao utilizador obter uma explicação contextual do subfator com base nas dissertações e no RT-SCIE, sem sair da app. Implementar após AI-02a concluído.

---

#### ❌ AI-02a — Curation manual do vault Obsidian

Trabalho manual residual do [AI-02](plans/subplans/AI-02.md): (1) preencher `## Definicao` nas 27 notas de subfator; (2) validar entradas "verificar" em `## Onde e mencionado` (confirmar Sim/Não e correr `map_sources.py` para limpar); (3) abrir vault no Obsidian e verificar Graph View e cores por tipo de nó.

Ver [AI-02a_UNDONE.md](plans/subplans/AI/AI-02a_UNDONE.md).

---

### Futuro / Sem prioridade definida

#### Nota — Subdomínio `admin.dominio` separado

Avaliado em 2026-07-02: não vale a pena atualmente. Admin (`AdminUsersPage`,
`AdminLogPage`, `AdminSupportPage`) vive no mesmo bundle React (`/app/admin/*`,
`RequireAuth`) e mesma app FastAPI (`routers/admin.py`, `Depends(require_admin)`).
A proteção real é sessão + `role == "admin"`, não a URL — um subdomínio próprio
não acrescenta segurança e implica custo de infra desproporcional (novo deploy
Cloudflare Pages, CORS extra, cookies cross-subdomain) para um projeto de
1 developer. Reconsiderar se um dia houver admins externos (ex: terceiros a
gerir suporte) ou se o bundle React crescer muito — nesse caso, a alternativa
mais barata é lazy loading (`React.lazy`) das páginas admin em vez de separar
por subdomínio.

---

#### ❌ SEC-14 — SOPS + age (gestão de secrets encriptados em Git)

Encriptação de secrets com SOPS + age para ambientes com múltiplos developers ou GitOps.
Inclui: `deploy/secrets/staging.sops.yaml`, `decrypt-secrets.sh`, Docker Compose Secrets,
role `chichorro_backup`, Gitleaks avançado. Referência: `docs/plans/main/SECRETS_MANAGEMENT_PLAN.md`.
**Não prioritário enquanto o projeto tiver 1 developer e secrets fora do Git.**

---

#### ❌ FEAT-01 — Gráfico de Impacto de Intervenções

Bar chart horizontal (tornado chart) com impacto individual de cada intervenção. Backend: `POST /RI/interv/impact` (~34 cálculos de RI por chamada). Frontend: Recharts (já disponível no projeto).

---

#### ❌ FEAT-02 — Guardar Edifício

Após cálculo completo, guardar avaliação com nome, morada, código postal, Distrito/Concelho/Freguesia (dropdowns em cascata), latitude/longitude + pin no mapa. Ver [FEAT-02_UNDONE.md](plans/subplans/FEAT/FEAT-02_UNDONE.md).

---

#### ❌ FEAT-03 — Chatbot AI

Assistente de IA para ajudar utilizadores a compreender o CHICHORRO e usar a aplicação (via Claude API ou similar).

---

#### ❌ FEAT-04 — Geração de relatório em PDF

Exportar resultados RI, CTI e subfatores (POI/DPI/ESCI) para ficheiro PDF imprimível e partilhável após cálculo completo.

---

#### ❌ FEAT-05 — Método simplificado baseado no CHICHORRO 2.0

Proposta de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1.

---

#### ❌ FEAT-06 — Alterar ordem do Cenário 4

CI → VVE → VHE alternativo.

---

#### ❌ FEAT-07 — Afinação de custos €/m² via "PRONIC" ou similar com atualização automática de base de dados de custos

---

#### ❌ FEAT-08 — Intervenções adicionais

Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa.

---

#### ❌ FEAT-09 — Georreferenciação e base de dados de edifícios

---

#### ❌ FEAT-10 — Tratamento de edifícios devolutos

---

#### ❌ FEAT-11 — Integração com Firecheck 2.0

---

## Concluídos

### Prioridade Alta

#### ✅ SEC-13 — Hardening stack Docker *(2026-06-18, `feat/sec13-docker-hardening`)*

Gitleaks CI (`secrets-scan` job antes de `test`); padrão `*_FILE` em `config.py` via `model_validator`; testes `test_config.py`; redes Docker internas (`edge`/`data` com `internal: true`); serviço `migrate` isolado (alembic separado do `app`); `deploy/systemd/chichorro.service` para autostart após reboot; docs `ENV_VARS.md`, `SECRETS_POLICY.md`, `DEPLOY_PROXMOX_DEBIAN.md` atualizados. Validado na VM staging.

---

#### ✅ DB-09 — Roles de BD + política de backups (diário/trienal/mensal) *(2026-06-17, `3.1-dev`)*

Migração Alembic `0004_create_db_roles.py` cria 3 roles (`chichorro_admin`, `chichorro_runtime`, `chichorro_readonly`) com `IF NOT EXISTS` e `ALTER DEFAULT PRIVILEGES`; `backup.sh` refatorado com política diferenciada (daily 7d, triennial 30d, monthly permanente); 3 cron entries no docker-compose.staging.yml; subplan `DB-09.md`.

---

#### ✅ INFRA-09 — Cloudflare Tunnel para chichorro.joaopmteixeira.net *(2026-06-15, `feat/infra09-cloudflare-tunnel`)*

`infra/cloudflare/config.yml` (template tunnel); `docker-compose.staging.yml` com `CHICHORRO_CORS_ORIGINS` e `APP_BASE_URL` atualizados; runbook INFRA-09 em `DEPLOY_PROXMOX_DEBIAN.md`; `cloudflared` instalado na VM como serviço systemd. Validado: `https://chichorro.joaopmteixeira.net/health/db` → ok.

---

#### ✅ DB-08 — Runbook migração Supabase → PostgreSQL local *(2026-06-15, `feat/db07-db08-backups`)*

Script `scripts/migrate_supabase_to_local.sh` (pg_dump + drop/recreate + pg_restore + validação de contagens); runbook operacional completo `docs/deploy/RUNBOOK_MIGRATION_SUPABASE_TO_LOCAL.md` com 5 passos, plano de fallback 7 dias, rollback e migração de produção. Validado em staging: 65 access_log + 2 users migrados, login e cálculo POI→RI OK.

---

#### ✅ DB-07 — Backups PostgreSQL local *(2026-06-15, `feat/db07-db08-backups`)*

Serviço Docker `backup` (postgres:17-alpine) com cron diário 02:00 UTC via `pg_dump -F c`; retenção 7 dumps; `infra/backup/backup.sh` + `infra/backup/restore.sh`; volume `backup_dumps`; healthcheck falha se dump > 25h; secção operacional em `DEPLOY_PROXMOX_DEBIAN.md`. Validado em staging: dump criado, restore OK, `/health/db` → ok.

---

#### ✅ INFRA-07 — Staging Proxmox completo (Nginx + PostgreSQL local) *(2026-06-15, `3.1-dev`)*

`docker-compose.staging.yml` com `db` (PostgreSQL 16) + `app` (ENV=staging) + `nginx` (porta 80); `infra/nginx/nginx.conf` reverse proxy com headers proxy correctos; stack operacional em chichorro-staging (192.168.0.7); `/health/db` → ok.

---

#### ✅ REL-01 — Release baseline v3.1.0 *(2026-06-12, `3.1-dev`)*

Tag `v3.1.0` criada no GitHub; release notes publicadas em CHANGELOG.md com sumário completo das funcionalidades 3.1 (modelo, autenticação, segurança, infraestrutura Docker/Proxmox).

---

#### ✅ INFRA-06 — Separação de ambientes + deploy Proxmox/Debian 13 *(2026-06-11, `feat/infra07-env-proxmox` → `3.1-dev`)*

`.env` (gitignored) com credenciais de admin para dev local e Proxmox; `.env.example` (commitado) com template documentado de todas as variáveis; `docker-compose.yml` com `env_file` (`required: false` para CI); `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — guia de instalação Docker em Debian 13 e deploy da app.

---

#### ✅ DB-06 — Migrar camada de dados para SQLAlchemy ORM *(2026-06-09, `refactor/db06-sqlalchemy` → `3.1-dev`)*

SQLAlchemy 2.x com `DeclarativeBase`/`mapped_column`; `NullPool` para Neon PgBouncer; `migrate_sqlite()` para evolução de schema em dev; WAL pragma; Alembic autogenerate wired a `Base.metadata`. Code review high effort (6 findings F1-F6 corrigidos): IntegrityError handler, None guards, column projection em admin, WAL. 342 testes pass; verificação `/health/db` e registo concorrente → 409 OK.

---

#### ✅ INFRA-03 — Dockerfile + Compose *(2026-06-09, `3.1-dev`)*

Dockerfile Python 3.14-slim + docker-compose.yml (backend + PostgreSQL 16); `.dockerignore`; utilizador `appuser` não-root.

---

#### ✅ SEC-04b — Remoção do fallback werkzeug *(2026-05-28, `3.1-dev`)*

Werkzeug removido de `auth.py` e `requirements.txt` após confirmação que todos os hashes são `$argon2id`.

---

#### ✅ SEC-04 + SEC-05 + SEC-07 — Argon2id, SHA-256 tokens e magic bytes avatar *(2026-05-27, `sec/hardening` + `sec/token-hashing`)*

Argon2id RFC 9106 level 1 (`m=65536, t=3, p=4`); upgrade-on-login automático de hashes werkzeug (SEC-04b, 2026-05-28, removeu o fallback werkzeug após todos os utilizadores migrarem); `hashlib.sha256(token.encode()).hexdigest()` (64 hex chars) guardado na BD para tokens de reset/verificação, token em claro vai apenas no email/URL, CSRF exempt para rotas de registo/forgot-password/reset-password; `_check_avatar_magic()` valida magic bytes reais no upload de avatar: JPEG `\xff\xd8\xff`, PNG `\x89PNG`, WebP `RIFF...WEBP`, GIF `GIF8`/`GIF9` — SVG e tipos não listados rejeitados com 400.

---

#### ✅ feat/security — SEC-01..03, AUTH-06..08, SEC-08 *(2026-05-12, `feat/security`)*

CORS estrito (`allow_origins` sem `*`, `https://` obrigatório, `allow_headers` restringido, `max_age=86400`, `FRONTEND_URL` incluída nas origins); HTTPS obrigatório (Render força HTTPS no reverse proxy, `CHICHORRO_SESSION_SECURE=1`, HSTS via middleware, fail-fast `FRONTEND_URL`/`BACKEND_URL`); headers de segurança (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`) e CSRF via `starlette-csrf`; cookies HTTPONLY/SECURE/SameSite=Lax renomeado para `chichorro_session`; `AUTH-07` rate limiting via slowapi + Upstash Redis EU; `AUTH-08` `request.session.clear()` antes de login (mitiga session fixation); `legacyLogin.ts` removido.

---

#### ✅ AUTH-11 + AUTH-12 + DB-01 + TEST-01 — Produção: modal sessão, merge, Neon, e2e *(2026-05-08, `feat/access-log`)*

Modal de sessão expirada validado em produção (cookie apagado manualmente com cookies HTTPS); merge `feat/access-log` → `3.1-dev` integrando AUTH-01…08/11, DB-01, TEST-01; PostgreSQL Neon configurado no Render via `DATABASE_URL` (substituiu SQLite); fluxo e2e completo validado manualmente: registo → email Resend → verificação → login → reset password.

---

#### ✅ SEC-10 — Fail-fast secrets em produção *(2026-05-21, `audit-fix`)*

`CHICHORRO_SECRET_KEY=dev-change-me` rejeita arranque; `DATABASE_URL`, `CHICHORRO_CORS_ORIGINS`, `UPSTASH_REDIS_URL`, `RESEND_API_KEY`, `MAIL_DEFAULT_SENDER` obrigatórias; 8/8 testes de import aprovados (C-04).

---

#### ✅ AUTH-13 — Hardening de segurança da sessão *(2026-05-22, `3.1-dev`)*

`max_age` configurável via env var (anteriormente `None` — sessão nunca expirava); `CHICHORRO_SESSION_SECURE` com default seguro em produção; `starlette-csrf` integrado como middleware.

---

### Prioridade Média

#### ✅ UI-13 — Painel admin de pedidos de suporte *(2026-07-02, `feat/ui-13-admin-support`)* [FIR-54]

Página `/app/admin/support` (só admins). Tabela ordenável por qualquer coluna (ID, nome, email, assunto, status, data), badge colorido por status, dropdown inline com PATCH optimista (open/pending/working/closed). Backend: `GET /admin/support` e `PATCH /admin/support/{id}` em `admin.py`, schema `SupportStatusUpdate`. `lib/api.ts` ganhou `patchJson` (generalizado a partir de `postJson`). 358 testes pytest, typecheck e build sem erros.

---

#### ✅ UI-11 — Formulário de suporte técnico na LoginPage *(2026-06-30, `feat/ui-11-support-modal`)* [FIR-52]

FAB "Suporte" na LoginPage abre modal público fora do `<form>` de login. Campos: nome, email, telemóvel PT (validação JS + Pydantic), assunto (select), mensagem. Backend: tabela `support_requests` (migration 0005), status ENUM open/pending/working/closed (migration 0006), `POST /support/request` (rate limit 3/h), emails Resend HTML com tabela colorida e ID no assunto. `postJson` via `VITE_API_BASE_URL` para arquitetura split-origin (Cloudflare Pages + Render). 10/10 testes pytest.

---

#### ✅ INFRA-08 — Monitorização self-hosted *(2026-06-18, `feat/infra08-monitoring`)*

3 scripts bash em `infra/monitoring/` com cron e alertas por email (Resend API): `health_check.sh` (a cada 5 min), `disk_check.sh` (horário), `backup_check.sh` (02:30 UTC). Configuração em `/etc/chichorro-monitoring.env` na VM (chmod 600, nunca commitado). Validado na VM staging.

---

#### ✅ INFRA-10 — pgAdmin removido, Adminer em staging *(2026-06-17, `3.1-dev`)*

Após avaliação, pgAdmin removido (serviço, volume, nginx, GUIDE_PGADMIN.md); Adminer mantido e movido para porta 5050; `servers.json` e pgpass removidos; INFRA-10.md fechado com decisão registada.

---

#### ✅ AUTH-09d — Otimização do avatar: WebP 128 px, 100 KB *(2026-06-12, `3.1-dev`)*

WebP 128 px q0.80 com limite 100 KB; `scripts/migrate_avatars_to_webp.py` para conversão de avatares existentes (Pillow); redução estimada ~80% no armazenamento por utilizador.

---

#### ✅ AUTH-10 — Sistema de roles/permissões *(2026-05-26, `auth/roles`)*

Coluna `role TEXT NOT NULL DEFAULT 'engineer'`; `require_admin` em `deps.py` (401/403); login env var → `role=admin`, login DB → role da BD; `/admin/users` e `/admin/log` protegidos; sidebar grupo ADMIN condicional; `AdminUsersPage` e `AdminLogPage`.

---

#### ✅ DB-05 — Least privilege DB user *(2026-05-24, `audit-fix`)*

`chichorro_runtime` com apenas DML; `alembic/env.py` lê `DATABASE_URL_MIGRATIONS` (superuser para migrations).

---

#### ✅ DB-04 — Migrations Alembic *(2026-05-22, `audit-fix`)*

Alembic configurado com psycopg2 puro (sem SQLAlchemy ORM); `init_db()` guardado para dev SQLite; migration `0001_initial_schema.py` cobre schema completo; Release Command Render: `cd app/backend && alembic upgrade head`.

---

#### ✅ DB-03 — Estratégia de backups *(2026-05-22, `audit-fix`)*

`scripts/backup_db.py` exporta JSON com descoberta dinâmica de tabelas; `backup-db.yml` cron a cada 3 dias com artifact 90 dias; `scripts/restore_db.py` com `--confirm` e rollback automático.

---

#### ✅ INFRA-05 — Cache-Control no edge e backend *(2026-05-22, `audit-fix`)*

`Cache-Control: no-store` no middleware `add_security_headers`; `_headers` Cloudflare Pages com `no-store` em `/*` e `public, max-age=31536000, immutable` em `/assets/*`; assets Vite fingerprintados cacheados 1 ano (M-02).

---

#### ✅ INFRA-01/M-04 — X-Request-ID middleware e alerta de backup *(2026-05-24, `audit-fix`)*

`X-Request-ID` UUID por pedido com tag Sentry; email de alerta via Resend em caso de falha do backup.

---

#### ✅ Ciclo audit-fix (16 planos) *(2026-05-22, `audit-fix`)*

16 planos concluídos: Alembic, backups automáticos, CSP, CORS estrito, CSRF, fail-fast Redis e secrets, `/health/db`.

---

#### ✅ AUTH-09 (a/b/c) + UI-06 — Editar Perfil e SettingsPage *(2026-05-13, `3.1-dev`)*

5 rotas de perfil (`/auth/profile/username`, `/auth/profile/email` c/ re-verificação e re-login, `/auth/profile/password`, `/auth/profile/delete`, `/auth/profile/avatar`; rate limit 5/hora; migração DB colunas `new_email`, `new_email_token`, `new_email_token_expires_at`); ProfilePage card compacto `max-w-sm` com avatar (header gradient `brand-900→brand-800`, initials fallback, upload via canvas resize 256×256 JPEG 0.85, pencil overlay), 4 rows expansíveis inline (nome de utilizador, e-mail, palavra-passe, apagar conta) com ícones MDI e chevron animado, modal de eliminação com texto de confirmação; SettingsPage com `prefs.ts` store em localStorage (`theme`, `warnOnExit`, `decimalPlaces`), `usePrefs()` hook reactivo, 3 secções (Aparência, Sessão, Resultados), dark mode via `darkMode: "class"` no Tailwind.

---

#### ✅ BACK-01 + BACK-02 + BACK-04 — FastAPI, logging e deploy *(2026-05-12~15, `feat/flask-to-fastapi`)*

Migração completa Flask → FastAPI com estrutura modular (`routers/`, `schemas/`, `services/`, Starlette sessions, dependências injetadas via `Depends`, 11/11 testes PASS); logging de acessos com user-agent, IPs, failed logins e request IDs (tabela `access_log`, rota `/admin/log`); deploy no Render com gunicorn + uvicorn workers, `wsgi.py` com `--proxy-headers`, Supabase.

---

### Prioridade Baixa

#### ✅ UI-12 — Modal "Sobre" na LoginPage *(2026-07-08, `feat/ui-12-about-modal`)* [FIR-53]

FAB "Sobre" quadrado (`h-16 w-16`, ícone `mdiInformationOutline`) ao lado do FAB "Suporte"
(UI-11) no canto inferior direito da LoginPage — "Suporte" à esquerda, "Sobre" à direita.
`AboutModal.tsx` segue o padrão do `SupportModal.tsx` (`role="dialog"`, componente `Button`);
conteúdo: nome oficial, versão, descrição legal do modelo CHICHORRO (DL 220/2008 + DL 95/2019)
e contacto `mailto:`. 1ª iteração (link de texto dentro do card) substituída após feedback
de UX: pouco visível e não devia estar integrada na box de login. Typecheck e build sem erros.

---

#### ✅ SEC-12 — Proteção pgAdmin + Adminer (Basic Auth Nginx) *(2026-06-16, `feat/sec11-sec12-secrets-pgadmin`)*

Nginx expõe portas 5050/5051 com `auth_basic` + `/etc/nginx/.htpasswd` (gerado na VM, nunca commitado); pgAdmin e Adminer passaram de `ports:` para `expose:` — tráfego obrigatoriamente via Nginx; runbook SEC-12 em `DEPLOY_PROXMOX_DEBIAN.md`; nota de Basic Auth em `GUIDE_PGADMIN.md`.

---

#### ✅ SEC-11 — Gestão de secrets (política documental) *(2026-06-16, `feat/sec11-sec12-secrets-pgadmin`)*

`docs/deploy/SECRETS_POLICY.md` com inventário completo de secrets, onde não devem existir, procedimentos de rotação por tipo (Render, Supabase, SSH, htpasswd) e recomendação de backup no Bitwarden; `ENV_VARS.md` atualizado com secção staging VM e referência à policy.

---

#### ✅ AI-02 — Setup Obsidian vault *(2026-06-05, `feat/obsidian-vault`)* [FIR-35]

50 notas Obsidian geradas por `build_vault.py`; 27 subfatores × 8 fontes preenchidos por `map_sources.py` (incl. RT-SCIE 135/2020 e Backend/Frontend); merge em `3.1-dev`.

---

#### ✅ AI-01 — Setup Graphify *(2026-06-01, `3.1-dev`)* [FIR-34]

Graphify instalado; 3 grafos: backend (367 nós), frontend (346 nós), cross-stack (740 nós · 1657 arestas · 44 comunidades); CLAUDE.md com regras de refresh.

---

#### ✅ test: parity checker + 338 testes Literal *(2026-05-28, `3.1-dev`)*

`check_option_parity.py` verifica paridade frontend↔backend; `test_valid_options.py` com 338 testes parametrizados; detetou 2 bugs reais.

---

#### ✅ fix(schemas): POI_CC_Idade sem espaços + DPI_OGS_Aplica phantom *(2026-05-28, `3.1-dev`)*

`POI_CC_Idade` intervalos sem espaços; `DPI_OGS_Aplica "Nao Existe"` removido — phantom value ausente no modelo.

---

#### ✅ fix: POI campos condicionais + sync CTI↔ATIV + CTI desbloqueado *(2026-05-28, `3.1-dev`)*

`POI_IA_TipoInst2`/`POI_ATIV_TipoEdif2` tornados `Optional`; sync bidirecional CTI↔ATIV via module inputs.

---

#### ✅ fix: session remount no AppLayout *(2026-05-28, `3.1-dev`)*

`key={sessionKey}` no `<Outlet>` força remount ao importar/limpar sessão sem reload manual.

---

#### ✅ DOCS-02 — Uniformização dos headers dos subplans *(2026-05-28, `3.1-dev`)*

58 subplans uniformizados (Estado → Data → Branch); `DESIGN.md` duplicado removido; SEC-09 ❌ duplicado e INFRA-04 ❌ incorreto corrigidos.

---

#### ✅ BACK-05d + BACK-06 — Pydantic Literal types e JSON error handler *(2026-05-27, `back/validation`)*

Pydantic `Literal` em todos os schemas (DPI/ESCI/CTI/POI: 49+23+23+13 campos enum reescritos); payloads inválidos retornam 422 automaticamente; `unhandled_exception_handler` em `main.py` retorna sempre JSON `{"error":"INTERNAL_ERROR","request_id":...}` com HTTP 500 (erros 5xx estruturados; `HTTPException` continua a ser re-lançada pelo FastAPI).

---

#### ✅ TEST-02 + INFRA-02 — pytest e GitHub Actions CI/CD *(2026-05-27, `test/automated-tests` + `infra/ci-cd`)*

12/12 testes pytest (health, Literal 422 DPI/ESCI/CTI/POI, cálculo válido 200, auth login sem body 422, credenciais inválidas 401; fixture `client` com override de auth e CSRF automático); workflows `test.yml` (Python 3.12, pytest --cov, path `app/backend/**`) + `build.yml` (Node 20, npm ci + build, path `app/frontend/**`), sem Render Deploy Hook por agora.

---

#### ✅ B-01 + BACK-07 — Consolidação docs de deploy e naming de rotas API *(2026-05-24, `audit-fix`)*

`ENV_VARS.md` e `DEPLOY.md` reescritos; `DEPLOY_CLOUD_VPS.md` apagado; aliases legacy removidos; decisão documentada de manter paths atuais (`/POI/*`, `/CTI/*`, etc. — subdomain `api.*` fornece contexto, dead code confirmado por grep); Nginx VPS prefix-strip config documentada (B-02); audit-fix 16/16 completo.

---

#### ✅ DOCS-01 + INFRA-01 — VitePress e Sentry+UptimeRobot *(2026-05-19~20, `3.1-dev`)*

VitePress ^1.6.4 em produção em `docs.chichorrofireriskapp.joaopmteixeira.net` (Cloudflare Pages via `fireriskapp-docs`, repo público, sync automático via GitHub Actions); Sentry frontend+backend com Session Replay em erros; UptimeRobot a monitorizar `/health` a cada 5 min.

---

#### ✅ UI-07 — Dark mode *(2026-05-18, `3.1-dev`)*

Tema escuro em todas as páginas: sidebar, cards POI/DPI/ESCI, ProfilePage, SettingsPage, RiPage, CtiPage, InterventionsPage e páginas de autenticação.

---

#### ✅ AUTH-11 — Modal de sessão expirada — validação produção *(2026-05-08, `feat/access-log`)*

Modal aparece corretamente ao apagar cookie de sessão manualmente em produção com cookies HTTPS.

---

#### ✅ SEC-06 — Política de logs — sem PII em produção *(2026-05-22, `audit-fix`)*

`_TokenPathFilter` no `uvicorn.access` logger substitui tokens em URLs `/auth/verify/*` por `[REDACTED]`; guard `env != "production"` nos `print()` de `email.py`; `send_default_pii=False` no Sentry (A-05).

---

## Notas

### JWT — Notas Importantes

O projeto atual NÃO usa JWT. Isto NÃO é um problema.

A arquitetura atual (React + FastAPI + sessões Starlette) é totalmente válida.

JWT NÃO é automaticamente mais moderno, mais seguro ou melhor. Sessões Starlette/FastAPI podem até ser mais seguras e simples neste tipo de arquitetura.

---

## Arquitetura Atual Recomendada

```text
React
+
FastAPI + Starlette Sessions
+
PostgreSQL Supabase
```

E focar em: hardening, organização, deployment, testes, monitorização.
