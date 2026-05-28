# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-05-28 (SEC-04b werkzeug removido; DOCS-02 subplans uniformizados)

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
- **`B`** — Tarefas de manutenção/organização

---

## Concluídos Recentemente (mais recente → mais antigo)

### ✅ fix: POI campos condicionais + sync CTI↔ATIV + CTI desbloqueado *(2026-05-28, `3.1-dev`)*

`POI_IA_TipoInst2` e `POI_ATIV_TipoEdif2` tornados `Optional` no backend; payload filtrado por `opts.length > 0` (fix correto após tentativa com visibleWhen); CTI TipoEdif desbloqueado; sync bidirecional CTI↔ATIV via module inputs. Resolve HTTP 422 em POI IA e POI ATIV.

---

### ✅ fix: session remount no AppLayout *(2026-05-28, `3.1-dev`)*

`key={sessionKey}` no `<Outlet>` força remount ao importar/limpar sessão — páginas reflectem novo estado imediatamente sem reload manual.

---

### ✅ SEC-04b — Remoção do fallback werkzeug `Prioridade Alta` *(2026-05-28, `3.1-dev`)*

Após confirmação que ambos os utilizadores têm hashes `$argon2id`, werkzeug removido de `auth.py` e `requirements.txt`; `_verify_password` simplificada para apenas argon2id.

---

### ✅ DOCS-02 — Uniformização dos headers dos subplans `Prioridade Baixa` *(2026-05-28, `3.1-dev`)*

58 ficheiros em `docs/plans/subplans/` uniformizados com formato Estado → Data de conclusão → Branch; `DESIGN.md` duplicado removido; SEC-09 ❌ duplicado e INFRA-04 incorreto corrigidos.

---

### ✅ BACK-05d + BACK-06 — Pydantic Literal types e JSON error handler `Prioridade Média` *(2026-05-27, `back/validation`)*

Campos enum dos schemas DPI/ESCI/CTI/POI convertidos para `Literal[...]`; handler global 500 retorna sempre JSON `{"error":"INTERNAL_ERROR","request_id":...}`.

---

### ✅ SEC-04 + SEC-05 + SEC-07 — Argon2id, SHA-256 tokens e magic bytes avatar `Prioridade Média` *(2026-05-27, `sec/hardening` + `sec/token-hashing`)*

Passwords migradas de werkzeug para argon2id (RFC 9106 level 1); tokens guardados como SHA-256 na BD; upload de avatar valida magic bytes reais (JPEG/PNG/WebP/GIF).

---

### ✅ TEST-02 + INFRA-02 — pytest e GitHub Actions CI/CD `Prioridade Baixa` *(2026-05-27, `test/automated-tests` + `infra/ci-cd`)*

12/12 testes pytest com fixture CSRF automático; workflows `test.yml` e `build.yml` com path filters para backend e frontend separados.

---

### ✅ AUTH-10 — Sistema de roles/permissões `Prioridade Média` *(2026-05-26, `auth/roles`)*

Coluna `role` na BD; `require_admin` em `deps.py`; rotas `/admin/*` protegidas; sidebar condicional para grupo ADMIN.

---

### ✅ DB-05 — Least privilege DB user `Prioridade Média` *(2026-05-24, `audit-fix`)*

Alembic usa `DATABASE_URL_MIGRATIONS` (superuser); runtime usa `chichorro_runtime` com apenas DML. Ações manuais: criar role no Supabase, atualizar env vars Render e GitHub Secret.

---

### ✅ B-01 + BACK-07 — Consolidação docs de deploy e naming de rotas API `Prioridade Baixa` *(2026-05-24, `audit-fix`)*

`ENV_VARS.md` e `DEPLOY.md` reescritos; `DEPLOY_CLOUD_VPS.md` apagado; aliases legacy `/login`, `/logout`, `/me`, `/RI_interv` removidos; decisão de manter prefixos `/POI/*`, `/CTI/*` documentada.

---

### ✅ INFRA-01/M-04 — X-Request-ID middleware e alerta de backup `Prioridade Média` *(2026-05-24, `audit-fix`)*

`X-Request-ID` UUID por pedido com tag Sentry; `backup-db.yml` envia email de alerta via Resend em caso de falha.

---

### ✅ Ciclo audit-fix (16 planos) — DB-04, DB-03, SEC-09, INFRA-05, SEC-06, SEC-08, AUTH-07/A-02, SEC-10, SEC-01/A-01, AUTH-13, INFRA-04 `Prioridades Média/Alta` *(2026-05-22, `audit-fix`)*

Alembic; backups automáticos; CSP+Permissions-Policy; Cache-Control; logs sem PII; fail-fast Redis e secrets; CORS restrito; hardening sessão (max_age, CSRF); endpoint `/health/db`.

---

### ✅ DOCS-01 + INFRA-01 — VitePress e Sentry+UptimeRobot `Prioridade Baixa/Média` *(2026-05-19~20, `3.1-dev`)*

Documentação migrada para VitePress em `docs.chichorrofireriskapp.joaopmteixeira.net`; Sentry (frontend + backend) e UptimeRobot configurados.

---

### ✅ UI-07 — Dark mode `Prioridade Baixa` *(2026-05-18, `3.1-dev`)*

Tema escuro em todas as páginas: sidebar, cards, ProfilePage, SettingsPage, RiPage, CtiPage, InterventionsPage e páginas de autenticação.

---

### ✅ AUTH-09 (a/b/c) + UI-06 — Editar Perfil e SettingsPage `Prioridade Média` *(2026-05-13, `3.1-dev`)*

5 rotas de perfil (username, email c/ re-verificação, password, avatar, delete); ProfilePage card compacto com 4 rows expansíveis e avatar circular; SettingsPage com tema, warnOnExit e casas decimais em localStorage.

---

### ✅ BACK-01 + BACK-02 + BACK-04 — FastAPI, logging e deploy `Prioridade Média` *(2026-05-12~15, `feat/flask-to-fastapi`)*

Migração completa Flask → FastAPI com estrutura modular; logging de acessos com user-agent e IDs; deploy no Render com gunicorn.

---

### ✅ feat/security — SEC-01..03, AUTH-06..08, SEC-08 `Prioridade Alta` *(2026-05-12, `feat/security`)*

CORS estrito; HTTPS obrigatório; headers de segurança; cookies HTTPONLY/SECURE/SameSite; session regeneration pós-login; rate limiting slowapi; legacyLogin.ts removido.

---

### ✅ AUTH-11 + AUTH-12 + DB-01 + TEST-01 — Produção: modal sessão, merge, Neon, e2e `Prioridade Alta` *(2026-05-08, `feat/access-log`)*

Modal de sessão expirada validado em produção; merge `feat/access-log` → `3.1-dev`; PostgreSQL Neon configurado no Render; fluxo completo registo → email → verificação → login → reset validado.

---

## Prioridade Alta

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

`alembic/env.py` lê `DATABASE_URL_MIGRATIONS` (superuser para migrations); `DATABASE_URL` aponta para `chichorro_runtime` (apenas DML). Ações manuais pendentes: criar role no Supabase SQL Editor, atualizar env vars Render e GitHub Secret.

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

`tools/backup_db.py` exporta JSON com descoberta dinâmica de tabelas; `backup-db.yml` cron a cada 3 dias com artifact 90 dias; `tools/restore_db.py` com `--confirm` e rollback automático.

---

### ✅ SEC-08 — Remover legacyLogin.ts e limpar .env (concluído 2026-05-22, branch `audit-fix`)

`legacyLogin.ts` eliminado (código morto, nunca importado); `VITE_LOGIN_USER_1`/`VITE_LOGIN_PASS_1` removidos do `.env` local; build TypeScript 0 erros (M-05).

---

## Prioridade Baixa

### ❌ DB-06 — Migrar camada de dados para SQLAlchemy ORM

Substituir `_PGConn` (psycopg2 manual) por SQLAlchemy 2.x; desbloqueia autogenerate de migrations, connection pooling nativo e type safety. Fora do âmbito do audit — a implementar em branch próprio. Ver [DB-06_UNDONE.md](plans/subplans/DB-06_UNDONE.md).

---

### ❌ INFRA-03 — Dockerfile + Compose

Containerização para deploy reproduzível. Para o Render (PaaS) atual não é bloqueante; relevante para migração futura para VPS/Proxmox.

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

### ❌ MODEL-01 — Método simplificado baseado no CHICHORRO 2.0

Proposta de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1.

---

### ❌ MODEL-02 — Alterar ordem do Cenário 4

CI → VVE → VHE alternativo.

---

### ❌ MODEL-03 — Afinação de custos €/m² via PRONIC

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
