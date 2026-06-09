# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-06-08 (DB-06 e INFRA-03 → Alta; AI-03 → Média; Concluídos reformulados)

---

## Prefixos de ID

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
- **`MODEL`** — Modelo CHICHORRO (backlog pós-3.1)
- **`AI`** — AI tooling e knowledge graph (Graphify, Obsidian, RAG)
- **`B`** — Tarefas de manutenção/organização

---

## Concluídos Recentemente (mais recente → mais antigo)

### ✅ AI-02 — Setup Obsidian vault `Prioridade Baixa` *(2026-06-05, `feat/obsidian-vault`)* [FIR-35]

50 notas Obsidian; 27 subfatores × 8 fontes (incl. RT-SCIE 135/2020 e Backend/Frontend); merge em `3.1-dev`.

---

### ✅ AI-01 — Setup Graphify `Prioridade Baixa` *(2026-06-01, `3.1-dev`)* [FIR-34]

Graphify instalado; 3 grafos: backend (367 nós), frontend (346 nós), cross-stack (740 nós · 1657 arestas · 44 comunidades); CLAUDE.md com regras de refresh.

---

### ✅ test: parity checker + 338 testes Literal `Prioridade Baixa` *(2026-05-28, `3.1-dev`)*

`check_option_parity.py` verifica paridade frontend↔backend; `test_valid_options.py` com 338 testes parametrizados; detetou 2 bugs reais.

---

### ✅ fix(schemas): POI_CC_Idade sem espaços + DPI_OGS_Aplica phantom *(2026-05-28, `3.1-dev`)*

`POI_CC_Idade` intervalos sem espaços; `DPI_OGS_Aplica "Nao Existe"` removido — phantom value ausente no modelo.

---

### ✅ fix: POI campos condicionais + sync CTI↔ATIV + CTI desbloqueado *(2026-05-28, `3.1-dev`)*

`POI_IA_TipoInst2`/`POI_ATIV_TipoEdif2` tornados `Optional`; sync bidirecional CTI↔ATIV via module inputs.

---

### ✅ fix: session remount no AppLayout *(2026-05-28, `3.1-dev`)*

`key={sessionKey}` no `<Outlet>` força remount ao importar/limpar sessão sem reload manual.

---

### ✅ SEC-04b — Remoção do fallback werkzeug `Prioridade Alta` *(2026-05-28, `3.1-dev`)*

Werkzeug removido de `auth.py` e `requirements.txt` após confirmação que todos os hashes são `$argon2id`.

---

### ✅ DOCS-02 — Uniformização dos headers dos subplans `Prioridade Baixa` *(2026-05-28, `3.1-dev`)*

58 subplans uniformizados (Estado → Data → Branch); `DESIGN.md` duplicado removido.

---

### ✅ BACK-05d + BACK-06 — Pydantic Literal types e JSON error handler `Prioridade Média` *(2026-05-27, `back/validation`)*

Pydantic `Literal` em todos os schemas (DPI/ESCI/CTI/POI); handler 500 retorna sempre JSON `{"error":"INTERNAL_ERROR","request_id":...}`.

---

### ✅ SEC-04 + SEC-05 + SEC-07 — Argon2id, SHA-256 tokens e magic bytes avatar `Prioridade Média` *(2026-05-27, `sec/hardening` + `sec/token-hashing`)*

Argon2id RFC 9106 level 1; tokens SHA-256 na BD; magic bytes validados no upload de avatar.

---

### ✅ TEST-02 + INFRA-02 — pytest e GitHub Actions CI/CD `Prioridade Baixa` *(2026-05-27, `test/automated-tests` + `infra/ci-cd`)*

12/12 testes pytest; workflows `test.yml` + `build.yml` com path filters.

---

### ✅ AUTH-10 — Sistema de roles/permissões `Prioridade Média` *(2026-05-26, `auth/roles`)*

Coluna `role`, `require_admin` em `deps.py`, rotas `/admin/*` protegidas, sidebar ADMIN condicional.

---

### ✅ DB-05 — Least privilege DB user `Prioridade Média` *(2026-05-24, `audit-fix`)*

`chichorro_runtime` com apenas DML; `DATABASE_URL_MIGRATIONS` para Alembic superuser.

---

### ✅ B-01 + BACK-07 — Consolidação docs de deploy e naming de rotas API `Prioridade Baixa` *(2026-05-24, `audit-fix`)*

`ENV_VARS.md` e `DEPLOY.md` reescritos; aliases legacy removidos; audit-fix 16/16 completo.

---

### ✅ INFRA-01/M-04 — X-Request-ID middleware e alerta de backup `Prioridade Média` *(2026-05-24, `audit-fix`)*

`X-Request-ID` UUID por pedido com tag Sentry; email de alerta via Resend em caso de falha do backup.

---

### ✅ Ciclo audit-fix (16 planos) `Prioridades Média/Alta` *(2026-05-22, `audit-fix`)*

16 planos concluídos: Alembic, backups automáticos, CSP, CORS estrito, CSRF, fail-fast Redis e secrets, `/health/db`.

---

### ✅ DOCS-01 + INFRA-01 — VitePress e Sentry+UptimeRobot `Prioridade Baixa/Média` *(2026-05-19~20, `3.1-dev`)*

VitePress em `docs.chichorrofireriskapp.joaopmteixeira.net`; Sentry frontend+backend; UptimeRobot ativo.

---

### ✅ UI-07 — Dark mode `Prioridade Baixa` *(2026-05-18, `3.1-dev`)*

Tema escuro em todas as páginas: sidebar, cards, auth, RiPage, CtiPage, InterventionsPage.

---

### ✅ AUTH-09 (a/b/c) + UI-06 — Editar Perfil e SettingsPage `Prioridade Média` *(2026-05-13, `3.1-dev`)*

5 rotas de perfil; ProfilePage card compacto com avatar; SettingsPage (tema, warnOnExit, casas decimais).

---

### ✅ BACK-01 + BACK-02 + BACK-04 — FastAPI, logging e deploy `Prioridade Média` *(2026-05-12~15, `feat/flask-to-fastapi`)*

Migração completa Flask → FastAPI; logging de acessos; deploy no Render com Supabase.

---

### ✅ feat/security — SEC-01..03, AUTH-06..08, SEC-08 `Prioridade Alta` *(2026-05-12, `feat/security`)*

CORS estrito, HTTPS obrigatório, headers de segurança, cookies hardened, rate limiting, `legacyLogin.ts` removido.

---

### ✅ AUTH-11 + AUTH-12 + DB-01 + TEST-01 — Produção: modal sessão, merge, Neon, e2e `Prioridade Alta` *(2026-05-08, `feat/access-log`)*

Modal sessão expirada; merge `feat/access-log`; PostgreSQL Neon; e2e completo aprovado em produção.

---

## Prioridade Alta

### ❌ DB-06 — Migrar camada de dados para SQLAlchemy ORM

Substituir `_PGConn` (psycopg2 manual) por SQLAlchemy 2.x; desbloqueia autogenerate de migrations, connection pooling nativo e type safety. Pré-requisito para INFRA-03 e deploy VPS. Ver [DB-06_UNDONE.md](plans/subplans/DB-06_UNDONE.md).

---

### ❌ INFRA-03 — Dockerfile + Compose

Containerização para deploy reproduzível em VPS/Proxmox. Depende de DB-06 (SQLAlchemy) para pooling correto em ambiente containerizado.

---

### ✅ AUTH-06 — Hardening de cookies de sessão (concluído 2026-05-22, branch `feat/security` + `audit-fix`)

Cookies com HTTPONLY, SECURE (`CHICHORRO_SESSION_SECURE=1`) e SameSite=Lax; cookie renomeado para `chichorro_session` (anti-fingerprinting); fase C-02 corrigiu interpretação de headers de proxy Render com `--proxy-headers --forwarded-allow-ips='*'`.

---

### ✅ AUTH-07 — Rate limiting nos endpoints /auth/* (concluído 2026-05-22, branch `feat/security` + `audit-fix`)

slowapi com Upstash Redis EU (free tier) para limites globais entre workers; fail-fast `_check_redis_startup()` no lifespan rejeita arranque se Redis inválido em produção; contadores visíveis no Data Browser Upstash.

---

### ✅ AUTH-08 — Regeneração de sessão após login (concluído 2026-05-08, branch `feat/security`)

`request.session.clear()` antes de definir `chichorro_auth=1` em todos os pontos de login — mitiga session fixation (OWASP ASVS V3.3).

---

### ✅ AUTH-12 — Merge feat/access-log → 3.1-dev (concluído 2026-05-08, branch `feat/access-log`)

Integração do sistema de autenticação completo (AUTH-01…AUTH-08, AUTH-11, DB-01, TEST-01) no branch principal após validação e2e em produção.

---

### ✅ DB-01 — Neon PostgreSQL em produção (concluído 2026-05-08, branch `feat/access-log`)

PostgreSQL Neon configurado no Render via `DATABASE_URL`; substituiu SQLite que só funciona em desenvolvimento.

---

### ✅ TEST-01 — Teste e2e em produção (concluído 2026-05-08, branch `feat/access-log`)

Fluxo completo validado manualmente: registo → email Resend → verificação → login → reset password com cookies HTTPS no Render.

---

### ✅ SEC-01 — CORS estrito em produção (concluído 2026-05-22, branch `feat/security` + `audit-fix`)

`allow_origins` sem `*`; `https://` obrigatório; `allow_headers` restringido; `max_age=86400`; `FRONTEND_URL` incluída nas origins; fallback dev explícito (A-01).

---

### ✅ SEC-02 — HTTPS obrigatório em produção (concluído 2026-05-12, branch `feat/security`)

Render força HTTPS no reverse proxy; `CHICHORRO_SESSION_SECURE=1` ativo; HSTS via middleware; fail-fast `FRONTEND_URL`/`BACKEND_URL` obrigatórias com `https://` em produção; `app_base_url` overridden por `FRONTEND_URL` (C-01).

---

### ✅ SEC-03 — Headers de segurança e CSRF (concluído 2026-05-12, branch `feat/security`)

`X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy: strict-origin-when-cross-origin`; `starlette-csrf` middleware para proteção CSRF.

---

### ✅ SEC-10 — Fail-fast secrets em produção (concluído 2026-05-21, branch `audit-fix`)

`CHICHORRO_SECRET_KEY=dev-change-me` rejeita arranque; `DATABASE_URL`, `CHICHORRO_CORS_ORIGINS`, `UPSTASH_REDIS_URL`, `RESEND_API_KEY`, `MAIL_DEFAULT_SENDER` obrigatórias; 8/8 testes de import aprovados (C-04).

---

## Prioridade Média

### ❌ UI-02 — Página de Documentação

Criar página de DOCS na app com documentação e manuais de utilização.

---

### ❌ UI-03 — Página de Ajuda

Criar página HELP integrada na app com respostas rápidas às dúvidas mais comuns.

---

### ❌ UI-04 — FAQs — Perguntas Frequentes

Criar página de perguntas frequentes integrada na app.

---

### ❌ UI-05 — Sistema de Reporte de Bugs

Formulário de reporte de bugs na app; canal de destino a definir (email, GitHub Issues ou ClickUp).

---

### ❌ UI-08 — Ícones de informação nos subfatores

Ícone ℹ️ em cada subfator POI/CTI/DPI/ESCI; painel com descrição detalhada do subfator (o que mede, valores esperados, como interpretar), tabela de valores e referência RT-SCIE. Torna a app autónoma para utilizadores sem formação prévia no modelo CHICHORRO.

---

### ❌ AUTH-09d — Otimização do avatar: WebP, 128 px, limite 100 KB

Avatar atualmente guardado como base64 JPEG 256×256 q0.85 (até 700 KB/utilizador). A 50k utilizadores, o tamanho acumulado pode exceder o limite free do Supabase. Reduzir para WebP 128×128 q0.80 e limite de 100 KB — redução estimada de ~80% no armazenamento.

Ver [AUTH-09d.md](plans/subplans/AUTH-09d.md).

---

### ❌ UI-09 — Badge de lápis persistente no avatar

O ícone de câmara no avatar é apenas visível no hover (`opacity-0 group-hover:opacity-100`) — invisível em mobile. Substituir por um badge circular persistente com `mdiPencil` no canto inferior-direito, sempre visível, seguindo o padrão Gmail/LinkedIn.

Ver [UI-09.md](plans/subplans/UI-09.md).

---

### ❌ UI-10 — Sidebar direita — resumo de sessão e subfatores

Painel lateral direito persistente, colapsável, com resumo da sessão atual: valores introduzidos nos subfatores (POI/CTI/DPI/ESCI), resultado RI calculado e estado dos campos em falta. Visível durante o preenchimento e o cálculo para referência rápida sem necessidade de navegar entre páginas.

---

### ❌ AI-03 — RAG — botão "Explicar" por subfator

pgvector + `routers/rag.py` + botão "Explicar" em cada subfator POI/CTI/DPI/ESCI. Permite ao utilizador obter uma explicação contextual do subfator com base nas dissertações e no RT-SCIE, sem sair da app. Implementar após AI-02a concluído.

---

### ✅ AUTH-10 — Sistema de roles/permissões (concluído 2026-05-26, branch `auth/roles`)

Coluna `role TEXT NOT NULL DEFAULT 'engineer'`; `require_admin` em `deps.py` (401/403); login env var → `role=admin`, login DB → role da BD; `/admin/users` e `/admin/log` protegidos; sidebar grupo ADMIN condicional; `AdminUsersPage` e `AdminLogPage`.

---

### ✅ AUTH-13 — Hardening de segurança da sessão (concluído 2026-05-22, branch `3.1-dev`)

`max_age` configurável via env var (anteriormente `None` — sessão nunca expirava); `CHICHORRO_SESSION_SECURE` com default seguro em produção; `starlette-csrf` integrado como middleware.

---

### ✅ AUTH-09 — Editar Perfil — backend (concluído 2026-05-13, branch `3.1-dev`)

5 rotas: `/auth/profile/username`, `/auth/profile/email` (c/ re-verificação e re-login), `/auth/profile/password`, `/auth/profile/delete`, `/auth/profile/avatar`; rate limit 5/hora; migração DB colunas `new_email`, `new_email_token`, `new_email_token_expires_at`.

---

### ✅ AUTH-09a — ProfilePage — card layout, accordion e ícones MDI (concluído 2026-05-13, branch `3.1-dev`)

Card compacto `max-w-sm`, header gradient `brand-900→brand-800`, avatar circular com initials fallback, menu accordion com ícones MDI e chevron animado; modal de eliminação com texto de confirmação.

---

### ✅ AUTH-09b — Avatar — upload, canvas resize e armazenamento (concluído 2026-05-13, branch `3.1-dev`)

Coluna `avatar TEXT` na BD; upload frontend com canvas resize 256×256 JPEG 0.85; rota FastAPI valida `data:image/`, limite 700 KB base64, rate limit 20/hora.

---

### ✅ AUTH-09c — ProfilePage redesign (card compacto) (concluído 2026-05-13, branch `3.1-dev`)

4 rows expansíveis inline (nome de utilizador, e-mail, palavra-passe, apagar conta); pencil overlay no avatar; sem "Zona de perigo" separada.

---

### ✅ UI-06 — SettingsPage (Definições) (concluído 2026-05-13, branch `3.1-dev`)

`prefs.ts` store em localStorage (`theme`, `warnOnExit`, `decimalPlaces`); `usePrefs()` hook reactivo; SettingsPage com 3 secções (Aparência, Sessão, Resultados); dark mode via `darkMode: "class"` no Tailwind.

---

### ✅ BACK-05 + BACK-05d — Pydantic Literal types nos schemas de cálculo (concluído 2026-05-27, branch `back/validation`)

49+23+23+13 campos enum em `schemas/dpi.py`, `schemas/esci.py`, `schemas/cti.py`, `schemas/poi.py` reescritos com `Literal[...]`; payloads inválidos retornam 422 automaticamente.

---

### ✅ BACK-06 — Error handler JSON normalizado (concluído 2026-05-27, branch `back/validation`)

`unhandled_exception_handler` em `main.py` retorna `{"error":"INTERNAL_ERROR","request_id":...}` com HTTP 500; `HTTPException` continua a ser re-lançada pelo FastAPI; erros 5xx produzem sempre JSON estruturado.

---

### ✅ SEC-04 — Argon2id password hashing (concluído 2026-05-27, branch `sec/hardening`)

`argon2-cffi` com RFC 9106 level 1 (`m=65536, t=3, p=4`); upgrade-on-login automático de hashes werkzeug; SEC-04b (2026-05-28) removeu o fallback werkzeug após todos os utilizadores migrarem.

---

### ✅ SEC-05 — SHA-256 dos tokens de reset/verificação (concluído 2026-05-27, branch `sec/token-hashing`)

`hashlib.sha256(token.encode()).hexdigest()` (64 hex chars) guardado na BD; token em claro vai apenas no email/URL; CSRF exempt para rotas de registo, forgot-password e reset-password.

---

### ✅ SEC-07 — Hardening do upload de avatar (concluído 2026-05-27, branch `sec/hardening`)

`_check_avatar_magic()` valida magic bytes reais: JPEG `\xff\xd8\xff`, PNG `\x89PNG`, WebP `RIFF...WEBP`, GIF `GIF8`/`GIF9`; SVG e tipos não listados rejeitados com 400.

---

### ✅ DB-04 — Migrations Alembic (concluído 2026-05-22, branch `audit-fix`)

Alembic configurado com psycopg2 puro (sem SQLAlchemy ORM); `init_db()` guardado para dev SQLite; migration `0001_initial_schema.py` cobre schema completo; Release Command Render: `cd app/backend && alembic upgrade head`.

---

### ✅ DB-05 — Least privilege DB user (concluído 2026-05-24, branch `audit-fix`)

`alembic/env.py` lê `DATABASE_URL_MIGRATIONS` (superuser para migrations); `DATABASE_URL` aponta para `chichorro_runtime` (apenas DML).

---

### ✅ INFRA-04 — Endpoint /health/db (concluído 2026-05-22, branch `audit-fix`)

`SELECT 1` real à BD; retorna `{"status":"ok","db":"ok"}` ou HTTP 503; HEAD suportado para UptimeRobot; CSRF isento.

---

### ✅ INFRA-01 — Monitorização (Sentry + UptimeRobot) (concluído 2026-05-19, branch `3.1-dev`)

Sentry no frontend e backend com Session Replay em erros; UptimeRobot a monitorizar `/health` a cada 5 min; M-04 (2026-05-24) adicionou `X-Request-ID` middleware e alerta email de falha de backup.

---

### ✅ INFRA-05 — Cache-Control no edge e backend (concluído 2026-05-22, branch `audit-fix`)

`Cache-Control: no-store` no middleware `add_security_headers`; `_headers` Cloudflare Pages com `no-store` em `/*` e `public, max-age=31536000, immutable` em `/assets/*`; assets Vite fingerprintados cacheados 1 ano (M-02).

---

### ✅ SEC-09 — CSP e Permissions-Policy (concluído 2026-05-22, branch `audit-fix`)

`Content-Security-Policy` e `Permissions-Policy` no middleware `add_security_headers`; CSP cobre Google Fonts e Sentry ingest, sem `'unsafe-inline'`; `app/frontend/public/_headers` para Cloudflare Pages com HSTS preload (M-01).

---

### ✅ BACK-01 — Migração Flask → FastAPI (concluído 2026-05-15, branch `feat/flask-to-fastapi`)

Migração completa para FastAPI com estrutura modular (`routers/`, `schemas/`, `services/`); 11/11 testes PASS; Starlette sessions; dependências injetadas via `Depends`.

---

### ✅ BACK-02 — Melhorar logging (concluído 2026-05-12, branch `3.1-dev`)

Logging de acessos com user-agent, IPs, failed logins e request IDs; tabela `access_log` na BD; rota `/admin/log` para visualização.

---

### ✅ BACK-04 — Deploy FastAPI no Render (concluído 2026-05-15, branch `feat/flask-to-fastapi`)

Deploy com gunicorn + uvicorn workers no Render; `wsgi.py` com `--proxy-headers`; variáveis de ambiente documentadas em `deploy/env.production.example`.

---

### ✅ DB-03 — Estratégia de backups (concluído 2026-05-22, branch `audit-fix`)

`scripts/backup_db.py` exporta JSON com descoberta dinâmica de tabelas; `backup-db.yml` cron a cada 3 dias com artifact 90 dias; `scripts/restore_db.py` com `--confirm` e rollback automático.

---

### ✅ SEC-08 — Remover legacyLogin.ts e limpar .env (concluído 2026-05-22, branch `audit-fix`)

`legacyLogin.ts` eliminado (código morto, nunca importado); `VITE_LOGIN_USER_1`/`VITE_LOGIN_PASS_1` removidos do `.env` local; build TypeScript 0 erros (M-05).

---

## Prioridade Baixa

### ✅ AI-02 — Setup Obsidian vault (concluído 2026-06-05, branch `feat/obsidian-vault`) [FIR-35]

50 notas geradas por `build_vault.py`; 27 subfatores × 8 fontes preenchidos por `map_sources.py` (incl. RT-SCIE 135/2020 e Backend/Frontend).

---

### ✅ AI-01 — Setup Graphify (concluído 2026-06-01, branch `3.1-dev`) [FIR-34]

Graphify instalado; CLAUDE.md com regras de refresh; 3 grafos: backend (367 nós), frontend (346 nós), cross-stack (740 nós · 1657 arestas · 44 comunidades).

---

### ❌ AI-02a — Curation manual do vault Obsidian

Trabalho manual residual do [AI-02](plans/subplans/AI-02.md): (1) preencher `## Definicao` nas 27 notas de subfator; (2) validar entradas "verificar" em `## Onde e mencionado` (confirmar Sim/Não e correr `map_sources.py` para limpar); (3) abrir vault no Obsidian e verificar Graph View e cores por tipo de nó.

Ver [AI-02a.md](plans/subplans/AI-02a.md).

---

### ✅ TEST-02 — Testes automatizados com pytest (concluído 2026-05-27, branch `test/automated-tests`)

12/12 testes: health, Literal 422 (DPI/ESCI/CTI/POI), cálculo válido 200, auth login sem body 422, credenciais inválidas 401. Fixture `client` com override de auth e CSRF automático.

---

### ✅ INFRA-02 — Pipeline CI/CD GitHub Actions (concluído 2026-05-27, branch `infra/ci-cd`)

`test.yml` (Python 3.12, pytest --cov, path `app/backend/**`) + `build.yml` (Node 20, npm ci + build, path `app/frontend/**`). Sem Render Deploy Hook por agora (deploy manual).

---

### ✅ DOCS-02 — Uniformização dos headers dos subplans (concluído 2026-05-28, branch `3.1-dev`)

58 ficheiros em `docs/plans/subplans/` com formato uniforme (Estado → Data de conclusão → Branch); `DESIGN.md` duplicado removido; SEC-09 ❌ duplicado e INFRA-04 ❌ incorreto corrigidos.

---

### ✅ SEC-06 — Política de logs — sem PII em produção (concluído 2026-05-22, branch `audit-fix`)

`_TokenPathFilter` no `uvicorn.access` logger substitui tokens em URLs `/auth/verify/*` por `[REDACTED]`; guard `env != "production"` nos `print()` de `email.py`; `send_default_pii=False` no Sentry (A-05).

---

### ✅ UI-07 — Dark mode (concluído 2026-05-18, branch `3.1-dev`)

Tema escuro cobrindo todas as páginas: sidebar, cards POI/DPI/ESCI, ProfilePage, SettingsPage, RiPage, CtiPage, InterventionsPage e páginas de autenticação.

---

### ✅ DOCS-01 — Migração para VitePress (concluído 2026-05-20, branch `3.1-dev`)

VitePress ^1.6.4 em produção em `docs.chichorrofireriskapp.joaopmteixeira.net`; Cloudflare Pages via `fireriskapp-docs` (repo público); sync automático via GitHub Actions.

---

### ✅ AUTH-11 — Modal de sessão expirada — validação produção (concluído 2026-05-08, branch `feat/access-log`)

Modal aparece corretamente ao apagar cookie de sessão manualmente em produção com cookies HTTPS.

---

### ✅ B-01 — Consolidação docs de deploy (concluído 2026-05-24, branch `audit-fix`)

`ENV_VARS.md` reescrito com todas as variáveis atuais; `DEPLOY.md` corrigido; `DEPLOY_CLOUD_VPS.md` apagado; audit-fix 16/16 completo.

---

### ✅ BACK-07 — Naming de rotas API (concluído 2026-05-24, branch `audit-fix`)

Decisão documentada: manter paths atuais (`/POI/*`, `/CTI/*`, etc.) — subdomain `api.*` fornece contexto; aliases legacy removidos (dead code confirmado por grep); Nginx VPS prefix-strip config documentada (B-02).

---

## Futuro

### ❌ FEAT-01 — Gráfico de Impacto de Intervenções

Bar chart horizontal (tornado chart) com impacto individual de cada intervenção. Backend: `POST /RI/interv/impact` (~34 cálculos de RI por chamada). Frontend: Recharts (já disponível no projeto).

---

### ❌ FEAT-02 — Guardar Edifício

Após cálculo completo, guardar avaliação com nome, morada, código postal, Distrito/Concelho/Freguesia (dropdowns em cascata), latitude/longitude + pin no mapa. Ver [FEAT-02.md](plans/subplans/FEAT-02.md).

---

### ❌ FEAT-03 — Chatbot AI

Assistente de IA para ajudar utilizadores a compreender o CHICHORRO e usar a aplicação (via Claude API ou similar).

---

### ❌ FEAT-04 — Geração de relatório em PDF

Exportar resultados RI, CTI e subfatores (POI/DPI/ESCI) para ficheiro PDF imprimível e partilhável após cálculo completo.

---

### ❌ MODEL-01 — Método simplificado baseado no CHICHORRO 2.0

Proposta de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1.

---

### ❌ MODEL-02 — Alterar ordem do Cenário 4

CI → VVE → VHE alternativo.

---

### ❌ MODEL-03 — Afinação de custos €/m² via "PRONIC" ou similar com atualização automática de base de dados de custos

---

### ❌ MODEL-04 — Intervenções adicionais

Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa.

---

### ❌ MODEL-05 — Georreferenciação e base de dados de edifícios

---

### ❌ MODEL-06 — Tratamento de edifícios devolutos

---

### ❌ MODEL-07 — Integração com Firecheck 2.0

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
