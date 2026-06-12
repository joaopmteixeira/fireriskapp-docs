# Changelog

---

## [v3.1.0] — 2026-06-12

Release baseline do CHICHORRO 3.1. Snapshot estavel antes de avançar para infraestrutura self-hosted (INFRA-07, DB-07/08).

### Funcionalidades principais

**Modelo CHICHORRO 3.1**

- CTI — `VHE_Dispositivos`/`VVE_Dispositivos` distintos por cenario
- DPI_OGS — 7→4 campos reformulados
- ESCI_GP — deteção automatica; ESCI_EXT — campo Formação; ESCI_RIA+CS — campos Formação e CS
- RI — escala de 12 classes (A++ a F); aceitabilidade por `POI_CC_Idade` (RI_RIA)
- Intervencoes — 34 ativas/passivas + conjuntos predefinidos + custo €/m²

**Autenticação e sessoes** (AUTH-01..13)

- Registo com verificação de e-mail (Resend); recuperação de palavra-passe
- Perfil de utilizador com avatar WebP 128 px; pagina de definicoes (dark mode, casas decimais)
- CSRF protection (starlette-csrf); sessoes com expiração configuravel (8 h)
- Sistema de roles: `engineer` (padrao) e `admin`; paginas AdminUsers e AdminLog

**Segurança** (SEC-01..10, AUTH-06..08)

- Argon2id (RFC 9106 level 1); SHA-256 em tokens de reset/verificação
- CORS estrito, HTTPS obrigatorio, security headers (CSP, HSTS, X-Frame-Options)
- Rate limiting via slowapi + Upstash Redis; fail-fast de secrets em producao
- Pydantic `Literal` em todos os schemas de calculo (422 em payloads invalidos)

**Backend** (BACK-01..07)

- Migracao Flask → FastAPI com routers modulares; SQLAlchemy 2.x ORM
- Alembic migrations (4 versoes); dual-mode SQLite (dev) / PostgreSQL (producao)
- Error handler JSON normalizado (5xx retorna `{"error":"INTERNAL_ERROR","request_id":...}`)

**Infraestrutura** (INFRA-01..07, DB-01..06)

- Deploy: Cloudflare Pages (frontend) + Render (backend) + Supabase PostgreSQL
- Sentry frontend + backend + Session Replay em erros; UptimeRobot a 5 min
- Backups JSON via GitHub Actions (a cada 3 dias, artifact 90 dias)
- GitHub Actions CI/CD: `test.yml` (Python 3.12, pytest) + `build.yml` (Node 20)
- Docker: Dockerfile Python 3.12-slim + docker-compose; staging Proxmox/Debian 13 operacional

**Documentacao e AI tooling**

- VitePress em `docs.chichorrofireriskapp.joaopmteixeira.net`
- Graphify: 740 nos / 1657 arestas / 44 comunidades (backend + frontend + cross-stack)
- Obsidian vault: 50 notas, 27 subfatores × 8 fontes, RT-SCIE 135/2020

---

## 2026-06-12 — AUTH-09d avatar WebP 128 px + migração de existentes

### perf(auth): optimize avatar to WebP 128px, 100 KB limit + migration script — AUTH-09d

- `app/frontend/src/pages/ProfilePage.tsx` — `resizeToDataUrl` default `maxPx` 256→128; `toDataURL` JPEG q0.85→WebP q0.80; chamada com argumento explícito removida; mensagem `AVATAR_TOO_LARGE` atualizada para 100 KB
- `app/backend/routers/auth.py` — `_AVATAR_MAX_BYTES` 700 000→100 000
- `scripts/migrate_avatars_to_webp.py` — script one-shot para converter avatares JPEG/PNG/GIF existentes para WebP 128 px (skip se já WebP; suporte --dry-run)
- `scripts/requirements-scripts.txt` — `Pillow>=10.0,<11` adicionado
- `docs/plans/subplans/AUTH/AUTH-09d.md` — marcado concluído

---

## 2026-06-11 — INFRA-03 verificacao + INFRA-06 env + deploy Proxmox

### feat(infra): verify INFRA-03 — Python 3.12, split dev deps, 342 tests [INFRA-03] *(commit `237cc51`)*

- `Dockerfile` — Python 3.14-slim → Python 3.12-slim (imagem estavel)
- `app/backend/requirements-dev.txt` — criado com pytest + pytest-cov; removidos de requirements.txt
- `app/backend/requirements.txt` — dependencias de producao apenas
- `scripts/requirements-scripts.txt` — criado com pypdf; docling comentado (opcional, ~2 GB)
- `.github/workflows/test.yml` — Python 3.12
- `docs/plans/subplans/INFRA/INFRA-03.md` — resumo de verificacao: /health OK, /health/db OK, 342 testes, imagem 526 MB

### feat(infra): add .env setup + Proxmox deploy guide — INFRA-06 [INFRA-06] *(commits `459839e`, `80f10e3`)* *(branch original: feat/infra07-env-proxmox)*

- `.env.example` — template com todas as variaveis documentadas (commitado; .env gitignored)
- `docker-compose.yml` — `env_file` com `required: false` (CI-safe)
- `docs/deploy/DEPLOY_PROXMOX_DEBIAN.md` — guia Docker Debian 13: instalacao, clone, .env, arranque, acesso
- `docs/plans/subplans/INFRA/INFRA-06.md` — subplan criado e fechado
- Deploy verificado em chichorro-staging (VM Proxmox Debian 13, 192.168.0.7): /health OK, /health/db OK, calculo OK

---

## 2026-06-09 — DB-06 SQLAlchemy ORM + INFRA-03 Docker

### refactor(db): migrate to SQLAlchemy 2.x ORM — DB-06 *(commits `04447d9`, `2ab2556`, `efade57`, `3979f15`)*

- `app/backend/models.py` — DeclarativeBase + `User` + `AccessLog` com `Mapped`/`mapped_column` (SQLAlchemy 2.x)
- `app/backend/database.py` — engine com `NullPool` (Neon PgBouncer); `get_db()` context manager; `migrate_sqlite()` por coluna com `try/except`; WAL pragma listener no connect event
- `app/backend/routers/auth.py` — F1: `IntegrityError` → 409 no registo; F2: guard `target=None` → 401; F3: guard `row.new_email=None` no verify-email-change
- `app/backend/routers/admin.py` — F5: projecao de colunas com `select()`, sem `avatar`/`hash` em `admin_users`
- `app/backend/alembic/env.py` — integrado com `Base.metadata` do SQLAlchemy
- `docs/plans/subplans/DB/DB-06.md` — estado `Concluido`, resumo de implementacao + F1-F6
- `docs/TODO_LIST.md`, `docs/TODO_PRIORITIES.md`, `docs/NEXT_STEPS.md` — DB-06 marcado como concluido

### feat(infra): add Dockerfile + docker-compose — INFRA-03 *(commits `c399f1e`, `d8d5e6e`)*

- `Dockerfile` — imagem Python 3.14-slim, gunicorn + uvicorn workers, utilizador nao-root `appuser`
- `docker-compose.yml` — servicos `backend` + `db` (PostgreSQL 16), volumes e env vars
- `.dockerignore` — exclui `__pycache__`, `*.pyc`, `.env`, `docs/`
- `docs/plans/subplans/INFRA/INFRA-03.md` — subplan criado

---

## 2026-06-08 — Planeamento VPS + gestao de tarefas

### docs(planning): create ROADMAP_SELF_HOSTED_VPS.md *(commit `7b3f78a`)*

- `docs/plans/main/ROADMAP_SELF_HOSTED_VPS.md` — roadmap de 12 fases para migracao Render+Supabase para VPS auto-alojado; novos IDs: REL-01, INFRA-06, DB-07, DB-08, SEC-11, SEC-12, INFRA-08, TEST-04

### docs(todos): add AI-03 + prefix legend + reorganize priorities *(commits `c033951`, `2e87c98`, `cf9f09e`, `b02527c`)*

- `docs/TODO_LIST.md` — AI-03 adicionado; seccao "Prefixos de ID" com 13 definicoes; FEAT-04 verificado
- `docs/TODO_PRIORITIES.md` — DB-06 + INFRA-03 para Prioridade Alta; AI-03 para Prioridade Media; AI-01 em Prioridade Baixa; "Concluidos Recentemente" condensados para 1-2 linhas; FEAT-04 em Futuro

---

## 2026-06-05 — AI-02 encerrado + merge feat/obsidian-vault → 3.1-dev

### docs(brain): mark AI-02 complete — Passo 8 results *(commit `4268b6a`, `feat/obsidian-vault`)*

- `docs/plans/subplans/AI/AI-02.md` — estado `✅ Concluído`, data `2026-06-05`, Passo 8 documentado com tabela de resultados (7 fontes × subfatores)
- `docs/TODO_PRIORITIES.md` — entrada AI-02 atualizada com RT-SCIE 135/2020 + Backend/Frontend

### docs: incorporate PR #2 and PR #4 into feat/obsidian-vault *(commits `9e47b8f`, `f0a1a8b`)*

- `docs/plans/subplans/AUTH/AUTH-09d.md` — otimização avatar: WebP 128 px, limite 100 KB, redução ~80% armazenamento
- `docs/plans/subplans/UI/UI-09.md` — badge lápis persistente no avatar (substitui overlay câmara hover-only)
- `docs/deploy/VPS_CONSOLIDATION.md` — guia de referência para migração para VPS única (Hetzner CX32 ~€6.80/mês)
- `docs/NEXT_STEPS.md`, `docs/TODO_LIST.md`, `docs/TODO_PRIORITIES.md` — AUTH-09d, UI-09, UI-10 adicionados como ❌ Prioridade Média
- PRs #2 e #4 fechados no GitHub (incorporados manualmente)

### docs(brain): add AI-02a subplan *(commit `d32bf38`, `feat/obsidian-vault`)*

- `docs/plans/subplans/AI/AI-02a.md` — 3 tarefas manuais residuais do AI-02: (1) preencher `## Definicao` nas 27 notas de subfator; (2) validar entradas "verificar" em `## Onde e mencionado`; (3) verificar Graph View Obsidian
- `docs/TODO_LIST.md` — secção AI com AI-02a ❌ adicionada
- `docs/TODO_PRIORITIES.md` — AI-02a em Prioridade Baixa

### merge(feat/obsidian-vault): AI-02 Obsidian vault + RT-SCIE 135/2020 *(commit `a14c1f5`, `3.1-dev`)*

- 35 commits de `feat/obsidian-vault` mergeados em `3.1-dev` com `--no-ff`
- Push para `origin/3.1-dev` (`3a2f190..a14c1f5`)

---

## 2026-06-02 — AI-02 · pipeline investigação + vault Obsidian CHICHORRO

### feat(regulations): add RT-SCIE Portaria 1532/2008 *(commit `7fbe5aa`, `feat/research-organization`)*

- `docs/regulations/Portaria-1532_2008/` — PDF original, 309 artigos em `articles/art_*.md` com frontmatter YAML (título, epígrafe, página, artigo)
- `docs/regulations/_pipeline/` — scripts genéricos `convert.py`, `split.py`, `worker.py`; novo regulamento adicionado via `config.json` sem duplicar scripts

### feat(ai): add chichorro-registry.json — fonte única de verdade *(commit `d909d27`, `feat/research-organization`)*

- `docs/vault/_data/chichorro-registry.json` — 5 fatores, 27 subfatores com `calc_linha`/`frontend_linha`, 9 fontes
- Referências de código verificadas a 2026-06-01 (backend + frontend)

### docs(research): pipeline de conversão de dissertações com docling *(commits `5c84e5f`, `68c6b7f`)*

- `scripts/thesis_convert.py` — orquestrador: chunks de 12 páginas → `.ai.md` + `.chunks.jsonl` com marcadores `<!-- page: N -->`
- `scripts/thesis_worker.py` — worker por chunk (paramétrico, aceita `pdf_path`)
- Tese 4.0 IC (366 págs, 112 chunks), Tese 3.0 JPT (250 págs, 194 chunks), Tese 3.1 RS (140 págs, 104 chunks) convertidas

### feat(scripts): add map_sources.py — heading-aware subfactor source mapper *(commit `8fc1429`)*

- `scripts/map_sources.py` — percorre `.ai.md` com `heading_stack` + `current_page`; popula `## Onde e mencionado` com subcapítulo + página; cria `[[art_xxx_...|Artigo N - epígrafe]]` para o RT-SCIE
- 27 notas de subfatores preenchidas com referências das 3 teses + artigos RT-SCIE

### feat(ai): add build_vault.py + generate Obsidian vault (48 notes) *(commit `68f1c1f`, `feat/obsidian-vault`)*

- `scripts/build_vault.py` — idempotente; lê `chichorro-registry.json`; gera 5 fatores, 27 subfatores, 9 fontes, 6 conceitos, `Indice.md`; frontmatter YAML + `[[wiki-links]]`; flag `--force`
- `docs/vault/fatores/`, `subfatores/`, `fontes/`, `conceitos/`, `Indice.md` — 48 notas geradas

### docs(ai): expand vault root to docs/ — thesis .ai.md files accessible *(commit `1c805e3`, `feat/obsidian-vault`)*

- Vault root movido de `docs/vault/` para `docs/` — teses `.ai.md` e artigos RT-SCIE ficam acessíveis no Obsidian
- Notas fonte das 3 teses com `[[tese3.0.ai|Abrir conteudo]]` para navegação directa
- Links `[[art_xxx_...]]` resolvem agora (deixam de ser órfãos no Graph View)
- `.gitignore`: `docs/.obsidian/` e `docs/vault/.obsidian/` ambos ignorados

---

## 2026-06-01 — AI-01 · setup Graphify (execução) + AI strategy formalizada

### feat(ai): install Graphify + generate cross-stack knowledge graph *(AI-01 / FIR-34)*

- Graphify instalado (manual — auto-installer bloqueado por classificador supply chain)
- Grafos gerados: backend (367 nós), frontend (346 nós), cross-stack (740 nós / 1657 arestas / 44 comunidades)
- God nodes: `_get_db()` (21 arestas), `getAppStorage()` (24), `Request` (20)
- Hyperedges: pipeline RI = f(POI,CTI,DPI,ESCI); factor definitions; session state via `resultsStore`; auth flow; parity test suite
- `CLAUDE.md` criado na raiz (gitignored): mapa rápido arquitetura, comandos de dev, regras de refresh do grafo
- `.gitignore` expandido: `graphify-out/`, `graph.html`, `graph.json`, `GRAPH_REPORT.md`, `.graphify/`, `docs/vault/`

### docs(ai): AI strategy + AI-02 handoff *(commits `087e387`, `19da190`)*

- `HANDOFF_OBSIDIAN_VAULT.md` — handoff detalhado para AI-02: estrutura do vault (5 fatores, 27 subfatores, 9 fontes), scripts necessários, schema YAML frontmatter
- `docs/TODO_LIST.md` — secção "AI Tooling" adicionada: AI-01 ✅, AI-02 ❌, AI-03 🔮
- `docs/TODO_PRIORITIES.md` — prefixo AI adicionado; AI-01 marcado concluído
- `docs/plans/subplans/AI/AI-01.md` — subplan com stats do grafo, god nodes, hyperedges, referências FIR-34/FIR-35

---

## 2026-05-31 — docs(ai) · estratégia IA documentada

### docs(ai): add Graphify setup, Obsidian vault guide and RAG future plan *(commit `2bd5607`)*

- `docs/ai/SETUP_GRAPHIFY.md` — guia completo de instalação Graphify: passos, blocos CLAUDE.md, adições .gitignore, regras de refresh (quando correr vs. não)
- `docs/ai/OBSIDIAN_SETUP.md` — estrutura do vault com subfactores reais CHICHORRO (POI_CC, POI_IEE, DPI_REIC, ESCI_GP, etc.), passos de conversão PDF, lista plugins
- `docs/research/RAG_FUTURE.md` — arquitetura para assistente RAG futuro com pgvector + Claude API; a implementar após validação do Obsidian

---

## 2026-05-29 — fix(poi) · chore · refactor(repo) · refactor(docs) · fix(repo)

### fix(poi): TipoEdif2 — tipo pai como primeira opção *(commit `6128086`, `3.1-dev`)*

- `app/backend/schemas/poi.py` — valores pai (`Industria`, `Oficinas`, `Desporto`) adicionados como primeira opção em `POI_ATIV_TipoEdif2` nos schemas `POIATIVRequest` e `POIRequest`; backend `else` clauses já devolviam os valores pai corretos
- `app/frontend/src/components/poi/poiDefinitions.ts` — tipo pai adicionado como primeira entrada em cada grupo `TipoEdif2`; desbloqueia cálculo POI ATIV quando não é necessário subtipo
- `docs/deploy/DEPLOY.md` — secção de dev local atualizada: flag `--hot-reload` e nota de fallback SQLite auto

### chore: excluir tabelas de investigação do repositório *(commit `d3adf1a`, `3.1-dev`)*

- `docs/research/tables/` adicionado ao `.gitignore`; 5 ficheiros Excel removidos do índice git (FATORES, JP_CTI, JP_DPI, JP_ESCI, JP_POI)

### docs(todo): adicionar UI-08 *(commit `6b64e2a`, `3.1-dev`)*

- `docs/NEXT_STEPS.md`, `docs/TODO_LIST.md`, `docs/TODO_PRIORITIES.md` — UI-08 (ícones de informação nos subfatores) adicionado como tarefa pendente de prioridade média

### refactor(repo): reorganização da raiz *(commit `8bf3933`, `3.1-dev`)*

- `server/` dissolvido — `security_audit_plans/` (13 .md) → `docs/audits/security/`; `cloud_vps_audit_plans/` (43 .md) → `docs/audits/cloud-vps/`; `HANDOFF_*.md` (2) → `docs/ai/handoffs/`; `server/README.md` eliminado
- `tools/` → `scripts/` via `git mv` (histórico preservado); `.gitignore` atualizado: `tools/*` → `scripts/*` com mesmas exceções
- `sessions/` → `var/sessions/`; `.gitignore` atualizado: `sessions/` → `var/`
- `deploy/` reestruturado: `env.*.example` → `deploy/env/`; `nginx-chichorro.example.conf` → `deploy/nginx/`
- `docs/guides/TOOLS.md`, `docs/deploy/DEPLOY.md`, `docs/README.md` atualizados com novos paths
- `README.md` criado na raiz: resumo do projeto, requisitos, comandos de desenvolvimento, links para docs

### refactor(docs): reorganização interna de docs/ *(commit `6d2093b`, `3.1-dev`)*

- 15 ficheiros movidos de `docs/` root para subdiretorias temáticas:
  - `docs/project/` (novo) — ARCHITECTURE, PRD, PROJECT_OVERVIEW, DESIGN, SERVICES, FRONTEND_UX_MODIFICATIONS
  - `docs/method/` (novo) — METODO_CALCULO
  - `docs/guides/` (novo) — USER_GUIDE, TOOLS + merge de `guidelines/` (BACKEND_GUIDELINES, FRONTEND_GUIDELINES)
  - `docs/deploy/` (existente) — HOSTING_OPTIONS adicionado
  - `docs/changelog/` (novo) — CHANGELOG, DECISIONS_LOG, HISTORY_AI
- `docs/guidelines/` eliminado (vazia após merge)
- `docs/.vitepress/config.ts` — todos os links de nav e sidebar atualizados para novos paths
- `docs/index.md`, `docs/README.md` — ~15 links relativos corrigidos
- Cross-refs internas em `PRD.md`, `SERVICES.md`, `BACKEND_GUIDELINES.md`, `FRONTEND_GUIDELINES.md` corrigidas

### fix(repo): cleanup pós-reorganização *(commit `9878f7e`, `3.1-dev`)*

- `README.md` (raiz) — 3 links quebrados corrigidos: `docs/project/`, `docs/method/`, `docs/guides/`
- `.gitignore` — `!scripts/restore_db.py` adicionado como tracked; bloco de comentários de política de tracking adicionado
- `docs/audits/cloud-vps/README.md` — nota de path histórico: referência a `server/cloud_vps_audit_plans/` para contexto
- `scripts/restore_db.py` — passado a tracked (estava sem seguimento apesar de não ignorado)

---

## 2026-05-28 — SEC-04b · DOCS-02 · session-remount · POI conditional fields

### SEC-04b — Remoção do fallback werkzeug *(commit direto `3.1-dev`)*

- `app/backend/routers/auth.py` — `_verify_password` simplificada: apenas `_PH.verify` (argon2id); bloco werkzeug e upgrade-on-login removidos
- `app/backend/requirements.txt` — `werkzeug>=3.0,<4` removido
- `docs/plans/subplans/SEC/SEC-04.md` — secção SEC-04b adicionada com data/branch

### DOCS-02 — Uniformização headers dos subplans *(commit direto `3.1-dev`)*

- 58 ficheiros `docs/plans/subplans/` — formato canónico `Estado → Data de conclusão → Branch`; YAML frontmatter, datas inline no H1 e campos `**Data:**` removidos
- `docs/plans/subplans/DESIGN.md` — eliminado (duplicado de `docs/DESIGN.md`, 753 linhas)
- `docs/TODO_PRIORITIES.md` — bloco ❌ SEC-09 duplicado removido; INFRA-04 corrigido de ❌ para ✅

### fix(frontend): session remount *(commit `da8c6fe`)*

- `app/frontend/src/pages/AppLayout.tsx` — `key={sessionKey}` no `<Outlet>` forçava remount completo ao importar/limpar sessão; páginas passam a reflectir novo estado imediatamente

### fix(poi): campos condicionais — dois commits *(commits `81ba110` + `c2dc0ab`)*

- `app/backend/schemas/poi.py` — `POI_IA_TipoInst2` e `POI_ATIV_TipoEdif2` tornados `Optional[Literal[...]] = None` nos 3 modelos (`POIIARequest`, `POIATIVRequest`, `POIRequest`)
- `app/frontend/src/components/poi/PoiFactorSection.tsx` — payload filtrado por `opts.length > 0` (excluir campos getOptions sem opções; manter campos estáticos com visibleWhen); pré-actualização de module inputs CTI+POI antes do `setValues` quando muda `POI_ATIV_TipoEdif`
- `app/frontend/src/pages/CtiPage.tsx` — `disabled={isTipoEdifSynced}` removido do campo TipoEdif; pré-actualização simétrica de module inputs ao mudar TipoEdif no CTI; sync bidirecional CTI↔ATIV funcional

### test: verificador de paridade + cobertura de Literals *(commit `d6a22cc`)*

- `tools/check_option_parity.py` — verificador estático frontend↔backend: lê schemas Pydantic (`Literal` types) e compara com os `*Definitions.ts` do frontend; saída `[OK]`/`[FAIL]`/`[WARN]`; exit code 1 em divergências (CI-friendly); detetou 2 bugs reais (POI_CC_Idade espaços, DPI_OGS_Aplica phantom)
- `app/backend/tests/test_valid_options.py` — 338 testes parametrizados auto-gerados de todos os schemas Pydantic; cobre cada valor `Literal` de cada campo de cada subfator; usa endpoints individuais (`/POI/IA`, etc.) para evitar TypeError no endpoint combinado
- `.gitignore` — excepção `!tools/check_option_parity.py` adicionada à regra `tools/*`

### fix(schemas): POI_CC_Idade e DPI_OGS_Aplica *(commit `6d85d77`)*

- `app/backend/schemas/poi.py` — `POI_CC_Idade` corrigido em `POICCRequest` e `POIRequest`: intervalos sem espaços (`"1991-2008"` em vez de `"1991 - 2008"`)
- `app/backend/schemas/dpi.py` — `DPI_OGS_Aplica` corrigido em `DPIOGSRequest` e `DPIRequest`: `"Nao Existe"` removido (phantom — não consta da tabela do modelo, nunca oferecido pelo frontend, sempre causaria ERRO no cálculo)
- `app/backend/calc/Chichorro_POI.py` — comentário `POI_CC_Idade` atualizado para refletir formato sem espaços

### plan: CALC_AUDIT — plano de validação do código contra a tese3.1

- `docs/plans/main/CALC_AUDIT.md` criado — plano para criar ~280 golden tests que validam cada célula das tabelas de lookup POI/DPI/ESCI/CTI contra a dissertação 3.1; bloqueado até o utilizador criar os Excel da tese3.1

---

## 2026-05-27 — audit-fix-3 · SEC-04 · SEC-05 · SEC-07 · BACK-05 · BACK-06 · BACK-05d · TEST-02 · INFRA-02

### audit-fix-3 — Gaps Codex post-review *(branch `audit-fix-3`)*

- `app/backend/database.py` — coluna `users.role` adicionada ao path SQLite `init_db()` (estava ausente após AUTH-10)
- `app/backend/config.py` — validação do username na `DATABASE_URL` alargada para suportar o formato Supabase `username.project_ref`; fail-fast em produção mantido
- `app/frontend/vite.config.ts` — prefixo `/admin` adicionado ao proxy de desenvolvimento (faltava após BACK-07)
- `tools/backup_db.py` — sincronizado com `.github/scripts/backup_db.py`: descoberta de PK via `information_schema` e `psycopg2.sql.Identifier`
- `docs/` — contradições pós-audit-fix-2 corrigidas
- `.gitignore` — regra `tools/*` com excepção explícita para `backup_db.py`; `tools/backups/` mantido

### SEC-04 — Argon2id password hashing *(branch `sec/hardening`)*

- `app/backend/routers/auth.py` — `argon2-cffi` substitui werkzeug PBKDF2/scrypt; `_PH = PasswordHasher()` (RFC 9106 level 1: m=65536, t=3, p=4)
- `_verify_password`: positivo em `$argon2id`, fallback werkzeug para hashes legados (scrypt/pbkdf2)
- Upgrade-on-login: após autenticação com hash não-argon2, re-hash atómico e UPDATE na BD
- `requirements.txt`: `argon2-cffi>=23.1,<25` adicionado

### SEC-07 — Validação magic bytes no avatar *(branch `sec/hardening`)*

- `app/backend/routers/auth.py` — `_check_avatar_magic()` decodifica os primeiros 12 bytes base64 e valida assinatura: JPEG `\xff\xd8\xff`, PNG `\x89PNG`, WebP `RIFF…WEBP`, GIF `GIF8`/`GIF9`
- SVG e qualquer tipo fora da lista rejeitados com HTTP 400
- `docs/plans/subplans/SEC/SEC-04.md` e `SEC-07.md` actualizados

### SEC-05 — SHA-256 dos tokens de verificação/reset/email-change *(branch `sec/token-hashing`)*

- `app/backend/routers/auth.py` — `_hash_token(token)` → `hashlib.sha256(token.encode()).hexdigest()`
- 3 stores (register, forgot-password, profile/email-change) guardam o hash; token em claro apenas no e-mail/URL
- 3 lookups (verify, reset-password, verify-email-change) fazem `WHERE` pelo hash
- `app/backend/main.py` — `/auth/register`, `/auth/forgot-password`, `/auth/reset-password` adicionados a `_CSRF_EXEMPT`
- `docs/plans/subplans/SEC/SEC-05.md` actualizado

### BACK-05 — Pydantic Literal types em dpi, esci, cti *(branch `back/validation`)*

- `schemas/dpi.py` — 23 campos `str` → `Literal` (valores de `Chichorro_DPI.py`)
- `schemas/esci.py` — 23 campos `str` → `Literal` (valores de `Chichorro_ESCI.py`)
- `schemas/cti.py` — 13 campos `str` → `Literal`; aliases `_DISPOSITIVOS`/`_REACAO_FOGO`; `model_validator(mode="before")` preservado; Literal usa valores pós-normalização
- `sessions/*.json` actualizados para conformidade (campos obrigatórios em falta, `ç`→`c`)

### BACK-06 — Error handler JSON normalizado *(branch `back/validation`)*

- `app/backend/main.py` — `unhandled_exception_handler` retorna `JSONResponse({"error":"INTERNAL_ERROR","request_id":...}, 500)` em vez de re-raise
- `HTTPException` continua a ser re-lançada (FastAPI trata nativamente)
- `docs/plans/subplans/BACK/BACK-05.md` e `BACK-06.md` criados

### BACK-05d — Pydantic Literal types em poi.py *(branch `back/validation`)*

- `app/backend/schemas/poi.py` — 49 campos `str` livres → `Literal[...]` em 12 sub-modelos + `POIRequest`
- Import `from typing import Literal`; sem `model_validator` (valores literais directos das condicionais de `Chichorro_POI.py`)
- `POI_ATIV_TipoEdif2`: union flat de 19 valores (dependência runtime não suportada por Literal cruzado)
- `docs/plans/subplans/BACK/BACK-05.md` actualizado com secção BACK-05d
- Validado: `POICCRequest(POI_CC_Comb="Talvez", ...)` → `ValidationError: literal_error` ✅

### TEST-02 — Infraestrutura pytest *(branch `test/automated-tests`)*

- `pytest>=8.0,<9` e `pytest-cov>=5.0,<6` adicionados a `requirements.txt`
- `app/backend/pytest.ini` — `testpaths = tests`
- `app/backend/tests/conftest.py` — override `require_auth` + seed CSRF cookie + fixtures de payload (DPI/ESCI/CTI/POI do `parity_runner.py`)
- `tests/test_health.py` — GET /health e GET /health/db
- `tests/test_literals.py` — POST com campo Literal inválido → 422; auth login sem body → 422; credenciais inválidas → 401
- `tests/test_calc.py` — POST com payload válido → 200 + resultado `0 < x ≤ 5`
- **12/12 testes passam** em 0.22s ✅

### INFRA-02 — GitHub Actions CI/CD *(branch `infra/ci-cd`)*

- `.github/workflows/test.yml` — Python 3.12, `pytest -v --cov`, activa em `app/backend/**`
- `.github/workflows/build.yml` — Node 20, `npm ci && npm run build`, activa em `app/frontend/**`
- Path filters: sem runs desnecessários em alterações de docs ou outro subprojeto

---

## audit-fix-2 — Codex findings #2-7 (2026-05-26)

Branch criada a partir de `auth/roles` (via `3.1-dev`). Corrige os 6 findings pendentes da revisão Codex.

### Finding #2 — Validação positiva `https://` *(commit `24e0cdd`)*

- `app/backend/config.py` — substituído `startswith("http://")` por `_require_https_url()` via `urlparse`; rejeita `ftp://`, URLs sem esquema, protocol-relative; aplicado a `FRONTEND_URL`, `BACKEND_URL` e cada CORS origin

### Finding #3 — `DATABASE_URL_MIGRATIONS` fail-fast em produção *(commit `4b027ce`)*

- `app/backend/config.py` — `validate_production_urls` exige `DATABASE_URL_MIGRATIONS` definida em `ENV=production`
- `app/backend/alembic/env.py` — eliminado fallback silencioso; `RuntimeError` explícito se ausente em produção

### Finding #4 — Role read-only para backup *(commit `3307b0a`)*

- `.github/workflows/backup-db.yml` — usa `DATABASE_URL_BACKUP` em vez de `DATABASE_URL` (chichorro_runtime)
- `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md` — nova secção "Supabase — Utilizador de backup com SELECT (A-04)" com SQL de criação do role `chichorro_backup` e checklist; secção GitHub Secrets atualizada para `DATABASE_URL_BACKUP`

### Finding #5 — Backup robusto sem coluna `id` *(commit `bd5b6a3`)*

- `.github/scripts/backup_db.py` — `get_pk_columns()` via `information_schema`; `export_table()` usa `psycopg2.sql.Identifier` em vez de f-string com ORDER BY id fixo

### Finding #6 — README frontend: remover `VITE_LOGIN_*` *(commit `7fb926e`)*

- `app/frontend/README.md` — removidas referências a `VITE_LOGIN_USER_N`/`VITE_LOGIN_PASS_N`; secção "Autenticação" reescrita; env var corrigida para `VITE_API_BASE_URL`

### Finding #7 — CSP: endpoint Sentry EU *(commit `7707b28`)*

- `app/frontend/public/_headers` — `*.ingest.de.sentry.io` adicionado ao `connect-src`
- `app/backend/main.py` — mesmo fix no middleware `add_security_headers`

---

## auth/roles — AUTH-10: sistema de roles e UI admin (2026-05-26)

Branch criada a partir de `3.1-dev`. Merge `--no-ff` em `3.1-dev` em 2026-05-26.

### Codex security review — documentação *(commit `d88fac0`)*

- `server/cloud_vps_audit_plans/CODEX_REVIEW_BRIEF.md` — brief para revisão OpenAI Codex do ciclo audit-fix
- `server/cloud_vps_audit_plans/CODEX_REVIEW_FINDINGS_FOR_CLAUDE.md` — 6 findings do Codex (CRITICAL: `/admin/*` sem autorização; HIGH: validação https, DATABASE_URL_MIGRATIONS; MEDIUM: backup sensível, backup sem `id`; LOW: README VITE_LOGIN_*)
- `server/cloud_vps_audit_plans/CODEX_REVIEW_ANALYSIS_CLAUDE.md` — análise Claude com concordância, ordem de correção, finding #7 (CSP bloqueia Sentry)

### AUTH-10 backend *(commit `f9af8d3`)*

- `app/backend/alembic/versions/0003_add_user_role.py` — migration: `ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'engineer'`
- `app/backend/deps.py` — `require_admin`: 401 se não autenticado, 403 se `chichorro_role != "admin"`
- `app/backend/routers/auth.py` — login env var define `session["chichorro_role"] = "admin"`; login DB lê `role` da BD; logout limpa `chichorro_role`; `/auth/me` devolve `role`
- `app/backend/routers/admin.py` — `require_auth` → `require_admin`; query de `/admin/users` inclui coluna `role`

### AUTH-10 frontend *(commits `4ffeab4`, `2d60de1`)*

- `app/frontend/src/auth/session.ts` — `saveRole(role)`, `getRole()`, `logout()` limpa `chichorro_role_v1`
- `app/frontend/src/pages/AppLayout.tsx` — `userRole` state; `/auth/me` guarda role; grupo ADMIN no fundo do sidebar (condicional, acima da secção do utilizador)
- `app/frontend/src/pages/AdminUsersPage.tsx` (NOVO) — tabela: username, email, verificado, role (badge colorido), criado em (YYYY-MM-DD HH:MM)
- `app/frontend/src/pages/AdminLogPage.tsx` (NOVO) — tabela: timestamp, username, evento, IP, user agent (truncado, limit 200)
- `app/frontend/src/App.tsx` — rotas `/app/admin/users` e `/app/admin/log`

### Documentação *(commits `04cee5c`, `37410f1`)*

- `docs/plans/subplans/AUTH/AUTH-10.md` — consolidado com toda a informação de implementação
- `server/cloud_vps_audit_plans/AUTH-10_CLAUDE.md` — removido (conteúdo integrado no subplan)
- Finding #7 (CSP Sentry) adicionado a `CODEX_REVIEW_ANALYSIS_CLAUDE.md`

---

## audit-fix — Ciclo de audit segurança cloud (2026-05-21)

### Auditoria de segurança cloud — planos C-01, C-04, M-05, C-02 *(21/05/2026)*

Branch `audit-fix` criada a partir de `c559e34` (base limpa). Todos os planos do ciclo de
audit Codex vão para esta branch única; merge em `3.1-dev` no final do ciclo completo.

#### Infraestrutura de audit — `server/`

- `server/cloud_vps_audit_plans/` — 16 planos de audit (C-01..04, A-01..06, M-01..05, B-01..02) com análise Codex + opinião técnica `_CLAUDE.md` + resumo de implementação
- `server/security_audit_plans/` — 12 fases de auditoria VPS (Proxmox/cloud) criadas pelo Codex
- `server/HANDOFF_FOR_CLAUDE.md`, `HANDOFF_TODO_COMPATIBILITY_FOR_CLAUDE.md`, `README.md` — documentação de handoff entre Codex e Claude
- `server/IMPLEMENTATION_PLAN_ORDER_CLAUDE.md` — ordem de implementação justificada dos 16 planos

#### C-01 — TLS end-to-end, fail-fast URLs produção (SEC-02) *(commit `a7ce7ca`)*

- `app/backend/config.py` — novos campos `env`, `frontend_url`, `backend_url`; `model_validator(mode="after")` fail-fast em produção: `FRONTEND_URL`/`BACKEND_URL` obrigatórias e `https://`; `app_base_url` overridden por `FRONTEND_URL` em produção
- `deploy/nginx-chichorro.example.conf` — comentários Flask→FastAPI; `X-Forwarded-Host $host` adicionado

#### C-04 — Fail-fast secrets em produção (SEC-10) *(commit `4dc1a02`)*

- `app/backend/config.py` — `validate_production_urls` estendido: `CHICHORRO_SECRET_KEY=dev-change-me` rejeita arranque; `DATABASE_URL`, `CHICHORRO_CORS_ORIGINS`, `UPSTASH_REDIS_URL`, `RESEND_API_KEY`, `MAIL_DEFAULT_SENDER` obrigatórias em produção
- `deploy/env.production.example` criado — referência de vars para dashboard Render
- `deploy/env.development.example` criado — referência de vars para dev local

#### M-05 — Remover credenciais frontend (SEC-08) *(commit `a5d29c5`)*

- `app/frontend/src/auth/legacyLogin.ts` eliminado — código morto (nunca importado); lia `VITE_LOGIN_USER_*`/`VITE_LOGIN_PASS_*` que ficavam em texto claro no bundle JS
- `app/frontend/.env` — `VITE_LOGIN_USER_1=admin`/`VITE_LOGIN_PASS_1=admin` removidos localmente (gitignored)
- Build frontend: 0 erros, 390 módulos

#### C-02 — Cookies Secure/SameSite + proxy headers (AUTH-06) *(commit `bf2f30f`)*

- `app/backend/config.py` — `field_validator("session_samesite")` restringe a `{"Lax", "Strict"}`
- `app/backend/wsgi.py` — start commands Render (`--proxy-headers --forwarded-allow-ips='*'`) e VPS documentados
- `deploy/env.production.example` — secção "Render start command" adicionada
- Nota: `ProxyHeadersMiddleware` removido no Starlette 1.0.0; abordagem correcta é uvicorn flags
- **Ação manual pendente:** atualizar Start Command no dashboard Render

#### `.gitignore` *(commit `bf2f30f`)*

- `app/backend/Python/` e `app/backend/python_install_*.log` excluídos (instalação local VS Code Python Install Manager)

### Auditoria de segurança cloud — planos A-01, A-06, A-02, M-01, M-02, A-03, A-05, A-04 *(22/05/2026)*

#### A-01 — CORS estrito em produção (SEC-01) *(commit `1410fe8`)*

- `app/backend/config.py` — 3 checks A-01 no `validate_production_urls`: rejeita `*` em qualquer CORS origin; rejeita origins com `http://`; rejeita se `FRONTEND_URL` não estiver incluída nas CORS origins
- `deploy/env.production.example` — comentário junto a `CHICHORRO_CORS_ORIGINS` com as regras A-01
- 5/5 testes de import Python aprovados

#### A-06 — Endpoint `/health/db` com query real à BD (INFRA-04) *(commit `c8178c4`)*

- `app/backend/main.py` — endpoint `GET/HEAD /health/db` com `SELECT 1`; HTTP 200/503 sem expor internos; adicionado a `_CSRF_EXEMPT`

#### A-02 — Fail-fast Redis no arranque (AUTH-07) *(commit `4eadb6d`)*

- `app/backend/main.py` — `_check_redis_startup()` no lifespan; pinga Redis em produção antes de aceitar requests (`socket_connect_timeout=5`); token nunca exposto nos logs
- `deploy/env.production.example` — comentário sobre TLS Redis e comportamento A-02

#### M-01 — CSP e Permissions-Policy (SEC-09) *(commit `b9425ed`)*

- `app/backend/main.py` — `Content-Security-Policy` e `Permissions-Policy` adicionados ao middleware `add_security_headers`; CSP cobre Google Fonts e Sentry ingest; sem `'unsafe-inline'`
- `app/frontend/public/_headers` — criado: headers Cloudflare Pages com `connect-src` para backend + HSTS `preload`

#### M-02 — Cache-Control no edge e backend (INFRA-05) *(commit `ae92698`)*

- `app/backend/main.py` — `Cache-Control: no-store` no middleware `add_security_headers`
- `app/frontend/public/_headers` — `no-store` em `/*`; `public, max-age=31536000, immutable` em `/assets/*`; assets Vite fingerprintados cacheados 1 ano de forma segura

#### A-03 — Migrations Alembic (DB-04) *(commit `eb65dbd`)*

- `app/backend/alembic.ini` + `app/backend/alembic/` criados: `env.py`, `script.py.mako`, `versions/0001_initial_schema.py`
- `alembic/env.py` — ligação psycopg2 via `settings.database_url`; falha com `RuntimeError` se `DATABASE_URL` não definida
- `alembic/versions/0001_initial_schema.py` — snapshot completo do schema atual (`access_log` + `users`); `IF NOT EXISTS` — idempotente na Supabase existente
- `app/backend/main.py` — `init_db()` guardado para dev SQLite; produção usa Alembic Release Command
- `requirements.txt` — `alembic>=1.13,<2` adicionado (instalado 1.18.4)
- **Ação pendente no Render:** Release Command → `cd app/backend && alembic upgrade head`

#### A-05 — Política de logs sem tokens/PII (SEC-06) *(commit `15ac08b`)*

- `app/backend/main.py` — `_TokenPathFilter` registado no `uvicorn.access` logger; substitui tokens em `/auth/verify/{token}` e `/auth/verify-email-change/{token}` por `[REDACTED]`
- `app/backend/services/email.py` — guard `env != "production"` nos `print()` (defesa em profundidade)

#### A-04 — Backups externos e restore (DB-03) *(commit `3dc2a8d`)*

- `.github/scripts/backup_db.py` — `TABLES` estático substituído por `discover_tables()` via `information_schema.tables`; `alembic_version` excluída
- `tools/restore_db.py` (local, gitignored) — restore de JSON com `--confirm` obrigatório; transação única; rollback automático em erro
- `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md` — renomeado de `docs/deploy/DEPLOY_RENDER_CLOUDFLARE.md`; secção GitHub Secrets adicionada (`DATABASE_URL` para `backup-db.yml`)
- `docs/plans/subplans/DB/DB-03.md` — secções de backup automático externo, descoberta dinâmica e restore completo adicionadas
- **Ação manual pendente:** secret `DATABASE_URL` em GitHub → Settings → Secrets → Actions

#### DB-06 — Backlog: SQLAlchemy ORM (decidido 2026-05-22)

- `docs/plans/subplans/DB-06_UNDONE.md` — subplan criado: comparação SQLAlchemy vs. psycopg2 puro, ficheiros afetados, estimativa de escopo (~300-400 linhas), dependências
- Decidido fora do escopo do audit; depende de DB-04 ou substitui-o

### Auditoria de segurança cloud — planos C-03, M-04, B-02, B-01 + merge final *(24/05/2026)*

#### C-03 — Least Privilege DB User (DB-05) *(commit `91443d1`)*

- `app/backend/alembic/env.py` — `DATABASE_URL_MIGRATIONS` tem prioridade sobre `DATABASE_URL` quando disponível; Alembic usa superuser (`postgres`) para migrations; runtime usa `chichorro_runtime` (só DML)
- `deploy/env.production.example` — `DATABASE_URL_MIGRATIONS` documentada com comentário explicativo
- `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md` — secção Supabase SQL completa: SQL para criar role `chichorro_runtime`, GRANTs mínimos (`SELECT`, `INSERT`, `UPDATE`, `DELETE` nas tabelas da app), ordem de atualização das env vars no Render
- **Ações manuais pendentes:** Supabase SQL Editor (criar role + GRANTs); Render (atualizar `DATABASE_URL` para porta 6543 + adicionar `DATABASE_URL_MIGRATIONS`); GitHub Actions (secret `DATABASE_URL` para `chichorro_runtime`)

#### M-04 — Observabilidade mínima (INFRA-01 extensão) *(commit `6c0c782`)*

- `app/backend/main.py` — middleware `add_request_id`: gera UUID4 por pedido antes do CSRF, expõe em `X-Request-ID` na resposta; tag `request_id` adicionada ao scope Sentry no exception handler para correlação de eventos
- `.github/workflows/backup-db.yml` — step `if: failure()` com notificação via Resend API para `eng.joao.pm.teixeira@gmail.com`; inclui link direto para o run falhado; token `RESEND_API_KEY` necessário como GitHub Secret
- **Ações manuais pendentes:** UptimeRobot monitor HTTP para `/health/db` (5 min); Sentry alert rule > 10 eventos/1h → e-mail; `RESEND_API_KEY` em GitHub Secrets

#### B-02 — Naming de rotas API (BACK-07) *(commit `ecc7149`)*

- `app/backend/routers/auth.py` — aliases legacy removidos: `POST /login`, `POST /logout`, `GET /me` (dead code — frontend usa exclusivamente `/auth/*`)
- `app/backend/routers/ri.py` — `@router.post("/RI_interv")` removido; rota canónica `/RI/interv` mantida
- `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md` — secção "VPS — nginx config" adicionada: prefix-strip `proxy_pass http://127.0.0.1:8000/;` (trailing slash) elimina `/api/` antes de repassar ao backend; backend permanece deployment-agnostic
- **Decisão:** subdomain `api.*` já fornece contexto; prefixo `/api` no código seria redundante; nginx é o ponto correto para este concern

#### B-01 — Consolidação docs de deploy *(commit `f0b6966`)*

- `docs/deploy/ENV_VARS.md` — reescrito: adicionadas `FRONTEND_URL`, `BACKEND_URL` (obrigatórias desde C-01), `DATABASE_URL_MIGRATIONS` (obrigatória desde DB-05), `VITE_API_BASE_URL` (Cloudflare Pages); `UPSTASH_REDIS_URL` marcada obrigatória em produção (A-02); comandos Render corrigidos (`uvicorn main:app` + `alembic upgrade head` como Release Command); Root Directory corrigido para `app/backend`; GitHub Secrets documentados; emails em `<>` (markdownlint MD034)
- `docs/deploy/DEPLOY.md` — secção "Backend (Linux típico)" substituída por tabela de comandos Render + referência a `DEPLOY_PRODUCTION.md`; arranque local corrigido para uvicorn
- `server/cloud_vps_audit_plans/DEPLOY_CLOUD_VPS.md` — **apagado** (`git rm`): cobria apenas C-01 (TLS); conteúdo integralmente absorvido por `DEPLOY_PRODUCTION.md`

#### Merge `audit-fix` → `3.1-dev` *(commit `8b35963`)*

- 16/16 planos do ciclo de audit Codex integrados em `3.1-dev` com `--no-ff`
- 37 commits de `audit-fix` integrados; 63 ficheiros alterados; sem conflitos

#### Fix deploy — `alembic/env.py` SQLAlchemy engine *(commit `a07fe55`)*

- `app/backend/alembic/env.py` — substituída ligação raw `psycopg2.connect()` por `sqlalchemy.create_engine()`;
  alembic 1.18.4 (SQLAlchemy 2.0) exige um objecto `Connection` SQLAlchemy em `context.configure()`,
  não uma `psycopg2.extensions.connection` (causava `AttributeError: 'psycopg2.extensions.connection' object has no attribute 'dialect'`)
- Deploy no Render confirmado live *(2026-05-24, 18:02 UTC)*

### Verificação pós-deploy e bugs encontrados em produção *(26/05/2026)*

#### Fix CSRF — cookie_domain split-domain *(commit `16a6604` audit-fix / `f92e000` 3.1-dev)*

- `app/backend/main.py` — `cookie_domain` adicionado ao `CSRFMiddleware`: em produção é derivado do
  hostname de `FRONTEND_URL` (`chichorrofireriskapp.joaopmteixeira.net`) via `urlparse`
- **Causa:** frontend e backend em subdomínios diferentes; cookie `csrftoken` era escoped para
  `api.*` e ilegível via `document.cookie` no frontend → `getCsrfToken()` sempre vazia → 403 em
  todos os POST não isentos (forgot-password, register, cálculos)
- Confirmado: `Set-Cookie: csrftoken=...; Domain=chichorrofireriskapp.joaopmteixeira.net`
- Em desenvolvimento (`ENV != "production"`), `cookie_domain` fica `None` — sem alterações

#### Fix RLS Supabase — migração 0002 *(commit `afa38d6` audit-fix / `ff76fa2` 3.1-dev)*

- `app/backend/alembic/versions/0002_disable_rls.py` — criada: `ALTER TABLE public.users DISABLE ROW LEVEL SECURITY` + `ALTER TABLE public.access_log DISABLE ROW LEVEL SECURITY`
- **Causa:** Supabase ativa RLS por defeito; `chichorro_runtime` tem grants de tabela mas sem políticas
  RLS → vê zero linhas → login retornava 401 `INVALID_CREDENTIALS` (SELECT na `users` vazio);
  INSERT no `access_log` falhava com `psycopg2.errors.InsufficientPrivilege`
- Fix manual executado no Supabase SQL Editor (2026-05-26); migração 0002 torna-o reproduzível
- Login confirmado a funcionar após desativar RLS

---

## 3.1-dev — Git history cleanup: retroactive branch extractions (2026-05-20)

### Reorganização retroativa do histórico git *(20/05/2026)*

Commits que tinham sido feitos diretamente em `3.1-dev` foram isolados em branches próprias,
e o histórico de `3.1-dev` foi reescrito para mostrar merges `--no-ff` explícitos — grafo
igual ao que seria produzido com git flow.

Branches criadas/extraídas:

- `auth/profile` — AUTH-09, AUTH-09a, AUTH-09b, AUTH-09c, UI-06 (7 commits; perfil de utilizador e definições)
- `db/backup` — DB-03 (3 commits; estratégia de backups e GitHub Actions workflow)
- `infra/sentry` — INFRA-01 (13 commits; Sentry frontend + backend + UptimeRobot)
- `docs/vitepress` — DOCS-01 (5 commits; migração Docsify → VitePress)

Técnicas usadas:

- `git cherry-pick` para reconstituir commits em novo base
- `git rebase --onto` para corrigir common ancestor de `auth/profile` após mudança de base
- `git commit-tree` para preservar `feat/flask-to-fastapi` como merge commit sem re-merge (evita conflitos)
- `git push --force-with-lease` em todas as branches reconstruídas
- Verificação: `git diff <old-HEAD> reconstruct-3.1-dev` = vazio (conteúdo final idêntico)

Não há alterações de código — apenas reorganização do grafo git.

---

## 3.1-dev — DOCS-01: Migração para VitePress (2026-05-20)

### DOCS-01 — Documentação pública em VitePress *(20/05/2026)* ✅

Docsify substituído por VitePress; documentação pública em `docs.chichorrofireriskapp.joaopmteixeira.net`.

- `docs/.vitepress/config.ts` — VitePress ^1.6.4; PT-PT; `cleanUrls`; `lastUpdated`; sidebar 6 secções; search local; `socialLinks` → `fireriskapp-docs`
- `docs/package.json` — VitePress ^1.6.4 como `devDependency`; scripts `dev`, `build`, `preview`
- `docs/index.md` — homepage com hero, descrição e quick links
- `docs/_sidebar.md` — apagado: ficheiro Docsify legado (causava 18 dead links no build VitePress)
- `docs/README.md` — reescrito: apenas links para ficheiros públicos; removidos links para `deploy/`, `plans/`, `security/`, `audits/`, `migration/`, `HISTORY_AI.md`
- `.github/workflows/sync-docs.yml` — `audits/` adicionada ao rsync `--exclude` e ao step de limpeza do target (auditoria de segurança não deve ser pública)
- Deploy: Cloudflare Pages via repo público `joaopmteixeira/fireriskapp-docs`; branch `main`; build `npm ci && npm run build`; output `.vitepress/dist`; domínio `docs.chichorrofireriskapp.joaopmteixeira.net`
- Build local verificado: 0 dead links; build Cloudflare verde

---

## 3.1-dev — INFRA-01 + DB-03: Monitorização + Backups (2026-05-19)

### INFRA-01 — Monitorização completa *(19/05/2026)* ✅

Sentry ativo em produção (frontend + backend) e UptimeRobot a monitorizar o endpoint `/health`.

- `app/frontend/src/main.tsx` — `@sentry/react` inicializado com `Sentry.init()`; `<Sentry.ErrorBoundary>` envolve a app; Session Replay com `replaysOnErrorSampleRate: 1.0` (apenas erros) e `maskAllText: true`; DSN via `VITE_SENTRY_DSN`
- `app/backend/main.py` — `sentry_sdk.init()` com DSN via `SENTRY_DSN`; `@app.exception_handler(Exception)` captura todos os erros 5xx e faz `sentry_sdk.capture_exception()` — sem dependência de integrações Starlette/FastAPI (incompatíveis com Starlette 1.0.0 + Python 3.14)
- `app/backend/main.py` — endpoint `/health` passa a usar `@app.api_route(..., methods=["GET", "HEAD"])` para suporte ao UptimeRobot (que usa HEAD)
- `app/backend/main.py` — `re.compile()` aplicado às `exempt_urls` do `CSRFMiddleware` (bug desde AUTH-13: `starlette-csrf` exige `re.Pattern`, não strings)
- `app/backend/requirements.txt` — `sentry-sdk>=2.0,<3` adicionado
- `app/frontend/package.json` — `@sentry/react` adicionado
- `docs/SERVICES.md` — criado: lista completa de todos os serviços externos, roles, configurações e notificações
- Validado em produção: erro capturado com replay de sessão anexado no Sentry; UptimeRobot a 147ms avg

### DB-03 — Estratégia de Backups *(19/05/2026)* ✅

Backup automático da base de dados implementado via GitHub Actions, com documentação completa.

- `.github/scripts/backup_db.py` — script commitado que exporta `users` + `access_log` para JSON timestamped em `backup/<timestamp>/`; usa `psycopg2` (sem pg_dump); lê `DATABASE_URL` do ambiente
- `.github/workflows/backup-db.yml` — workflow que corre de 3 em 3 dias (cron `0 3 */3 * *`) + `workflow_dispatch`; instala `psycopg2-binary`; guarda artifact com 90 dias de retenção
- `docs/deploy/ENV_VARS.md` — criado: referência completa de todas as env vars do projeto (backend Render + frontend Cloudflare Pages), sem valores, com indicação de onde obter cada um
- `docs/TOOLS.md` — criado: documentação commitada de todos os scripts em `tools/` (backup_db, create_test_user, dev-backend, migrate_neon_to_supabase, pdf_to_ai_markdown, fix_fences, fix_markdown_lint)
- Workflow validado em produção: run #1 verde, artifact gerado com sucesso; secret `DATABASE_URL` configurado no repositório GitHub

---

## 3.1-dev — AUTH-13: Session Hardening + Dark Mode completo (2026-05-18)

### AUTH-13 — Hardening de segurança da sessão *(18/05/2026)* ✅

Correção de três gaps de segurança identificados na cookie de sessão (FIR-30).

- `app/backend/config.py` — `session_secure` passa a `True` por omissão quando `ENV=production`; novo campo `session_max_age` (default 8h, configurável via `CHICHORRO_SESSION_MAX_AGE`)
- `app/backend/main.py` — `SessionMiddleware` passa `max_age`; `CSRFMiddleware` (starlette-csrf) adicionado com double-submit cookie — login/logout/health isentos; CORS passa a aceitar header `x-csrftoken`
- `app/frontend/src/lib/api.ts` — `getCsrfToken()` lê cookie `csrftoken`; `postJson` inclui `x-csrftoken` em todos os POST
- `app/backend/requirements.txt` — `starlette-csrf>=1.0,<2` adicionado
- `app/backend/Flask.py` — **eliminado** (backend legado v3.0, supersedido pelo FastAPI)
- `docs/deploy/DEPLOY.md` — tabela de env vars de sessão documentada

### UI-07 — Dark Mode completo *(18/05/2026)* ✅

- `RiPage.tsx` — scale classes, result cards, RI boxes, banners, limit card
- `CtiPage.tsx` — headings, secções CI/VHE/VVE, Input sub-component, ResultBlock, CTI final box
- `InterventionsPage.tsx` — lista de intervenções, ResultPanel, custo, escala
- Páginas de autenticação (Login, SignUp, ForgotPassword, ResetPassword) — labels, inputs, banners
- `PoiPage.tsx`, `DpiPage.tsx`, `EsciPage.tsx` — títulos e subtítulos com suporte dark mode
- `tailwind.config.js` — paleta neutra dark revisada; border de card header escondida quando colapsada

### Sidebar e avatar *(18/05/2026)*

- `AppLayout.tsx` — botão "Limpar sessão" restaurado (tinha sido removido acidentalmente no commit `c5cbf11`); `SidebarNavItem` refatorado com prop `variant: "default" | "warning" | "danger"` — "Limpar sessão" usa âmbar, "Sair" usa vermelho
- `ProfilePage.tsx` — dispatch `PROFILE_UPDATED_EVENT` após gravação de avatar; sidebar atualiza instantaneamente sem recarregar

### Correções diversas *(18/05/2026)*

- `fix(auth)` — removido gate `AUTH_NOT_CONFIGURED` que bloqueava logins de utilizadores DB sem pares estáticos definidos (`routers/auth.py`)
- `fix(dev)` — porta do proxy Vite corrigida de 50 → 8000 (`vite.config.ts`)
- `chore` — `docs/DEV_LOCAL.md` adicionado ao `.gitignore` (ficheiro local com referências a credenciais)

---

## 3.1-dev — BACK-04 + DB-02: Deploy FastAPI + Supabase (2026-05-15)

### BACK-04 — Deploy FastAPI no Render *(15/05/2026)* ✅

Resolução de erros de arranque no Render e deploy final do backend FastAPI em produção.

- `app/backend/database.py` — `_add_column()` usa `IF NOT EXISTS` para PostgreSQL (commits `024a33d`, `a0c5176`)
- `app/backend/database.py` — `SimpleConnectionPool` **removido**; substituído por conexões por request (`psycopg2.connect()` em cada `with _get_db()`). Causa: o pool é criado ao nível do módulo antes do gunicorn fazer fork dos workers — as conexões SSL ficam inválidas nos processos filho (`SSL SYSCALL error: EOF detected`). O PgBouncer do Supabase faz pooling do lado do servidor (commit `6562206`)
- `app/backend/requirements.txt` — `itsdangerous>=2.0,<3` adicionado: dependência implícita do `SessionMiddleware` do Starlette (commit `aa4de81`)
- Merge `3.1-dev` → `feat/flask-to-fastapi` sem conflitos (commit `f3173f8`); paridade verificada: `parity_runner.py` → **11/11 PASS**
- **Merge `feat/flask-to-fastapi` → `3.1-dev`** (commit `748dff1`, --no-ff): FastAPI é agora o backend de produção
- Teste e2e produção: login 1.49s, `/auth/me` 275ms, sem cold start ✓

### DB-02 — Migração Neon → Supabase *(15/05/2026)* ✅

Migração da base de dados de produção para eliminar o cold start de 45s do Neon free tier.

- **Neon free tier**: autosuspend após 5 min de inatividade → cold start 45s na primeira query pós-idle
- **Supabase free tier**: suspende apenas após 1 semana → sempre quente em uso regular
- `DATABASE_URL` (pooler Supabase, porta 6543, IPv4) substituiu `NEON_DATABASE_URL` (porta 5432, IPv6 — incompatível com Render free tier)
- `config.py` e `database.py` atualizados; env var no Render substituída
- 2 utilizadores migrados com `tools/migrate_neon_to_supabase.py`
- Resultado: login ~1.5s (antes 45s), `/auth/me` ~275ms; sem erros SSL

---

## feat/flask-to-fastapi — Migração Flask → FastAPI (2026-05-14)

### BACK-01 — Migração Flask → FastAPI *(14/05/2026)*

Migração do backend monolítico `Flask.py` (~2300 linhas) para FastAPI com estrutura modular.
A API pública (paths, payloads, cookies) é 100% preservada — o frontend não tem alterações.

- **Fase 1** — Scaffold FastAPI: `calc/` (motores de cálculo movidos de `app/backend/`), `config.py` (pydantic-settings), `database.py` (dual-mode SQLite/PostgreSQL, mantém `_PGConn`), `deps.py` (`require_auth` via `Depends`), `main.py` (app FastAPI + middleware CORS + SessionMiddleware + Limiter + routers)
- **Fase 2** — Pydantic schemas para todos os endpoints: `schemas/auth.py`, `schemas/poi.py`, `schemas/cti.py` (inclui `@model_validator` para normalização CTI, substitui `_normalize_cti_payload`), `schemas/dpi.py`, `schemas/esci.py`, `schemas/ri.py`
- **Fase 3** — Routers modulares: `routers/auth.py` (todos os endpoints `/auth/*`, `/login`, `/logout`, `/me`), `routers/admin.py` (`/admin/log`, `/admin/users`), `routers/poi.py`, `routers/cti.py`, `routers/dpi.py`, `routers/esci.py`, `routers/ri.py` (`/RI`, `/RI/interv`); `services/email.py` (helpers Resend extraídos)
- **Fase 5** — `wsgi.py` actualizado para FastAPI/uvicorn; `parity_runner.py` aponta para `http://127.0.0.1:8000`; `requirements.txt` actualizado (`fastapi`, `uvicorn[standard]`, `pydantic-settings`, `starlette`); `docs/ARCHITECTURE.md` atualizado com nova estrutura

Verificação: `python parity_runner.py` → **11/11 PASS**

### BACK-03 — ASCII enum values *(14/05/2026)*

- `app/frontend/src/components/dpi/dpiDefinitions.ts` — `value:` de 3 opções DPI/OGS → ASCII (sem `ç`/`ã`)
- `app/backend/calc/Chichorro_DPI.py` — comparações `if/elif` actualizadas para ASCII
- `app/backend/parity_runner.py` — payload de teste DPI/OGS → ASCII
- `app/backend/schemas/cti.py` — removidas entradas `"Inexistência"`, `"Não existe"`, `"Não Existe"` do `_ENUM_ALIASES`

---

## v3.1.2 — Perfil, Definições e Dark Mode (2026-05-13)

### AUTH-09 / AUTH-09a / AUTH-09b / AUTH-09c — Sistema de Perfil de Utilizador *(13/05/2026)*

- **AUTH-09 (backend)** — 5 rotas em `Flask.py`: `POST /auth/profile/username` (+ verificação password atual), `POST /auth/profile/email` (envio de link de re-verificação para novo e-mail), `POST /auth/profile/password`, `POST /auth/profile/delete` (confirmação textual `"eliminar conta"`), `POST /auth/profile/avatar`; migração DB para colunas `avatar TEXT`, `new_email`, `new_email_token`, `new_email_token_expires_at`; rate limit 5/hora por rota; endpoint `GET /auth/verify-email-change/<token>`
- **AUTH-09a** — ProfilePage: card `max-w-sm`, header gradient `brand-900→brand-800`, avatar circular com initials fallback, menu accordion com ícones MDI e chevron animado
- **AUTH-09b** — Avatar de utilizador: canvas resize 256×256 JPEG 0.85 → base64 → `POST /auth/profile/avatar`; coluna `avatar` na tabela `users`; sidebar actualizada com avatar real
- **AUTH-09c** — Redesign card compacto: 4 rows expansíveis inline (nome de utilizador, endereço de e-mail, palavra-passe, apagar conta); pencil overlay no avatar para edição; sem modal separado; sem "Zona de perigo"; sem botão "Sair"; errMsg melhorado para mostrar erros específicos do servidor

### UI-06 — Página de Definições *(13/05/2026)*

- `src/lib/prefs.ts` (novo) — store de preferências em localStorage; tipo `Prefs = {theme: "system"|"light"|"dark", warnOnExit: boolean, decimalPlaces: 2|3|4}`; `getPrefs()`, `setPrefs()`, `usePrefs()` (hook reactivo via `PREFS_CHANGED_EVENT`); `applyTheme()` com suporte a preferência do sistema via `matchMedia`
- `src/pages/SettingsPage.tsx` (novo) — 3 secções num único card: **Aparência** (radio system/claro/escuro), **Sessão** (toggle avisar antes de sair com dados não guardados), **Resultados** (radio 2/3/4 casas decimais); rota `/app/settings` adicionada em `App.tsx`
- `src/main.tsx` — aplica tema na inicialização; escuta `prefers-color-scheme` do SO e `PREFS_CHANGED_EVENT`
- `tailwind.config.js` — `darkMode: "class"`; paleta `ink` estendida: `400: "#94a3b8"`, `800: "#1e293b"`, `950: "#020617"`
- `src/index.css` — `.dark { color-scheme: dark; }`
- `AppLayout.tsx` — `shouldWarnOnExit` usa `prefs.warnOnExit`; link "Definições" aponta para `/app/settings`; username sidebar corrigido (lê de `/auth/me` em vez de sessionStorage)
- `RiPage.tsx` + `CtiPage.tsx` — `toFixed(getPrefs().decimalPlaces)` em todos os resultados numéricos

### UI-07 (parcial) — Dark Mode infra + conteúdo principal *(13/05/2026)*

- `Card.tsx` — `dark:bg-ink-900 dark:border-ink-700`; CardHeader com `dark:text-ink-50` / `dark:border-ink-700`
- `Field.tsx` — Label `dark:text-ink-300`; Select `dark:bg-ink-800 dark:border-ink-700 dark:text-ink-50`
- `Button.tsx` — variante `secondary` com `dark:bg-ink-800 dark:text-ink-50 dark:border-ink-700 dark:hover:bg-ink-700`
- `ModuleGlobalValueCard.tsx` — `dark:bg-ink-900 dark:border-ink-700`; valor e label com dark variants
- `PoiFactorSection.tsx` / `DpiFactorSection.tsx` / `EsciFactorSection.tsx` — removido `style={{ color }}` (inline style bloqueava dark mode); dark variants nos result boxes, banners âmbar/vermelho, botão limpar
- `AppLayout.tsx` + `ProfilePage.tsx` + `SettingsPage.tsx` — dark variants completos

### Fix backend — Rota catch-all SPA *(13/05/2026)*

- `Flask.py` — `_serve_spa_or_asset` (`@app.get("/<path:asset_path>")`) passou a excluir `auth`, `admin`, `login`, `logout`, `me` do catch-all; evita que o gunicorn responda 405 com `Allow: GET, HEAD, OPTIONS` a pedidos POST para `/auth/profile/*`

---

## v3.1.1 — Autenticação e segurança (2026-05)

### AUTH-01 — Log de acessos (base de dados) *(05/05/2026)*

- Base de dados PostgreSQL (Neon) em produção; SQLite local em dev (comutação automática via `NEON_DATABASE_URL`)
- Wrapper `_PGConn` em `Flask.py`: converte `?` → `%s` e `AUTOINCREMENT` → `SERIAL PRIMARY KEY`; API idêntica ao `sqlite3`
- Tabela `access_log`: registo de eventos `login`/`logout` com username, timestamp UTC e IP
- Endpoints `GET /admin/log` e `GET /admin/users` (requerem autenticação)

### AUTH-02 — Registo de utilizadores com verificação de e-mail *(05/05/2026)*

- Tabela `users` com password hashing (`werkzeug.security`), token de verificação e expiração de 24h
- `POST /auth/register` — validação, unicidade e-mail/username, envio de e-mail em thread daemon
- `GET /auth/verify/<token>` — activa conta e redireciona para o frontend com `?verified=ok/expired/invalid/already`
- Envio de e-mail via SDK Resend (`resend.Emails.send()`); fallback para terminal quando `RESEND_API_KEY` não está definido
- Link de verificação usa `request.url_root` capturado antes de spawnar a thread; `APP_BASE_URL` é usado apenas para reset (rota React)

### AUTH-03 — Página de registo no frontend *(05/05/2026)*

- `SignUpPage.tsx` — formulário com e-mail, username, palavra-passe e confirmação
- Validação PT-PT no browser (`setCustomValidity`)
- Banner de sucesso com redirect para login
- `LoginPage.tsx` — banner `?verified=ok/expired/invalid/already`; link "Criar conta"

### AUTH-04 — Recuperação de palavra-passe *(06/05/2026)*

- Colunas `reset_token` e `reset_token_expires_at` adicionadas via migração automática (`_init_db`)
- `POST /auth/forgot-password` — gera token (1h), envia e-mail em background thread; sempre responde `{"ok":true}` (não revela existência do e-mail)
- `POST /auth/reset-password` — valida token, actualiza hash, limpa token
- `ForgotPasswordPage.tsx` e `ResetPasswordPage.tsx` — novas páginas com estilo consistente
- `LoginPage.tsx` — link "Esqueceu a palavra-passe?" e banner `?reset=ok`

### AUTH-05 — Modal de sessão expirada *(06/05/2026)*

- `postJson` despacha `SESSION_EXPIRED_EVENT` em qualquer resposta 401
- `AppLayout` escuta o evento e mostra modal bloqueante: "Sessão expirada — Recarregar página"
- Cobre o caso de cookies apagadas manualmente pelo utilizador

### Infra — Correção de IP no access_log *(08/05/2026)*

- `ProxyFix` (`werkzeug.middleware.proxy_fix`) adicionado ao `app.wsgi_app` com `x_for=1, x_proto=1, x_host=1`
- O `access_log` regista agora o IP real do cliente em vez do IP interno do proxy Render (`127.0.0.1`)

### DB-01 + TEST-01 — Validação em produção *(08/05/2026)*

- Neon PostgreSQL activo em produção; env vars configuradas no Render; deploy verde
- Fluxo e2e aprovado: registo → e-mail Resend → verificação → login → recuperação de palavra-passe
- Modal de sessão expirada validado ao apagar cookie manualmente em DevTools

### AUTH-12 — Merge `feat/access-log` → `3.1-dev` *(08/05/2026)*

- Merge completo do sistema de autenticação para o branch principal `3.1-dev`
- Resolução de 6 conflitos em ficheiros de docs (CHANGELOG, DECISIONS_LOG, HOSTING_OPTIONS, NEXT_STEPS, PROJECT_OVERVIEW, sync-docs.yml)
- Ficheiros TODO adicionados ao sidebar Docsify e ao sync público para `FIRERISKAPP-DOCS`

### AUTH-07 — Rate limiting nos endpoints de autenticação *(08/05/2026)*

- Flask-Limiter com Upstash Redis (EU Frankfurt, free tier) como backend partilhado entre workers gunicorn
- Limites: `/auth/login` 5/min · `/auth/register` 3/hora · `/auth/forgot-password` 3/hora · `/auth/reset-password` 5/hora
- `@app.errorhandler(429)` retorna JSON `{"error": "RATE_LIMITED", "message": "..."}` em PT-PT
- `postJson` em `api.ts` trata 429 com mensagem PT-PT específica
- Validado em produção dev: 5 pedidos passam, 6º retorna 429; contadores visíveis no Data Browser Upstash

### AUTH-08 — Regeneração de sessão após login *(08/05/2026)*

- `session.clear()` adicionado antes de `session["chichorro_auth"] = 1` nos 3 pontos de login em `Flask.py`
- Mitiga session fixation (OWASP ASVS V3.3)
- Cobre login hardcoded (env vars), login modo debug e login via base de dados

### AUTH-06 — Hardening de cookies de sessão *(08/05/2026)*

- Confirmadas as 3 configurações: `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SECURE` (via `CHICHORRO_SESSION_SECURE=1`), `SESSION_COOKIE_SAMESITE = "Lax"`
- Cookie renomeado de `session` para `chichorro_session` via `SESSION_COOKIE_NAME` (anti-fingerprinting)

### SEC-01 — Revisão da configuração CORS *(12/05/2026)*

- `allow_headers` restringido a `["Content-Type"]`
- Métodos limitados a `["GET", "POST", "OPTIONS"]`
- `max_age=86400` (1 dia de cache de preflight)
- Fallback dev explícito para `localhost:5173` quando `CHICHORRO_CORS_ORIGINS` não está definido

### SEC-02 — HTTPS obrigatório em produção *(12/05/2026)*

- Render força HTTPS no reverse proxy (sem acesso HTTP à app Flask)
- `CHICHORRO_SESSION_SECURE=1` ativo em produção (cookies apenas transmitidas por HTTPS)
- HSTS adicionado via `@app.after_request`: `Strict-Transport-Security: max-age=31536000; includeSubDomains` quando `SESSION_COOKIE_SECURE` está ativo

### SEC-03 — Headers de segurança *(12/05/2026)*

- `X-Content-Type-Options: nosniff` — previne MIME sniffing
- `X-Frame-Options: DENY` — previne clickjacking
- `Referrer-Policy: strict-origin-when-cross-origin` — limita informação enviada no Referer
- CSP diferida para Cloudflare Pages (documentada em `docs/plans/SEC-03.md`)

### Auditoria de segurança e usabilidade *(12/05/2026)*

Auditoria completa documentada em `docs/plans/AUDIT-2026-05-12.md`:

- **S-01** — `warnings.warn()` no arranque de `Flask.py` quando `CHICHORRO_SECRET_KEY` usa o valor default inseguro `"dev-change-me"`
- **S-02** — Validação de e-mail com regex `_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")` em vez de check permissivo `@`/`.`
- **U-01** — Estado de carregamento no `LoginPage.tsx`: botão disabled com "A iniciar sessão…" durante o pedido; previne double-submit
- **U-02** — Componente `PasswordInput.tsx` reutilizável com toggle show/hide (ícone SVG inline, `tabIndex={-1}`); aplicado em `LoginPage`, `SignUpPage` e `ResetPasswordPage`
- **U-03** — `role="alert"` adicionado a todos os elementos `<p>` de erro nas páginas de autenticação (anuncia erros a screen readers via `aria-live="assertive"` implícito)
- **U-04** — `role="dialog"`, `aria-modal="true"` e `aria-labelledby` adicionados aos 3 modais em `AppLayout.tsx` (sessão expirada, limpar sessão, sair)

### Merge `feat/security` → `3.1-dev` *(12/05/2026)*

- Merge `--no-ff` do branch `feat/security` para `3.1-dev`
- 20 ficheiros alterados, 968 inserções
- Push para GitHub; sync de docs para `FIRERISKAPP-DOCS` disparado

### BACK-02 — Melhorar logging *(12/05/2026)*

- Coluna `user_agent TEXT` adicionada ao `access_log` via migração idempotente (`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`)
- `_write_access_log()` passa a capturar e guardar o `User-Agent` de cada pedido
- `/auth/login` regista agora tentativas falhadas: `login_failed` (credenciais inválidas) e `login_failed:unverified` (e-mail não verificado)
- `@app.before_request` gera `g.request_id = uuid.uuid4().hex[:8]` por pedido
- `@app.errorhandler(500)` loga o erro com o `request_id` e devolve-o no JSON da resposta para correlação
- `/admin/log` atualizado para devolver a nova coluna `user_agent`

---

## v3.1 — Aplicação Web (Abril 2026)

Primeira versão pública do FireRiskApp como aplicação web, implementando o modelo CHICHORRO 3.1.

### Modelo implementado *(20–21/04/2026)*

- Implementação completa do modelo CHICHORRO 3.1 (dissertação Rui Sobral, FEUP, 2019)
- Escala de classificação de 12 classes: **A++, A+, A, B+, B, B-, C+, C, C-, D, E, F**
- Aceitabilidade de risco por utilização tipo (RI_RIA) baseada em POI_CC_Idade

### Módulos disponíveis

- **POI** — Potencial Ocorrência de Incêndio (subfatores: CC, EF, IA, ATIV)
- **CTI** — Consequências para os Utilizadores (subfatores: VHE, VVE, com Dispositivos distintos por veia)
- **DPI** — Desenvolvimento e Propagação (subfatores: CF, CA, OGS com 4 campos reformulados)
- **ESCI** — Eficácia de Socorro e Combate (subfatores: GP com deteção automática, EXT, RIA/CS com formação)
- **RI** — Cálculo do Índice de Risco final
- **Intervenções** — 34 intervenções ativas e passivas; conjuntos predefinidos por tipo de utilização

### Experiência de utilizador (UX-01…UX-08) *(22–29/04/2026)*

- **UX-01** — Campos em falta destacados com `ring-2 ring-red-400`; resultados antigos em cinza translúcido com aviso âmbar; card global mostra `Valor desatualizado`
- **UX-02** — Aviso vermelho na RiPage quando inputs mudam após cálculo do RI (`SESSION_DATA_UPDATED_EVENT` + `loadingRef`)
- **UX-03** — Colapsar/expandir subfatores em POI, DPI e ESCI: botão com chevron animado; animação CSS `grid-rows` sem `max-height` fixo; scroll automático ao receber deep link
- **UX-04** — Persistência do estado colapsado em `sessionStorage` com chave `collapse:{formKey}`
- **UX-05** — Aviso de sucesso com fade (3 s) na RiPage; gate de erros: avisos só aparecem após o primeiro cálculo
- **UX-06** — Persistência de `error`, `warning`, `missingFieldKey`, `isResultStale` em `sessionStorage` entre navegações
- **UX-07** — Warning âmbar ao limpar subfator; card e banner `ERRO` na RiPage quando módulo fica `undefined`
- **UX-08** — Auto-atualização de resultados na RiPage via listener `SESSION_DATA_UPDATED_EVENT`; botão "Atualizar resultados" removido

### Funcionalidades de interface *(13/04–04/05/2026)*

- Navegação por módulos com persistência de sessão (sessionStorage)
- Exportar / importar sessão em formato JSON
- Resultados desatualizados assinalados visualmente quando inputs são alterados após cálculo (→ UX-01, UX-02)
- Campos obrigatórios em falta com destaque visual e mensagem específica (→ UX-01)
- Módulo de Intervenções com cálculo de custo estimado (€/m²)

### Stack técnica *(inicial: 13/04/2026)*

- Frontend: React 18 + TypeScript + Vite + Tailwind CSS → Cloudflare Pages
- Backend: Python FastAPI/ASGI → Render

---

## v3.0 — Modelo CHICHORRO 3.0

Desenvolvimento original do modelo CHICHORRO 3.0 por **João Teixeira** (FEUP).

- Definição dos quatro fatores principais: POI, CTI, DPI, ESCI
- Escala de 6 classes: A1, A2, B, C, D, E
- Implementação em folha de cálculo e aplicação web de referência

---

## v2.0 — Método Simplificado

Desenvolvimento do método simplificado CHICHORRO 2.0 por **Ricardo Ferreira** (FEUP).

- Base metodológica para avaliação expedita de risco de incêndio
- Precursor do método completo utilizado nas versões 3.x

---

## v1.0 — Método base

Formulação original do método CHICHORRO para avaliação de risco de incêndio em edifícios históricos (FEUP).
