# TODO List — Por ID

Listagem completa de todas as ações do projeto, ordenadas por prefixo e número de ID.
Para prioridades e detalhes ver [TODO_PRIORITIES.md](TODO_PRIORITIES.md).

Última atualização: 2026-06-15 (INFRA-09 concluído — Cloudflare Tunnel para chichorro.joaopmteixeira.net)

Legenda: ✅ concluído · 🔄 em progresso · ❌ pendente

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
- **`MODEL`** — Modelo CHICHORRO (backlog pós-3.1)
- **`AI`** — AI tooling e knowledge graph (Graphify, Obsidian, RAG)
- **`B`** — Tarefas de manutenção/organização

---

## REL — Releases e Versionamento

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| REL-01 | ❌ | Release baseline v3.1.0 — tag git, release notes, snapshot estável pré-infra | — |

---

## AUTH — Autenticação e Sessões

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| AUTH-01 | ✅ | Log de acessos — tabela `access_log`, `/admin/log`, `/admin/users` | feat/access-log |
| AUTH-02 | ✅ | Registo com verificação de e-mail (Resend SDK, thread daemon) | feat/access-log |
| AUTH-03 | ✅ | Frontend de registo — SignUpPage, banners LoginPage | feat/access-log |
| AUTH-04 | ✅ | Recuperação de palavra-passe — ForgotPasswordPage, ResetPasswordPage | feat/access-log |
| AUTH-05 | ✅ | Modal "sessão expirada" — SESSION_EXPIRED_EVENT, AppLayout | feat/access-log |
| AUTH-06 | ✅ | Verificar hardening cookies: HTTPONLY, SECURE, SAMESITE + renomear cookie (anti-fingerprinting) | feat/security |
| AUTH-07 | ✅ | Rate limiting com slowapi + Upstash Redis nos endpoints /auth/* + fail-fast Redis no arranque (A-02) | feat/security + audit-fix |
| AUTH-08 | ✅ | Regenerar sessão após login (mitigação session fixation) | feat/security |
| AUTH-09 | ✅ | Editar perfil: backend routes (username, e-mail c/ re-verificação, password, apagar conta) | 3.1-dev |
| AUTH-09a | ✅ | ProfilePage redesign — card layout c/ header gradient, menu accordion, ícones MDI | 3.1-dev |
| AUTH-09b | ✅ | Avatar de utilizador — coluna `avatar` DB, rota `POST /auth/profile/avatar`, upload frontend c/ canvas resize | 3.1-dev |
| AUTH-09c | ✅ | ProfilePage redesign card compacto — 4 rows expansíveis inline (username, e-mail, password, apagar conta); sem modal separado | 3.1-dev |
| AUTH-09d | ✅ | Otimização do avatar: WebP, 128 px, limite 100 KB — reduz armazenamento na BD ~80% | 3.1-dev |
| AUTH-10 | ✅ | Sistema de roles/permissões: coluna `role`, `require_admin`, admin UI — viewer/demo diferidos | auth/roles → 3.1-dev |
| AUTH-13 | ✅ | Hardening sessão: max_age configurável, Secure flag obrigatória em prod, CSRF protection | 3.1-dev |
| AUTH-11 | ✅ | Validar modal sessão expirada em produção (apagar cookie) | feat/access-log |
| AUTH-12 | ✅ | Merge `feat/access-log` → `3.1-dev` | 3.1-dev |

---

## DB — Base de Dados e Persistência

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| DB-01 | ✅ | Neon PostgreSQL em produção — env vars, deploy, TEST-01 aprovado | feat/access-log |
| DB-02 | ✅ | Migração Neon → Supabase — elimina cold start 45s; per-request connections (PgBouncer) | 3.1-dev |
| DB-03 | ✅ | Estratégia de backups — `scripts/backup_db.py`, GitHub Actions workflow, `scripts/restore_db.py`, subplan (A-04: descoberta dinâmica + restore + DEPLOY_PRODUCTION.md) | 3.1-dev + audit-fix |
| DB-04 | ✅ | Migrations Alembic — versioning de schema, rollback, remover DDL do arranque da app | audit-fix |
| DB-05 | ✅ | Least privilege DB — utilizador `chichorro_runtime` criado; `DATABASE_URL_MIGRATIONS` para Alembic; ações manuais Supabase/Render/GitHub pendentes | audit-fix |
| DB-06 | ✅ | Migrar camada de dados para SQLAlchemy ORM — autogenerate Alembic, connection pooling, remover psycopg2 custom wrapper | 2026-06-09 |
| DB-07 | ✅ | Backups PostgreSQL local — script diário, restore testado, alertas em falha | feat/db07-db08-backups |
| DB-08 | ✅ | Runbook migração Supabase → PostgreSQL local — dump, restore, validação, rollback | feat/db07-db08-backups |

---

## SEC — Segurança e Hardening

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| SEC-01 | ✅ | CORS estrito em produção — sem `*`, validação positiva https:// (urlparse), `FRONTEND_URL` incluída nas origins (A-01; reforçado audit-fix-2 #2) | audit-fix, audit-fix-2 |
| SEC-02 | ✅ | HTTPS obrigatório em produção — fail-fast `FRONTEND_URL`/`BACKEND_URL` validação positiva urlparse (C-01; reforçado audit-fix-2 #2) | feat/security, audit-fix-2 |
| SEC-03 | ✅ | X-Content-Type-Options, X-Frame-Options, Referrer-Policy via `@app.after_request`; CSRF coberto por camadas existentes | feat/security |
| SEC-04 | ✅ | Argon2id password hashing (argon2-cffi, RFC 9106 level 1) + upgrade-on-login a partir de werkzeug scrypt/pbkdf2 | sec/hardening |
| SEC-05 | ✅ | Hash SHA-256 dos tokens de reset/verificação/email-change na BD; CSRF exemption para endpoints públicos | sec/token-hashing |
| SEC-06 | ✅ | Política de logs — garantir que tokens e PII não são impressos em produção (A-05) | audit-fix |
| SEC-07 | ✅ | Bloquear SVG e validar magic bytes no endpoint `/auth/profile/avatar` (JPEG/PNG/WebP/GIF) | sec/hardening |
| SEC-08 | ✅ | Remover `legacyLogin.ts` e limpar variáveis `VITE_LOGIN_*` do `.env` local (M-05) | audit-fix |
| SEC-09 | ✅ | CSP + Permissions-Policy no backend (`add_security_headers`) e Cloudflare Pages (`_headers`) (M-01) | audit-fix |
| SEC-10 | ✅ | Fail-fast secrets em produção — `CHICHORRO_SECRET_KEY` e outros secrets obrigatórios; sem arranque silencioso com defaults inseguros (C-04) | audit-fix |
| SEC-11 | ✅ | Gestão de secrets — política de env vars, backup seguro, rotação (JWT, DB, Resend, Sentry) | feat/sec11-sec12-secrets-pgadmin |
| SEC-12 | ✅ | Proteção pgAdmin — Nginx Basic Auth em 5050/5051; pgAdmin/Adminer sem ports diretos | feat/sec11-sec12-secrets-pgadmin |
| SEC-13 | ❌ | Hardening stack Docker — Gitleaks CI, redes internas, serviço migrate separado, suporte `*_FILE` em config.py, systemd na VM | — |
| SEC-14 | ❌ | SOPS + age — gestão de secrets encriptados em Git (futuro; relevante quando equipa crescer ou GitOps) | — |

---

## UI — Interface e Experiência

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| UI-02 | ❌ | Página de Documentação integrada na app | — |
| UI-03 | ❌ | Página de Ajuda integrada na app | — |
| UI-04 | ❌ | FAQs — Perguntas Frequentes | — |
| UI-05 | ❌ | Bug Report — formulário de reporte (destino: e-mail/GitHub/ClickUp) | — |
| UI-08 | ❌ | Ícones ℹ️ nos subfatores — painel com descrição detalhada, tabela de valores e referência RT-SCIE | — |
| UI-09 | ❌ | Badge de lápis persistente no avatar — sempre visível (mobile-friendly), substitui overlay câmara hover-only | 3.1-dev |
| UI-10 | ❌ | Sidebar direita persistente — resumo da sessão atual e valores introduzidos nos subfatores (POI/CTI/DPI/ESCI) visíveis durante o cálculo | — |
| UI-06 | ✅ | Preferências / Definições do utilizador — dark mode (sistema/claro/escuro), avisar antes de sair, casas decimais | 3.1-dev |
| UI-07 | ❌ | Dark Mode — redesign e validação pendentes; implementação inicial de 2026-05-18 carece de revisão completa de todas as vistas | 3.1-dev |

---

## FEAT — Funcionalidades Novas

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| FEAT-01 | ❌ | Gráfico impacto intervenções (tornado chart, Recharts) | — |
| FEAT-02 | ❌ | Guardar edifício — nome, morada, código postal, distrito/concelho/freguesia (cascata), GPS + mapa; resultados associados ao utilizador e em tabela geral | — |
| FEAT-03 | ❌ | Chatbot AI assistente CHICHORRO (Claude API ou similar) | — |
| FEAT-04 | ❌ | Geração de relatório em PDF após cálculo completo — exportar resultados RI, CTI e subfatores (POI/DPI/ESCI) para ficheiro PDF imprimível e partilhável | — |

---

## UX — Micro-melhorias de Experiência (CHICHORRO 3.1)

Todos concluídos durante a implementação do CHICHORRO 3.1.

| ID | Estado | Descrição |
| --- | --- | --- |
| UX-01 | ✅ | Campos em falta com ring vermelho; resultados antigos em cinza translúcido; card "Valor desatualizado" |
| UX-02 | ✅ | Aviso vermelho na RiPage quando inputs mudam após cálculo (SESSION_DATA_UPDATED_EVENT) |
| UX-03 | ✅ | Colapsar/expandir subfatores (POI, DPI, ESCI) com botão chevron animado |
| UX-04 | ✅ | Persistência do estado colapsado em sessionStorage por subfator |
| UX-05 | ✅ | Aviso de sucesso com fade (3 s) na RiPage; gate de erros pós-primeiro cálculo |
| UX-06 | ✅ | Persistência de error/warning/missingFieldKey/isResultStale entre navegações |
| UX-07 | ✅ | Warning âmbar ao limpar subfator; banner ERRO na RiPage quando módulo fica undefined |
| UX-08 | ✅ | Auto-atualização de resultados na RiPage; botão "Atualizar resultados" removido |

---

## BACK — Arquitetura Backend

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| BACK-01 | ✅ | Migração Flask → FastAPI: calc/, routers/, schemas/, services/, uvicorn | feat/flask-to-fastapi |
| BACK-02 | ✅ | Melhorar logging: failed logins, user-agent, request IDs, erros backend; fix 405 no catch-all SPA | 3.1-dev |
| BACK-03 | ✅ | ASCII enum values — remover ç/ã dos values DPI e aliases CTI | feat/flask-to-fastapi |
| BACK-04 | ✅ | Merge feat/flask-to-fastapi → produção; deploy FastAPI no Render (Supabase, 1.5s login) | 3.1-dev |
| BACK-05 | ✅ | Pydantic `Literal` types nos schemas dpi, esci, cti, poi (BACK-05d) — payloads inválidos retornam 422 | back/validation |
| BACK-06 | ✅ | Error handler JSON normalizado — `JSONResponse({"error":"INTERNAL_ERROR"}, 500)` em vez de re-raise | back/validation |
| BACK-07 | ✅ | Estabilizar naming de rotas API — decisão documentada: manter paths actuais; aliases legacy removidos (`/login`, `/logout`, `/me`, `/RI_interv`); nginx VPS config documentada (B-02) | audit-fix |

---

## INFRA — Infraestrutura e DevOps

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| INFRA-01 | ✅ | Monitorização: Sentry (frontend + backend) + UptimeRobot `/health`; M-04 (audit-fix): X-Request-ID middleware, backup failure email Resend, UptimeRobot `/health/db` (manual) | 3.1-dev + audit-fix |
| INFRA-02 | ✅ | Pipeline CI/CD: GitHub Actions test.yml (pytest) + build.yml (npm build), path filters | infra/ci-cd |
| INFRA-03 | ✅ | Dockerfile + Compose local/prod — containerização para deploy reproduzível | 3.1-dev |
| INFRA-04 | ✅ | Endpoint `/health/db` — health check com query à BD para deteção de falha de ligação (A-06) | audit-fix |
| INFRA-05 | ✅ | Cache-Control headers: `no-store` no backend + `_headers` Cloudflare Pages; `/assets/*` com `immutable` (M-02) | audit-fix |
| INFRA-06 | ✅ | Separação de ambientes + deploy Proxmox/Debian 13: `.env` + `.env.example` + guia deploy Docker | feat/infra07-env-proxmox |
| INFRA-07 | ✅ | Staging Proxmox completo — Nginx reverse proxy + PostgreSQL local na VM Debian 13 | 2026-06-15 |
| INFRA-08 | ❌ | Monitorização self-hosted — Docker logs, PostgreSQL health, disco, CPU, RAM, alertas de backup | — |
| INFRA-09 | ✅ | Cloudflare Tunnel — expor chichorro.joaopmteixeira.net via tunnel sem abrir portas no router | feat/infra09-cloudflare-tunnel |
| INFRA-10 | 🔄 | pgAdmin + Adminer em staging — avaliação; conclusão após remover a ferramenta não escolhida | feat/infra10-pgadmin-adminer |

---

## TEST — Testes e Validação

| ID | Estado | Descrição |
| --- | --- | --- |
| TEST-01 | ✅ | Teste e2e em produção: registo → e-mail → verificação → login → reset password (aprovado 2026-05-08) |
| TEST-02 | ✅ | Testes automatizados: pytest 12/12 (health, Literal 422, calc 200, auth básico) — branch `test/automated-tests` |
| TEST-03 | ✅ | Parity checker (`scripts/check_option_parity.py`) + 338 golden tests Literal (`test_valid_options.py`) — todos os subfatores cobertos (`3.1-dev`) |
| TEST-04 | ❌ | Smoke tests Docker Compose — `/health`, `/health/db`, login, logout, sessão, CSRF, frontend build |
| CALC-AUDIT | ❌ | Golden tests do código de cálculo vs. tese3.1 (~280 tests) — bloqueado até Excel tese3.1 disponíveis (`fir-XX-calc-audit`) |

---

## MODEL — Modelo CHICHORRO (backlog pós-3.1)

Propostas de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1.

| ID | Estado | Descrição |
| --- | --- | --- |
| MODEL-01 | ❌ | Método simplificado baseado no CHICHORRO 2.0 (Ricardo Ferreira + Bruno Silva) |
| MODEL-02 | ❌ | Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo) |
| MODEL-03 | ❌ | Afinação de custos €/m² via PRONIC |
| MODEL-04 | ❌ | Intervenções adicionais: Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa |
| MODEL-05 | ❌ | Georreferenciação e base de dados de edifícios |
| MODEL-06 | ❌ | Tratamento de edifícios devolutos |
| MODEL-07 | ❌ | Integração com Firecheck 2.0 |

---

## AI — AI Tooling e Knowledge Graph

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| AI-01 | ✅ | Setup Graphify — grafos backend (367 nós), frontend (346 nós), cross-stack (740 nós); CLAUDE.md com regras de refresh | 3.1-dev |
| AI-02 | ✅ | Setup Obsidian vault — 50 notas, 27 subfatores × 8 fontes, RT-SCIE 1532/2008 + 135/2020, Backend/Frontend via registry lookup | feat/obsidian-vault |
| AI-02a | ❌ | Curation manual — `## Definicao` (27 notas), validar "verificar" em `## Onde e mencionado`, verificar Graph View Obsidian | feat/obsidian-vault |
| AI-03 | ❌ | RAG — pgvector + `routers/rag.py` + botão "Explicar" por subfator; implementar após AI-02a concluído | — |

---

## DOCS — Documentação

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| DOCS-01 | ✅ | Migrar documentação de Docsify para VitePress — build estático, SEO, deploy em docs.chichorrofireriskapp.joaopmteixeira.net. Linear: FIR-31. | 3.1-dev |
| DOCS-02 | ✅ | Uniformizar headers de todos os subplans (`docs/plans/subplans/`) — formato canónico Estado→Data→Branch; eliminado DESIGN.md duplicado | 3.1-dev |

---

## CHICHORRO 3.1 — Implementação (Blocos A/B/C)

Todos os itens concluídos. Detalhe completo em [NEXT_STEPS.md](NEXT_STEPS.md).

| ID | Estado | Descrição |
| --- | --- | --- |
| A1 | ✅ | Análise CTI 3.1 — diferenças identificadas |
| A1b | ✅ | Atualizar Chichorro_CTI.py (assinatura 3.1, sympy fix, paridade 11/11) |
| A3 | ✅ | Batch: substituir POI / ESCI / DPI + completar RI |
| A4 | ✅ | Backend legado + Chichorro_RI_inter.py — endpoints 3.1 + /RI/interv |
| B1 | ✅ | poiDefinitions.ts — adicionar POI_CC_Idade |
| B2 | ✅ | esciDefinitions.ts — ESCI_GP_Auto, ESCI_EXT_Formacao, ESCI_RIA_CS |
| B3 | ✅ | dpiDefinitions.ts — DPI_OGS de 7→4 campos |
| B4 | ✅ | RiPage.tsx — escala 12 classes, remover seletor período |
| B5 | ✅ | InterventionsPage.tsx — 34 intervenções, conjuntos predefinidos |
| B6 | ✅ | UX validação e invalidação de resultados (→ UX-01) |
| B7 | ✅ | Correções POI_EF e POI_IA |
| B8 | ✅ | Fix sync bidirecional CTI ↔ POI_ATIV (TipoEdif) |
| B9 | ✅ | Aviso RI desatualizado na RiPage (→ UX-02) |
| B10 | ✅ | Expor VHE_Dispositivos / VVE_Dispositivos em CtiPage.tsx |
| B11 | ✅ | Colapsar/expandir subfatores POI, DPI, ESCI (→ UX-03, UX-04) |
| C1 | ✅ | Paridade backend 3.1 — parity_runner.py: 11/11 checks ✅ |
