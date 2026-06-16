# Estado do Projeto e Próximos Passos

Última atualização: 2026-06-16 (SEC-11/12 concluídos — política de secrets + Basic Auth pgAdmin/Adminer)

> **Issues tracked in Linear** — team [FireRiskApp](https://linear.app/fireriskapp), projeto **CHICHORRO 3.1** (FIR-5 a FIR-31).
> Usar o Linear como fonte de verdade para estado de tarefas. Este ficheiro mantém-se como referência rápida.

---

## Estado atual

| Área | Estado |
| --- | --- |
| Modelo CHICHORRO 3.1 | ✅ Completo (11/11 paridade backend, e2e aprovado) |
| Autenticação e sessões | ✅ Completo (AUTH-01..09c, AUTH-10, AUTH-11, AUTH-12, AUTH-13) |
| Hardening de segurança | ✅ Completo (audit-fix 16/16 ✅; SEC-04/05/07 ✅; BACK-05/05d/06 ✅) |
| Auditoria segurança/UX | ✅ Completo (S-01..02, U-01..04) |
| Perfil de utilizador | ✅ Completo (AUTH-09, AUTH-09a, AUTH-09b, AUTH-09c, AUTH-09d — avatar WebP 128 px, limite 100 KB) |
| Preferências / Definições | ✅ Completo (UI-06: dark mode, avisar-antes-de-sair, casas decimais) |
| Dark Mode (UI-07) | ✅ Completo — todas as páginas cobertas (commit `d2d6492`) |
| Migração Flask → FastAPI (BACK-01) | ✅ Completo — 11/11 PASS (`feat/flask-to-fastapi`) |
| ASCII enums DPI/CTI (BACK-03) | ✅ Completo (`feat/flask-to-fastapi`) |
| Deploy FastAPI em produção (BACK-04) | ✅ Completo — FastAPI em produção (Render + Supabase); merge em `3.1-dev` |
| Migração Neon → Supabase (DB-02) | ✅ Completo — cold start 45s → 1.5s; per-request connections (PgBouncer) |
| Monitorização (INFRA-01) | ✅ Completo — Sentry frontend + backend ativos; UptimeRobot com email alerts |
| Estratégia de Backups (DB-03) | ✅ Completo — `scripts/backup_db.py`, GitHub Actions workflow, `scripts/restore_db.py`; A-04 (2026-05-22) |
| Documentação | ✅ Completo (DOCS-01 — VitePress em produção; docs.chichorrofireriskapp.joaopmteixeira.net) |
| AI Tooling (AI-02) | ✅ Vault Obsidian completo — 8 fontes, 27 subfatores, RT-SCIE 135/2020, Backend/Frontend (`feat/obsidian-vault`) |
| AI Tooling (AI-02a) | ❌ Curation manual pendente — `## Definicao` (27 notas), validação "verificar", Graph View Obsidian |
| SQLAlchemy ORM (DB-06) | ✅ Completo — SQLAlchemy 2.x; NullPool Neon; migrate_sqlite; WAL; code review F1-F6 ✅ |
| Docker (INFRA-03) | ✅ Completo — Dockerfile Python 3.12-slim + docker-compose.yml; PostgreSQL 16 local; appuser não-root |
| Env separation (INFRA-06) | ✅ Completo — `.env` + `.env.example` + guia deploy Proxmox/Debian 13; deploy verificado em chichorro-staging |
| Staging Proxmox completo (INFRA-07) | ✅ Completo — Nginx reverse proxy + PostgreSQL local; `docker-compose.staging.yml`; stack operacional em 192.168.0.7 |
| Backups PostgreSQL local (DB-07) | ✅ Completo — serviço Docker `backup` com cron diário 02:00 UTC; retenção 7 dumps; validado em staging |
| Migração Supabase → local (DB-08) | ✅ Completo — `scripts/migrate_supabase_to_local.sh`; runbook operacional; validado em staging |
| Cloudflare Tunnel (INFRA-09) | ✅ Completo — `chichorro.joaopmteixeira.net` acessível via HTTPS; `cloudflared` systemd na VM |
| Política de secrets (SEC-11) | ✅ Completo — `docs/deploy/SECRETS_POLICY.md`; inventário + rotação + backup Bitwarden |
| Basic Auth pgAdmin/Adminer (SEC-12) | ✅ Completo — Nginx Basic Auth portas 5050/5051; `./infra/nginx/.htpasswd` gitignored; validado em staging |
| Branch ativo | `3.1-dev` (produção + desenvolvimento) |

Detalhe completo de tudo o que foi implementado: ver [CHANGELOG.md](changelog/CHANGELOG.md).

---

## Concluído Recentemente (2026-06-16)

### ✅ SEC-11 — Política de gestão de secrets (`feat/sec11-sec12-secrets-pgadmin`)

- `docs/deploy/SECRETS_POLICY.md` — inventário completo de secrets, onde NÃO guardar, procedimentos de rotação por tipo (Render, Supabase, SSH, htpasswd), recomendação de backup em Bitwarden
- `docs/deploy/ENV_VARS.md` — secção "Staging — VM Proxmox" com `PGADMIN_EMAIL/PASSWORD` e nota htpasswd; referência a `SECRETS_POLICY.md`
- `docs/plans/subplans/SEC/SEC-11.md` — marcado ✅

### ✅ SEC-12 — Basic Auth Nginx para pgAdmin + Adminer (`feat/sec11-sec12-secrets-pgadmin`)

- `infra/nginx/nginx.conf` — dois `server` blocks: porta 5050 → pgAdmin, porta 5051 → Adminer; `auth_basic` com `/etc/nginx/.htpasswd`
- `docker-compose.staging.yml` — nginx expõe portas 5050/5051; monta `./infra/nginx/.htpasswd:ro`; pgAdmin e Adminer passaram de `ports:` para `expose:` (tráfego só via Nginx)
- `.gitignore` — `infra/nginx/.htpasswd` adicionado
- `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — secção SEC-12 com runbook: instalar apache2-utils, criar htpasswd em `/opt/chichorro/infra/nginx/`, verificar e rodar
- `docs/deploy/GUIDE_PGADMIN.md` — nota de Basic Auth no início; fix MD040
- Validado em staging: `curl -I :5050` → 401, `curl -u admin:<pass> :5050` → HTML pgAdmin ✅
- `docs/plans/subplans/SEC/SEC-12.md` — marcado ✅

### Novos IDs criados

- **SEC-13** — Hardening Docker: Gitleaks CI, redes internas, serviço `migrate`, suporte `*_FILE`, systemd (`docs/plans/subplans/SEC/SEC-13.md`)
- **SEC-14** — SOPS + age (backlog/futuro) — plano completo em `docs/plans/subplans/SEC/SEC-14.md`

---

## Concluído Recentemente (2026-06-15)

### ✅ INFRA-09 — Cloudflare Tunnel para chichorro.joaopmteixeira.net (`feat/infra09-cloudflare-tunnel`)

- `infra/cloudflare/config.yml` — template de configuração do tunnel (`cloudflared`)
- `docker-compose.staging.yml` — `CHICHORRO_CORS_ORIGINS` e `APP_BASE_URL` atualizados com o domínio público
- `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — secção INFRA-09 com runbook completo de 7 passos
- `cloudflared` instalado na VM como serviço systemd; CNAME criado automaticamente no Cloudflare
- Validado: `https://chichorro.joaopmteixeira.net/health/db` → `{"status":"ok","db":"ok"}`

### ✅ DB-07 — Backups PostgreSQL local (`feat/db07-db08-backups`)

- Serviço Docker `backup` (postgres:17-alpine) com cron diário 02:00 UTC via `pg_dump -F c`
- Retenção 7 dumps; `infra/backup/backup.sh` + `infra/backup/restore.sh`; volume `backup_dumps`
- Validado em staging: dump criado, restore OK, `/health/db` → ok

### ✅ DB-08 — Runbook migração Supabase → PostgreSQL local (`feat/db07-db08-backups`)

- `scripts/migrate_supabase_to_local.sh` — pg_dump + drop/recreate + pg_restore + validação de contagens
- `docs/deploy/RUNBOOK_MIGRATION_SUPABASE_TO_LOCAL.md` — 5 passos, plano de fallback 7 dias, rollback
- Validado em staging: 65 access_log + 2 users migrados, login e cálculo POI→RI OK

### ✅ INFRA-07 — Stack staging Proxmox completa (`3.1-dev`)

- `infra/nginx/nginx.conf` — reverse proxy porta 80 → app:8000; headers `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`
- `docker-compose.staging.yml` — stack completa: `db` (PostgreSQL 16-alpine) + `app` (ENV=staging) + `nginx`; healthchecks encadeados
- `.env.example` — `POSTGRES_PASSWORD` documentada
- `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — secção INFRA-07 com tabela comparativa dev vs staging
- Nota operacional: passwords com caracteres especiais (`@`, `.`) devem ser geradas com `python3 -c "import secrets; print(secrets.token_hex(32))"`
- VM `chichorro-staging` (192.168.0.7): SSH key do utilizador `deploy` adicionada ao GitHub; `/opt/chichorro` clonado via SSH sem credenciais; `/health/db` → `{"status":"ok","db":"ok"}`

---

## Concluído Recentemente (2026-06-12)

### ✅ AUTH-09d — Optimizacao avatar WebP 128 px + script de migracao (`3.1-dev`)

- `app/frontend/src/pages/ProfilePage.tsx` — `maxPx` 256→128, `toDataURL` JPEG→WebP q0.80, limite `AVATAR_TOO_LARGE` actualizado para 100 KB
- `app/backend/routers/auth.py` — `_AVATAR_MAX_BYTES` 700 000→100 000
- `scripts/migrate_avatars_to_webp.py` — conversor one-shot JPEG/PNG/GIF→WebP 128 px com `--dry-run`

### ✅ REL-01 — Release baseline v3.1.0 (`3.1-dev`)

- `docs/changelog/CHANGELOG.md` — seccao `[v3.1.0]` criada com sumario completo de todas as funcionalidades 3.1
- 8 novos IDs adicionados ao roadmap VPS: DB-07, DB-08, SEC-11, SEC-12, INFRA-07, INFRA-08, TEST-04
- `docs/plans/subplans/` reorganizado em 13 pastas de categoria (AUTH/, INFRA/, SEC/, DB/, ...)
- `app/frontend/package.json` — script `npm run typecheck` adicionado
- IDs INFRA-06/07 corrigidos (INFRA-06 = env separation concluido; INFRA-07 = staging Proxmox completo pendente)

---

## Concluído Recentemente (2026-06-11)

### ✅ INFRA-06 — Separação de ambientes + deploy Proxmox/Debian 13 (`feat/infra07-env-proxmox` → `3.1-dev`)

- `.env` (gitignored) — credenciais de admin para dev local e Proxmox
- `.env.example` (commitado) — template documentado de todas as variáveis
- `docker-compose.yml` — `env_file` com `required: false` (CI-safe)
- `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — guia de instalação Docker em Debian 13 e deploy

---

## Concluído Recentemente (2026-06-09)

### ✅ DB-06 — Migração SQLAlchemy ORM (`refactor/db06-sqlalchemy` → `3.1-dev`)

- `app/backend/models.py` — `DeclarativeBase` + `User` + `AccessLog` com `Mapped`/`mapped_column`
- `app/backend/database.py` — engine `NullPool` (Neon PgBouncer); `migrate_sqlite()` per-coluna; WAL pragma listener; `get_db()` como context manager `Session`
- `app/backend/main.py` — `lifespan` com `create_all` + `migrate_sqlite` em dev
- `app/backend/alembic/env.py` — `target_metadata = Base.metadata` para autogenerate
- Code review high effort: 6 findings F1-F6 corrigidos (IntegrityError handler, None guards, column projection admin, WAL)
- 342 testes pass; `/health/db` ✅; registo concorrente → 409 ✅ (sem 500)

---

### ✅ INFRA-03 — Dockerfile + Compose (`3.1-dev`)

- `Dockerfile` — Python 3.14-slim, gunicorn+uvicorn, utilizador `appuser` não-root
- `docker-compose.yml` — serviços `backend` + `db` (PostgreSQL 16), volumes e env vars
- `.dockerignore` — exclui caches e docs
- `docs/plans/subplans/INFRA/INFRA-03.md` — subplan documentado

---

## Concluído Recentemente (2026-06-05)

### ✅ AI-02 Passo 8 (FIR-35) — RT-SCIE 135/2020 + Backend/Frontend fontes

- RT-SCIE Portaria 135/2020 convertida: 302 artigos em `docs/regulations/Portaria-135_2020/articles/` com tabelas markdown preservadas; `delta_1532_to_135.md` (3851 linhas de alterações)
- `map_sources.py` — `scan_rtscie()` reutilizado para `rtscie2020`; Backend/Frontend populados via registry lookup (27 subfatores cada)
- 27 subfatores × 8 fontes preenchidos; 190 artigos RT-SCIE com backlinks `## Subfatores relacionados`
- `build_vault.py --force` preserva agora a secção `## Onde e mencionado` (fix bug validações)

---

## Concluído Recentemente (2026-06-02)

### ✅ AI-02 (FIR-35) — Pipeline de investigação + Vault Obsidian CHICHORRO

**Pipeline de investigação (`feat/research-organization` → mergeado em `3.1-dev`):**

- RT-SCIE Portaria 1532/2008 — PDF original + 309 artigos em `docs/regulations/Portaria-1532_2008/articles/` com frontmatter YAML; `_pipeline/` genérico para novos regulamentos
- `scripts/thesis_convert.py` + `thesis_worker.py` — converter docling com chunks de 12 páginas e marcadores `<!-- page: N -->`; teses 4.0 IC (366 págs, 112 chunks), 3.0 JPT (250 págs, 194 chunks), 3.1 RS (140 págs, 104 chunks) convertidas
- `docs/vault/_data/chichorro-registry.json` — fonte única: 5 fatores, 27 subfatores com `calc_linha`/`frontend_linha`, 9 fontes
- `scripts/map_sources.py` — heading-aware; mantém `heading_stack` + `current_page`; popula `## Onde e mencionado` com subcapítulo + página + links `[[art_xxx_...]]` para RT-SCIE
- `scripts/build_vault.py` — 48 notas geradas (idempotente, `--force` para regenerar); frontmatter YAML com `tipo`, `codigo`, `aliases`, `tags`; `[[wiki-links]]`
- Vault root expandido de `docs/vault/` para `docs/` — teses `.ai.md` e artigos RT-SCIE acessíveis no Obsidian; links `[[art_xxx_...]]` resolvem no Graph View
- Graph View configurado: fator=verde, subfator=azul, fonte=laranja, conceito=cinza

---

## Concluído Recentemente (2026-06-01)

### ✅ AI-01 (FIR-34) — Setup Graphify

- Graphify instalado (manual — auto-installer bloqueado por classificador supply chain)
- Grafo cross-stack: 740 nós / 1657 arestas / 44 comunidades — backend (367), frontend (346); god nodes: `_get_db()`, `getAppStorage()`, `Request`
- `CLAUDE.md` criado na raiz com mapa de arquitetura + regras de refresh do grafo
- `.gitignore` expandido: artefactos Graphify + `docs/vault/`
- `docs/TODO_LIST.md` + `docs/TODO_PRIORITIES.md` — secção AI Tooling formalizada (AI-NN)
- `docs/plans/subplans/AI/AI-01.md` criado; FIR-34 fechado no Linear
- `docs/ai/OBSIDIAN_VAULT.md` — plano detalhado AI-02; FIR-35 criado

*(Trabalho de 2026-05-31 — documentação da estratégia IA — incorporado nesta sessão: `docs/ai/SETUP_GRAPHIFY.md`, `docs/ai/OBSIDIAN_SETUP.md`, `docs/research/RAG_FUTURE.md`)*

---

## Concluído Recentemente (2026-05-29)

### ✅ fix(poi) — TipoEdif2 com tipo pai como primeira opção

- `app/backend/schemas/poi.py` — valores pai (`Industria`, `Oficinas`, `Desporto`) adicionados como primeira opção em `POI_ATIV_TipoEdif2`; desbloqueia cálculo quando não é necessário subtipo
- `app/frontend/src/components/poi/poiDefinitions.ts` — tipo pai como primeira entrada em cada grupo; backend `else` clauses já devolviam o valor pai correto

### ✅ chore — Tabelas Excel de investigação excluídas do git

- `docs/research/tables/` adicionado ao `.gitignore`; 5 ficheiros Excel removidos do índice git

### ✅ refactor(repo) — Reorganização da raiz do repositório

- `server/` dissolvido: 56 ficheiros Markdown → `docs/audits/security/` (13) + `docs/audits/cloud-vps/` (43) + `docs/ai/handoffs/` (2)
- `tools/` → `scripts/` via `git mv` (histórico preservado); `.gitignore` atualizado
- `sessions/` → `var/sessions/`; `deploy/` reestruturado com subdirs `env/` e `nginx/`
- `README.md` criado na raiz com overview, requisitos e comandos

### ✅ refactor(docs) — Reorganização interna de docs/

- 15 ficheiros movidos de `docs/` root para subdirs temáticas: `project/`, `method/`, `guides/`, `changelog/`, `deploy/`
- `docs/.vitepress/config.ts` — todos os links de nav e sidebar atualizados
- Cross-refs em `PRD.md`, `SERVICES.md`, `BACKEND_GUIDELINES.md`, `FRONTEND_GUIDELINES.md` corrigidas

### ✅ fix(repo) — Cleanup pós-reorganização (Codex review)

- `README.md` raiz — 3 links quebrados corrigidos
- `.gitignore` — `!scripts/restore_db.py` adicionado; política de tracking documentada
- `docs/audits/cloud-vps/README.md` — nota de path histórico adicionada
- `scripts/restore_db.py` — passado a tracked

---

## Concluído Recentemente (2026-05-28)

### ✅ SEC-04b — Remoção do fallback werkzeug

- `app/backend/routers/auth.py` — `_verify_password` simplificada: apenas `_PH.verify` (argon2id); fallback werkzeug e upgrade-on-login removidos
- `app/backend/requirements.txt` — `werkzeug>=3.0,<4` removido

### ✅ DOCS-02 — Uniformização headers subplans

- 58 ficheiros `docs/plans/subplans/` — formato canónico Estado → Data de conclusão → Branch aplicado em batch
- `docs/plans/subplans/DESIGN.md` eliminado (duplicado de `docs/DESIGN.md`)
- `docs/TODO_PRIORITIES.md` — SEC-09 ❌ duplicado removido; INFRA-04 corrigido ❌→✅

### ✅ fix — Session remount no AppLayout

- `app/frontend/src/pages/AppLayout.tsx` — `key={sessionKey}` no `<Outlet>` para forçar remount ao importar/limpar sessão

### ✅ fix — POI campos condicionais + sync CTI↔ATIV

- `app/backend/schemas/poi.py` — `POI_IA_TipoInst2` e `POI_ATIV_TipoEdif2` tornados `Optional[Literal[...]] = None` nos 3 modelos
- `app/frontend/src/components/poi/PoiFactorSection.tsx` — payload filtrado por `opts.length > 0`; pré-actualização CTI module inputs em `setField`
- `app/frontend/src/pages/CtiPage.tsx` — `disabled={isTipoEdifSynced}` removido; pré-actualização POI module inputs em `update`; sync bidirecional funcional

### ✅ test — Verificador de paridade + cobertura de Literals (338 testes)

- `tools/check_option_parity.py` — verificador estático frontend↔backend; detetou 2 bugs reais
- `app/backend/tests/test_valid_options.py` — 338 testes parametrizados auto-gerados; todos os subfatores cobertos

### ✅ fix(schemas) — POI_CC_Idade sem espaços + DPI_OGS_Aplica phantom removido

- `POI_CC_Idade`: `"1991 - 2008"` → `"1991-2008"` (e restantes intervalos) em `poi.py`
- `DPI_OGS_Aplica`: `"Nao Existe"` removido de `dpi.py` (phantom — não está no modelo nem no frontend)

### 📋 plan — CALC_AUDIT criado (bloqueado)

- `docs/plans/main/CALC_AUDIT.md` — plano para ~280 golden tests que validam tabelas de lookup contra tese3.1
- Bloqueado: aguarda Excel da tese3.1 pelo utilizador

---

## Concluído Recentemente (2026-05-27)

### ✅ SEC-04 — Argon2id password hashing + upgrade-on-login

- `argon2-cffi>=23.1` adicionado ao `requirements.txt`
- `_PH = PasswordHasher()` (RFC 9106 level 1: `m=65536, t=3, p=4`)
- `_verify_password`: positivo em `$argon2`, tudo o resto → `check_password_hash` werkzeug (cobre scrypt e pbkdf2)
- Upgrade-on-login: após login com hash não-argon2, re-hash e UPDATE atómico na BD
- Branch `sec/hardening` mergeada em `3.1-dev` com `--no-ff` (commit `a9c788e`)

### ✅ SEC-07 — Validação magic bytes no upload de avatar

- `_check_avatar_magic()`: decodifica os primeiros 12 bytes reais do base64 e valida assinatura
- JPEG `\xff\xd8\xff` · PNG `\x89PNG` · WebP `RIFF...WEBP` · GIF `GIF8`/`GIF9`
- SVG e qualquer tipo fora da lista rejeitados com HTTP 400
- Branch `sec/hardening` mergeada em `3.1-dev` com `--no-ff` (commit `a9c788e`)

### ✅ SEC-05 — SHA-256 dos tokens de verificação/reset/email-change na BD

- `_hash_token(token)` → `hashlib.sha256(token.encode()).hexdigest()` (64 hex chars)
- 3 stores (register, forgot-password, profile/email) guardam o hash; token em claro vai apenas no email/URL
- 3 lookups (verify, reset-password, verify-email-change) fazem WHERE pelo hash
- Fix CSRF: `/auth/register`, `/auth/forgot-password`, `/auth/reset-password` adicionados a `_CSRF_EXEMPT`
- Validado em produção: hash SHA-256 visível na BD Supabase; fluxo completo testado ✅
- Branch `sec/token-hashing` mergeada em `3.1-dev` com `--no-ff` (commit `f09437f`)

### ✅ BACK-05 — Pydantic Literal types nos schemas de cálculo

- `schemas/dpi.py` — todos os 23 campos reescritos com `Literal` (valores extraídos de `Chichorro_DPI.py`)
- `schemas/esci.py` — todos os 23 campos reescritos com `Literal` (valores extraídos de `Chichorro_ESCI.py`)
- `schemas/cti.py` — 13 campos `str` livres substituídos por `Literal`; aliases `_DISPOSITIVOS`/`_REACAO_FOGO`; `model_validator(mode="before")` e `normalize_cti_fields` preservados (Literal usa valores pós-normalização)
- `poi.py` diferido (139 campos — BACK-05d, tarefa separada)
- Payloads inválidos retornam agora HTTP 422 em vez de calcular resultados errados
- `sessions/*.json` actualizados para conformidade: `VHE_Dispositivos`/`VVE_Dispositivos` adicionados ao CTI; `DPI_OGS_OGS` corrigido (ç→c); campos ESCI em falta adicionados
- Branch `back/validation`; validado em produção ✅

### ✅ BACK-06 — Error handler JSON normalizado

- `app/backend/main.py` — `unhandled_exception_handler` passa a retornar `JSONResponse({"error": "INTERNAL_ERROR", "request_id": ...}, 500)` em vez de re-lançar a exceção
- `HTTPException` continua a ser re-lançada (FastAPI trata nativamente)
- Garante que erros 5xx inesperados produzem sempre JSON estruturado (nunca HTML ou stack trace)
- Branch `back/validation`; validado em produção ✅

### ✅ BACK-05d — Pydantic Literal types em poi.py

- `schemas/poi.py` — 49 campos `str` livres substituídos por `Literal[...]` em 12 sub-modelos + `POIRequest` completo
- Valores extraídos directamente de `calc/Chichorro_POI.py`; sem `model_validator` (valores literais directos)
- `POI_ATIV_TipoEdif2` usa union flat dos 19 valores possíveis — sem cross-field validation, mas rejeita valores completamente inválidos
- `docs/plans/subplans/BACK/BACK-05.md` actualizado com secção BACK-05d
- Branch `back/validation` (fresca); validado localmente (`ValidationError: literal_error` ✅)

### ✅ TEST-02 — Infraestrutura pytest e testes iniciais

- `pytest>=8.0,<9` e `pytest-cov>=5.0,<6` adicionados a `requirements.txt`
- `app/backend/pytest.ini` — `testpaths = tests`
- `app/backend/tests/conftest.py` — fixture `client` (override `require_auth` + seed CSRF cookie), fixture `ch` (headers CSRF), fixtures de payload para DPI/ESCI/CTI/POI
- `tests/test_health.py` — `GET /health` e `GET /health/db` (tolerante a BD indisponível)
- `tests/test_literals.py` — POST com campo Literal inválido → 422; auth login sem body → 422; auth login inválido → 401
- `tests/test_calc.py` — POST com payload válido → 200 + resultado numérico `0 < x ≤ 5`
- **12/12 testes passam** em 0.22s localmente ✅
- Branch `test/automated-tests`; subplan `TEST-02.md` criado

### ✅ INFRA-02 — Pipeline CI/CD GitHub Actions

- `.github/workflows/test.yml` — ativa em push/PR com alterações em `app/backend/**`; Python 3.12; `pytest -v --cov`
- `.github/workflows/build.yml` — ativa em push/PR com alterações em `app/frontend/**`; Node 20; `npm ci && npm run build`
- Path filters: cada workflow corre apenas quando os ficheiros relevantes mudam
- Sem Render Deploy Hook por agora (deploy permanece manual)
- Branch `infra/ci-cd`; subplan `INFRA-02.md` criado

---

## Concluído Recentemente (2026-05-26)

### ✅ AUTH-10 — Sistema de roles e UI admin

- Coluna `role TEXT NOT NULL DEFAULT 'engineer'` — migration `0003_add_user_role.py` via Alembic
- `deps.py` — `require_admin`: 401 se não autenticado, 403 se não admin
- Login env var → `session["chichorro_role"] = "admin"` · Login DB → role da BD na sessão
- `/auth/me` devolve `role` · `/admin/users` e `/admin/log` protegidos por `require_admin`
- Frontend: `saveRole`/`getRole` em `session.ts` · grupo ADMIN condicional no fundo do sidebar
- `AdminUsersPage.tsx` — tabela: username, email, verificado, role (badge), criado em (YYYY-MM-DD HH:MM)
- `AdminLogPage.tsx` — tabela: timestamp, username, evento, IP, user agent (limit 200)
- Verificado em produção: anónimo → 401 ✅ · admin → 200 ✅ · engineer → 403 ✅
- Ação manual executada: `UPDATE public.users SET role = 'admin' WHERE username = 'JoaoTeixeira';`
- Branch `auth/roles` mergeada em `3.1-dev` com `--no-ff`

### ✅ audit-fix-2 — Codex findings #2-7

- #2 — Validação positiva `https://` com `urlparse` em `config.py` (rejeita `ftp://`, URLs sem esquema)
- #3 — `DATABASE_URL_MIGRATIONS` obrigatória em produção; Alembic falha explicitamente sem ela
- #4 — Backup usa `DATABASE_URL_BACKUP` (role `chichorro_backup`, só SELECT); ações manuais documentadas em `DEPLOY_PRODUCTION.md`
- #5 — `backup_db.py`: PK descoberta via `information_schema`; `sql.Identifier` em vez de f-string
- #6 — `README.md` frontend sem referências a `VITE_LOGIN_*`
- #7 — CSP: `*.ingest.de.sentry.io` adicionado em `_headers` e `main.py`
- Branch `audit-fix-2` mergeada em `3.1-dev` (commit `9f07380`)

### ✅ Codex security review — documentação

- `CODEX_REVIEW_BRIEF.md` — brief para revisão pelo OpenAI Codex (diff `c559e34..2cd965a`, 16 planos)
- `CODEX_REVIEW_FINDINGS_FOR_CLAUDE.md` — 6 findings do Codex (CRITICAL→LOW)
- `CODEX_REVIEW_ANALYSIS_CLAUDE.md` — análise Claude: concordância, ordem de correção, finding #7 (CSP Sentry)

### ✅ Fix CSRF cookie_domain — split-domain

- `app/backend/main.py` — `cookie_domain` adicionado ao `CSRFMiddleware`; em produção scoped ao hostname do frontend
- Causa: CSRF cookie ilegível em `document.cookie` no frontend (subdomínio diferente do backend) → 403 em todos os POST
- Verificado: `Domain=chichorrofireriskapp.joaopmteixeira.net` no `Set-Cookie`

### ✅ Fix RLS Supabase — chichorro_runtime

- Supabase ativa RLS por defeito; `chichorro_runtime` sem políticas RLS → vê zero linhas → login 401
- Fix manual: `ALTER TABLE public.users DISABLE ROW LEVEL SECURITY; ALTER TABLE public.access_log DISABLE ROW LEVEL SECURITY;`
- Migração Alembic `0002_disable_rls.py` criada para reproduzir o fix automaticamente
- Login confirmado a funcionar

### ✅ Secção 8 da checklist — verificação pós-deploy concluída

- `/health` → `X-Request-ID` + `Cache-Control: no-store` ✅
- `/health/db` → HTTP 200 ✅
- Alembic migrations aplicadas no Render ✅
- Login e operações com `chichorro_runtime` ✅
- Artifact backup GitHub Actions confirmado (users.json, access_log.json, meta.json) ✅
  - Dados estavam a zero no run de 25 Mai (RLS bloqueava SELECTs); próximo run a 28 Mai terá dados reais

## Concluído Recentemente (2026-05-24)

### ✅ Fix deploy — alembic/env.py SQLAlchemy engine (concluído 2026-05-24)

- `app/backend/alembic/env.py` corrigido: substituída ligação raw `psycopg2.connect()` por `sqlalchemy.create_engine()` + `engine.connect()`
- Causa: alembic 1.18.4 (SQLAlchemy 2.0) exige `Connection` SQLAlchemy em `context.configure()`; `psycopg2.extensions.connection` não tem atributo `.dialect` → `AttributeError` → exit 1
- Bug invisível em desenvolvimento (alembic só corre no Render); detectado via `PYTHONUNBUFFERED=1` nos logs
- Deploy verde no Render às 18:02 UTC em `audit-fix`; commit `a07fe55` cherry-picked para `3.1-dev`

### ✅ Ações manuais nos dashboards (concluído 2026-05-24)

- Supabase — role `chichorro_runtime` criado + GRANTs; connection string PgBouncer obtida
- Render — `DATABASE_URL` → `chichorro_runtime`; `DATABASE_URL_MIGRATIONS` → `postgres`; `UPSTASH_REDIS_URL` corrigida (formato `rediss://`)
- GitHub Secrets — `DATABASE_URL` + `RESEND_API_KEY` configurados
- UptimeRobot — monitor `/health/db` a cada 5 min; Sentry — alert rule `> 10 eventos/1h`
- Cloudflare Pages — vars e domínio verificados

### ✅ B-01 — Consolidação docs de deploy (concluído 2026-05-24)

- `docs/deploy/ENV_VARS.md` reescrito: adicionadas `FRONTEND_URL`, `BACKEND_URL`, `DATABASE_URL_MIGRATIONS`, `VITE_API_BASE_URL`; `UPSTASH_REDIS_URL` marcada obrigatória; comandos Render corrigidos (uvicorn + `alembic upgrade head`)
- `docs/deploy/DEPLOY.md` actualizado: referência a `DEPLOY_PRODUCTION.md`; gunicorn/wsgi removido
- `server/cloud_vps_audit_plans/DEPLOY_CLOUD_VPS.md` apagado — conteúdo integralmente em `DEPLOY_PRODUCTION.md`
- **Audit-fix 16/16 completo**

---

### ✅ BACK-07 / B-02 — Naming de rotas API (concluído 2026-05-24)

- Aliases legacy removidos: `/login`, `/logout`, `/me` em `auth.py`; `/RI_interv` em `ri.py` (dead code confirmado por grep)
- Decisão documentada: rotas actuais mantidas; prefixo `/api` é responsabilidade do proxy nginx, não da app
- Nginx VPS prefix-strip config adicionada ao `DEPLOY_PRODUCTION.md`
- Branch `audit-fix` (15/16 planos completos ao momento)

---

### ✅ INFRA-01 / M-04 — Observabilidade mínima (concluído 2026-05-24)

- `app/backend/main.py`: middleware `add_request_id` — gera UUID por pedido, expõe em `X-Request-ID` no cabeçalho da resposta; tag `request_id` adicionada ao scope Sentry no exception handler para correlação de eventos
- `.github/workflows/backup-db.yml`: step `if: failure()` com notificação via Resend API para `eng.joao.pm.teixeira@gmail.com` — independente da conta GitHub; inclui link direto para o run falhado
- **Ações manuais pendentes:**
  1. UptimeRobot — adicionar monitor HTTP para `/health/db` (5 min)
  2. Sentry dashboard — criar alert rule: > 10 eventos em 1h → e-mail
  3. GitHub Secrets — adicionar `RESEND_API_KEY` em Settings → Secrets and variables → Actions
- Branch `audit-fix` (14/16 planos completos ao momento)

---

### ✅ DB-05 / C-03 — Least Privilege DB User (concluído 2026-05-24)

- `app/backend/alembic/env.py`: `db_url = os.environ.get("DATABASE_URL_MIGRATIONS") or settings.database_url` — Alembic usa superuser (`postgres`) para migrations; app runtime usa `chichorro_runtime` (só DML)
- `deploy/env.production.example`: `DATABASE_URL_MIGRATIONS` documentada com comentário explicativo
- `DEPLOY_PRODUCTION.md`: secção Supabase SQL completa, checklists, ordem de atualização de env vars no Render
- `docs/plans/subplans/DB/DB-05.md`: subplan criado
- **Ações manuais pendentes (por esta ordem):**
  1. Supabase SQL Editor — criar role `chichorro_runtime` + GRANTs (SQL em DEPLOY_PRODUCTION.md)
  2. Render — copiar `DATABASE_URL` atual; atualizar para URL de `chichorro_runtime`; adicionar `DATABASE_URL_MIGRATIONS` com URL de `postgres`
  3. GitHub Actions — atualizar secret `DATABASE_URL` para `chichorro_runtime`; trigger manual de `backup-db.yml`
- Branch `audit-fix`

---

## Concluído Recentemente (2026-05-22)

### ✅ DB-03 / A-04 — Backups externos e restore (concluído 2026-05-22)

- `.github/scripts/backup_db.py`: substituída lista estática `["users", "access_log"]`
  por descoberta dinâmica via `information_schema.tables`; novas tabelas incluídas
  automaticamente; `alembic_version` excluída (metadata de schema)
- `tools/backup_db.py` (local, gitignored): mesma atualização para paridade com CI
- `tools/restore_db.py` (novo, gitignored): restore de JSON backup com `--confirm`
  obrigatório; transação única com rollback automático em erro
- `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md`: secção GitHub Secrets
  adicionada — secret `DATABASE_URL` para o workflow `backup-db.yml`
- `docs/plans/subplans/DB/DB-03.md`: secções de backup automático externo e restore
  adicionadas; instrução de Alembic pré-restore documentada
- **Ação manual pendente:** adicionar secret `DATABASE_URL` em GitHub →
  Settings → Secrets and variables → Actions
- Branch `audit-fix`

### ✅ SEC-06 / A-05 — Política de logs sem tokens/PII (concluído 2026-05-22)

- `app/backend/main.py`: `_TokenPathFilter` registado no `uvicorn.access` logger — substitui tokens em `/auth/verify/{token}` e `/auth/verify-email-change/{token}` por `[REDACTED]` nos access logs do Render
- `app/backend/services/email.py`: guard `env != "production"` antes de cada `print()` (defesa em profundidade; C-04 já impede arranque sem `RESEND_API_KEY`)
- Sentry já tinha `send_default_pii=False` — sem alteração
- Sem novas variáveis de ambiente; sem ações manuais no Render ou Cloudflare
- Branch `audit-fix`

### ✅ DB-04 / A-03 — Migrations Alembic (concluído 2026-05-22)

- `app/backend/alembic.ini` + `app/backend/alembic/` criados (env.py, script.py.mako, versions/0001_initial_schema.py)
- `alembic/env.py`: ligação psycopg2 via `settings.database_url`; falha com `RuntimeError` se `DATABASE_URL` não definida
- `alembic/versions/0001_initial_schema.py`: snapshot completo do schema atual (`access_log` + `users`); usa `IF NOT EXISTS` — idempotente na Supabase existente
- `app/backend/main.py`: `init_db()` guardado para dev SQLite (`not settings.database_url`); produção usa Alembic Release Command
- `requirements.txt`: `alembic>=1.13,<2` adicionado (instalado 1.18.4)
- **Ação pendente no Render:** definir Release Command: `cd app/backend && alembic upgrade head`
- Branch `audit-fix`

### ✅ INFRA-05 / M-02 — Cache-Control no edge e backend (concluído 2026-05-22)

- `app/backend/main.py`: `Cache-Control: no-store` adicionado ao middleware `add_security_headers`
- `app/frontend/public/_headers`: `Cache-Control: no-store` em `/*`; nova regra `/assets/*` com `public, max-age=31536000, immutable`
- Assets Vite fingerprintados (nomes com hash) cacheados 1 ano de forma segura; `index.html` nunca cacheado
- Branch `audit-fix`

### ✅ SEC-09 / M-01 — CSP e headers de segurança (concluído 2026-05-22)

- `app/backend/main.py`: `Content-Security-Policy` e `Permissions-Policy` adicionados ao middleware `add_security_headers`
- CSP: `default-src 'self'`; Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`); Sentry (`*.ingest.sentry.io`); sem `'unsafe-inline'` (zero inline styles confirmado)
- `app/frontend/public/_headers` criado (novo): headers Cloudflare Pages com `connect-src` que inclui domínio backend e HSTS `preload`
- Branch `audit-fix`

### ✅ AUTH-07 / A-02 — Fail-fast Redis no arranque (concluído 2026-05-22)

- `app/backend/main.py`: função `_check_redis_startup()` + lifespan atualizado
- Pinga Redis em produção antes de aceitar requests (`socket_connect_timeout=5`)
- URL inválida → `RuntimeError A-02` no arranque em vez de HTTP 500 na primeira request
- Token Redis nunca exposto nos logs (`type(exc).__name__` em vez de `str(exc)`)
- `deploy/env.production.example`: comentário sobre TLS obrigatório + comportamento A-02
- Branch `audit-fix`

### ✅ INFRA-04 / A-06 — Endpoint `/health/db` com query real à BD (concluído 2026-05-22)

- `app/backend/main.py`: endpoint `GET/HEAD /health/db` adicionado (rota síncrona — thread pool)
- Executa `SELECT 1` via `_get_db()` existente — suporta PostgreSQL e SQLite
- HTTP 200 `{"status":"ok","db":"ok"}` / HTTP 503 `{"status":"error","db":"unreachable"}` sem expor internos
- `/health/db` adicionado a `_CSRF_EXEMPT` para Render e monitorizações externas
- Branch `audit-fix`

### ✅ SEC-01 / A-01 — CORS estrito em produção (concluído 2026-05-22)

- `app/backend/config.py`: 3 checks A-01 adicionados ao `validate_production_urls`:
  - Rejeita `*` em qualquer CORS origin
  - Rejeita origins com `http://` (apenas `https://` permitido em produção)
  - Rejeita se `FRONTEND_URL` não estiver incluída nas CORS origins
- `deploy/env.production.example`: comentário junto a `CHICHORRO_CORS_ORIGINS` com as regras A-01
- 5/5 testes de import Python aprovados
- Branch `audit-fix`

---

## Concluído Recentemente (2026-05-21)

### ✅ AUTH-06 / C-02 — Cookies Secure/SameSite + proxy headers (concluído 2026-05-21)

- `app/backend/config.py`: `field_validator("session_samesite")` — restringe `CHICHORRO_SESSION_SAMESITE` a Lax/Strict
- `app/backend/wsgi.py`: documentados start commands Render (`--proxy-headers --forwarded-allow-ips='*'`) e VPS futura
- `deploy/env.production.example`: secção "Render start command" com nota do `--proxy-headers`
- Nota: `ProxyHeadersMiddleware` removido no Starlette 1.0.0 — uvicorn flags são a abordagem correta
- **Ação pendente no Render:** atualizar Start Command → `uvicorn main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*'`
- Branch `audit-fix`

### ✅ SEC-08 / M-05 — Remover legacyLogin.ts e VITE_LOGIN_* (concluído 2026-05-21)

- `app/frontend/src/auth/legacyLogin.ts` eliminado — código morto, nunca importado
- `VITE_LOGIN_USER_1`/`VITE_LOGIN_PASS_1` removidos de `.env` local (gitignored, alteração local)
- Build frontend: 0 erros · grep: 0 referências residuais
- Branch `audit-fix` (commit direto — metodologia audit)

### ✅ SEC-10 / C-04 — Fail-fast secrets em produção (concluído 2026-05-21)

- `app/backend/config.py`: `validate_production_urls` estendido com 6 checks C-04 — `CHICHORRO_SECRET_KEY=dev-change-me` rejeita arranque; `DATABASE_URL`, `CHICHORRO_CORS_ORIGINS`, `UPSTASH_REDIS_URL`, `RESEND_API_KEY`, `MAIL_DEFAULT_SENDER` obrigatórias em produção
- `deploy/env.production.example` e `deploy/env.development.example` criados como referência para o Render e para dev local
- 8/8 testes de import Python aprovados (6 falham esperadamente, 2 passam)
- Branch `sec/c04-production-secrets`, merge `--no-ff` em `3.1-dev`

### ✅ SEC-02 / C-01 — TLS end-to-end, fail-fast URLs produção (concluído 2026-05-21)

- `app/backend/config.py`: novos campos `env`, `frontend_url`, `backend_url`; `model_validator` fail-fast em produção (FRONTEND_URL/BACKEND_URL obrigatórias e https://); `app_base_url` overridden por `FRONTEND_URL` em produção
- `deploy/nginx-chichorro.example.conf`: Flask→FastAPI nos comentários; `X-Forwarded-Host $host` adicionado
- 5/5 testes de import Python aprovados (3 falham esperadamente em produção, 2 passam)
- Novos IDs criados: SEC-10, INFRA-05, INFRA-07, BACK-07, DB-05 (planos C-04, M-02, M-03, B-02, C-03)
- Inconsistência corrigida: `TODO_PRIORITIES.md` agora diz PostgreSQL (Supabase) em vez de (Neon)

---

## Concluído Recentemente (2026-05-20)

### ✅ DOCS-01 — Migração para VitePress (concluído 2026-05-20)

- Docsify substituído por VitePress ^1.6.4: build estático, SEO nativo, Vite-native
- `docs/.vitepress/config.ts` — sidebar com 6 secções, PT-PT, `cleanUrls`, `lastUpdated`, search local, `socialLinks` a apontar para `fireriskapp-docs`
- `docs/index.md` — homepage com hero e quick links
- `docs/_sidebar.md` apagado (Docsify legacy — causava 18 dead links no build VitePress)
- `docs/README.md` reescrito — apenas links para ficheiros públicos; removidos: `deploy/`, `plans/`, `security/`, `audits/`, `migration/`, `HISTORY_AI.md`
- `.github/workflows/sync-docs.yml` — `audits/` excluída do sync (segurança)
- Deploy: Cloudflare Pages via `fireriskapp-docs` (repo público); domínio `docs.chichorrofireriskapp.joaopmteixeira.net`; build `npm ci && npm run build`; output `.vitepress/dist`
- Build local 0 dead links; build Cloudflare verde

---

## Concluído Recentemente (2026-05-19)

### ✅ DB-03 — Estratégia de Backups (concluído 2026-05-19)

- `tools/backup_db.py` — exporta `users` e `access_log` para JSON timestamped em `tools/backups/` (gitignored); usa psycopg2, sem dependência de pg_dump
- `docs/deploy/ENV_VARS.md` — referência completa de todas as env vars (backend + frontend) por serviço, com indicação de onde obter cada valor
- `docs/plans/subplans/DB/DB-03.md` — subplan com limitações do Supabase free tier e frequência de backup recomendada

### ✅ INFRA-01 — Monitorização completa (concluído 2026-05-19)

- Frontend Sentry (`@sentry/react` + ErrorBoundary + Session Replay) ativo na Cloudflare Pages; validado em produção — erro capturado com replay da sessão anexado
- Session Replay: `replaysSessionSampleRate: 0.0` + `replaysOnErrorSampleRate: 1.0` — grava replay apenas em erros, com `maskAllText` e `blockAllMedia`
- Backend Sentry via `sentry-sdk` base + `@app.exception_handler(Exception)` — captura todos os erros 5xx sem depender de `StarletteIntegration`/`FastApiIntegration` (incompatíveis com Starlette 1.0.0 + Python 3.14); validado em produção
- UptimeRobot: monitor `/health` a cada 5 min (147ms avg), email `chichorrofireriskapp@gmail.com` configurado
- Fixes colaterais: starlette-csrf `re.compile()` (commit `5f195e1`), HEAD support no `/health` (commit `576a55c`)

---

## Concluído Recentemente (2026-05-18)

### ✅ AUTH-13 — Hardening de segurança da sessão (concluído 2026-05-18)

- Cookie de sessão passa a expirar automaticamente após 8h (configurável via `CHICHORRO_SESSION_MAX_AGE`)
- `session_secure=True` por omissão quando `ENV=production` — não precisa de ser definido manualmente
- Proteção CSRF ativa em todos os endpoints POST (exceto login/logout/health)
- Frontend envia automaticamente token CSRF em todos os pedidos
- `Flask.py` legado eliminado do repositório

### ✅ UI-07 — Dark Mode completo (concluído 2026-05-18)

- RiPage, CtiPage, InterventionsPage e todas as páginas de autenticação cobertas
- Títulos e subtítulos das páginas POI, DPI, ESCI com suporte dark mode
- Paleta neutra dark revisada; border de card header oculta quando colapsada

### ✅ Correções de sidebar e avatar (2026-05-18)

- Botão "Limpar sessão" restaurado na sidebar (tinha sido removido acidentalmente)
- `SidebarNavItem` passa a ter prop `variant` (default/warning/danger) em vez de `danger: boolean` — "Limpar sessão" em âmbar, "Sair" em vermelho
- Avatar atualiza instantaneamente na sidebar após gravação (dispatch `PROFILE_UPDATED_EVENT`)

---

## Concluído Recentemente (2026-05-15)

### ✅ BACK-04 — Deploy FastAPI no Render (concluído 2026-05-15)

- ✅ Passo 1 — `_add_column()` com `IF NOT EXISTS` em `database.py`
- ✅ Passo 2 — Merge `3.1-dev` → `feat/flask-to-fastapi` (sem conflitos)
- ✅ Passo 3 — `parity_runner.py` → 11/11 PASS
- ✅ Passo 4 — Deploy no Render: `itsdangerous` adicionado; conexões por request (Supabase + PgBouncer)
- ✅ Passo 5 — Teste e2e: login 1.5s, `/auth/me` 275ms, sem cold start
- ✅ Passo 6 — Merge `feat/flask-to-fastapi` → `3.1-dev` (commit `748dff1`)
- ✅ Passo 7 — Docs actualizados

### ✅ DB-02 — Migração Neon → Supabase (concluído 2026-05-15)

- Cold start 45s eliminado (Supabase pausa após 1 semana vs 5 min no Neon)
- `SimpleConnectionPool` incompatível com gunicorn fork → per-request connections via PgBouncer
- `DATABASE_URL` (porta 6543, pooler IPv4) substituiu `NEON_DATABASE_URL`
- 2 utilizadores migrados com `tools/migrate_neon_to_supabase.py`

---

## Concluído em 2026-05-14

### ✅ BACK-01 — Migração Flask → FastAPI

- Scaffold FastAPI: `calc/`, `config.py`, `database.py`, `deps.py`, `main.py`
- Pydantic schemas para todos os endpoints (auth, poi, cti, dpi, esci, ri)
- Routers modulares: `routers/auth.py`, `routers/admin.py`, `routers/poi.py`, `routers/cti.py`, `routers/dpi.py`, `routers/esci.py`, `routers/ri.py`; `services/email.py`
- `wsgi.py`, `parity_runner.py`, `requirements.txt` actualizados; `ARCHITECTURE.md` atualizado
- Verificação: `parity_runner.py` → **11/11 PASS**

### ✅ BACK-03 — ASCII enum values

- `dpiDefinitions.ts` + `Chichorro_DPI.py` + `parity_runner.py` + `schemas/cti.py` — sem `ç`/`ã` nos values de enum

---

## Concluído em 2026-05-13

### ✅ AUTH-09 / AUTH-09a / AUTH-09b / AUTH-09c — Perfil de Utilizador

- **AUTH-09** — 5 rotas backend: `/auth/profile/username`, `/auth/profile/email`, `/auth/profile/password`, `/auth/profile/delete`, `/auth/profile/avatar`; migração DB para colunas `avatar`, `new_email`, `new_email_token`
- **AUTH-09a** — ProfilePage: card layout com header gradient, accordion menu, ícones MDI
- **AUTH-09b** — Avatar: upload com canvas resize (256×256 JPEG 0.85), armazenamento em DB, sidebar actualizada
- **AUTH-09c** — ProfilePage redesign card compacto: 4 rows expansíveis inline (nome, e-mail, password, apagar conta); header com avatar + overlay de edição; sem "Zona de perigo"; sem botão "Sair"

### ✅ UI-06 — Página de Definições

- `src/lib/prefs.ts` — store localStorage com `Prefs` (theme, warnOnExit, decimalPlaces); `usePrefs()` hook reactivo; `applyTheme()` com suporte a "system"
- `SettingsPage.tsx` — 3 secções: Aparência (radio system/claro/escuro), Sessão (toggle avisar-antes-de-sair), Resultados (radio 2/3/4 casas decimais)
- `main.tsx` — aplica tema na inicialização; escuta mudanças do sistema e de `PREFS_CHANGED_EVENT`
- `tailwind.config.js` — `darkMode: "class"`; novas cores ink (400, 800, 950)
- `RiPage.tsx` e `CtiPage.tsx` — usam `getPrefs().decimalPlaces` em todos os `toFixed()`

### ✅ UI-07 — Dark Mode (concluído 2026-05-18)

Todas as páginas cobertas: sidebar, POI/DPI/ESCI cards, ProfilePage, SettingsPage, RiPage, CtiPage, InterventionsPage, páginas de autenticação, PasswordInput.

---

## Pendente — Prioridade Média

### UI-02 — Página de Documentação

Página de DOCS integrada na app com documentação e manuais de utilização.

### UI-03 — Página de Ajuda

Página HELP integrada na app.

### UI-04 — FAQs

Página de perguntas frequentes integrada na app.

### UI-05 — Bug Report

Formulário de reporte de bugs na app. Canal de destino a definir: e-mail, GitHub Issues ou ClickUp.

### UI-08 — Ícones de informação nos subfatores

Ícone ℹ️ em cada subfator POI/CTI/DPI/ESCI. Ao clicar, abre painel com descrição detalhada do subfator — o que mede, que valores esperar, como interpretar — incluindo tabela de valores e referência ao RT-SCIE quando aplicável. Exemplo: POI_IA com Quadro 3.3 (Centrais Térmicas, Aparelhos Autónomos, Combustível Sólido × Legislação).

---

### AUTH-09d — Otimização do avatar: WebP, 128 px, limite 100 KB

Avatar guardado como base64 JPEG 256×256 q0.85 (até 700 KB/utilizador). Com escala de
utilizadores, o tamanho acumulado na coluna `users.avatar` pode exceder o limite free do
Supabase (500 MB). Reduzir para WebP 128×128 q0.80 e limite de 100 KB — redução estimada
de ~80% no armazenamento, sem perda de qualidade percetível a esta dimensão.

Ficheiros: `app/frontend/src/pages/ProfilePage.tsx`, `app/backend/routers/auth.py`.
Ver plano detalhado em [AUTH-09d.md](plans/subplans/AUTH-09d.md).

---

### UI-09 — Badge de lápis persistente no avatar

O ícone de câmara no avatar só é visível no hover — invisível em dispositivos móveis.
Substituir por um badge circular persistente com ícone de lápis (`mdiPencil`) no canto
inferior-direito, sempre visível, seguindo o padrão Gmail/LinkedIn.

Ficheiro: `app/frontend/src/pages/ProfilePage.tsx`.
Ver plano detalhado em [UI-09.md](plans/subplans/UI-09.md).

---

## Pendente — Prioridade Baixa / Futuro

### ✅ INFRA-03 — Dockerfile + Compose (`3.1-dev`, 2026-06-09)

Dockerfile Python 3.14-slim + docker-compose.yml (backend + PostgreSQL 16); appuser não-root.

### FEAT-01 — Gráfico de Impacto de Intervenções

Tornado chart (bar chart horizontal) no módulo de Intervenções: impacto individual de cada intervenção selecionada.

- Backend: novo endpoint `POST /RI/interv/impact`
- Frontend: Recharts (já disponível)
- Custo: ~34 cálculos de RI por chamada (aceitável)

### FEAT-02 — Guardar Edifício

Após cálculo completo, guardar a avaliação associada a um edifício:

- Nome do projeto, morada, código postal (XXXX-XXX)
- Distrito / Concelho / Freguesia (dropdowns em cascata; inclui Regiões Autónomas)
- Latitude / Longitude + pin no mapa

Resultados (POI, CTI, DPI, ESCI, RI) ficam guardados por utilizador e em tabela geral na base de dados.

### FEAT-03 — Chatbot AI

Assistente de IA para ajudar os utilizadores a compreender o CHICHORRO e a usar a aplicação (Claude API ou similar).

### ✅ TEST-02 — Testes Automatizados (concluído 2026-05-27)

12/12 testes pytest passam. Cobre health, Literal 422, cálculo válido e auth básico. Ver secção acima.

### ✅ INFRA-02 — Pipeline CI/CD (concluído 2026-05-27)

GitHub Actions: `test.yml` (Python 3.12 + pytest) e `build.yml` (Node 20 + npm build), ambos com path filters. Ver secção acima.

---

## Backlog — Versão Futura (pós-3.1)

Propostas de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1:

| ID | Descrição |
| --- | --- |
| MODEL-01 | Método simplificado baseado no CHICHORRO 2.0 |
| MODEL-02 | Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo) |
| MODEL-03 | Afinação de custos €/m² via PRONIC |
| MODEL-04 | Intervenções adicionais: Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa |
| MODEL-05 | Georreferenciação e base de dados de edifícios |
| MODEL-06 | Tratamento de edifícios devolutos |
| MODEL-07 | Integração com Firecheck 2.0 |
