# Estado do Projeto e Próximos Passos

Última atualização: 2026-05-19

> **Issues tracked in Linear** — team [FireRiskApp](https://linear.app/fireriskapp), projeto **CHICHORRO 3.1** (FIR-5 a FIR-29).
> Usar o Linear como fonte de verdade para estado de tarefas. Este ficheiro mantém-se como referência rápida.

---

## Estado atual

| Área | Estado |
| --- | --- |
| Modelo CHICHORRO 3.1 | ✅ Completo (11/11 paridade backend, e2e aprovado) |
| Autenticação e sessões | ✅ Completo (AUTH-01..09c, AUTH-11, AUTH-12) |
| Hardening de segurança | 🔄 Parcial (SEC-01..03, AUTH-13 ✅; SEC-04..09, BACK-05..06 pendentes — auditoria 2026-05-19) |
| Auditoria segurança/UX | ✅ Completo (S-01..02, U-01..04) |
| Perfil de utilizador | ✅ Completo (AUTH-09, AUTH-09a, AUTH-09b, AUTH-09c) |
| Preferências / Definições | ✅ Completo (UI-06: dark mode, avisar-antes-de-sair, casas decimais) |
| Dark Mode (UI-07) | ✅ Completo — todas as páginas cobertas (commit `d2d6492`) |
| Migração Flask → FastAPI (BACK-01) | ✅ Completo — 11/11 PASS (`feat/flask-to-fastapi`) |
| ASCII enums DPI/CTI (BACK-03) | ✅ Completo (`feat/flask-to-fastapi`) |
| Deploy FastAPI em produção (BACK-04) | ✅ Completo — FastAPI em produção (Render + Supabase); merge em `3.1-dev` |
| Migração Neon → Supabase (DB-02) | ✅ Completo — cold start 45s → 1.5s; per-request connections (PgBouncer) |
| Monitorização (INFRA-01) | ✅ Completo — Sentry frontend + backend ativos; UptimeRobot com email alerts |
| Estratégia de Backups (DB-03) | ✅ Completo — `tools/backup_db.py`; `docs/deploy/ENV_VARS.md` |
| Branch ativo | `3.1-dev` (produção + desenvolvimento) |

Detalhe completo de tudo o que foi implementado: ver [CHANGELOG.md](CHANGELOG.md).

---

## Concluído Recentemente (2026-05-19)

### ✅ DB-03 — Estratégia de Backups (concluído 2026-05-19)

- `tools/backup_db.py` — exporta `users` e `access_log` para JSON timestamped em `tools/backups/` (gitignored); usa psycopg2, sem dependência de pg_dump
- `docs/deploy/ENV_VARS.md` — referência completa de todas as env vars (backend + frontend) por serviço, com indicação de onde obter cada valor
- `docs/plans/subplans/DB-03.md` — subplan com limitações do Supabase free tier e frequência de backup recomendada

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

### AUTH-10 — Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`.

**Importante:** verificação de permissões sempre no backend. Frontend não é segurança.

### SEC-08 — Remover `legacyLogin.ts`

Ficheiro `legacyLogin.ts` lê `VITE_LOGIN_USER_*`/`VITE_LOGIN_PASS_*`. Variáveis `VITE_*` ficam em texto claro no bundle JS. Remover antes de utilizadores externos terem acesso.

### BACK-05 — Validação de Enums nos Schemas Pydantic

Campos de cálculo são `str` livres — payloads malformados podem causar resultados de risco incorretos. Usar `Literal` ou enum Pydantic.

### DB-04 — Migrations Alembic

Versioning de schema com rollback. Remover DDL do arranque da app.

### SEC-07 — Hardening Avatar Upload

Bloquear `data:image/svg+xml` e validar magic bytes em `/auth/profile/avatar`.

### SEC-09 — CSP Header

`Content-Security-Policy` header completo no backend ou proxy.

### INFRA-04 — `/health/db`

Health check com query real à BD para deteção de falha de ligação ao Supabase.

### SEC-04 — Política de Password Hashing

Fixar parâmetros PBKDF2-SHA256 explicitamente ou migrar para Argon2id.

### SEC-05 — Hash de Tokens na BD

Guardar `sha256(token)` em vez do token em claro para tokens de reset e verificação.

### BACK-06 — Error Handler JSON

Envelope uniforme `{"error": "INTERNAL_ERROR"}` para respostas 5xx.

### UI-02 — Página de Documentação

Página de DOCS integrada na app com documentação e manuais de utilização.

### UI-03 — Página de Ajuda

Página HELP integrada na app.

### UI-04 — FAQs

Página de perguntas frequentes integrada na app.

### UI-05 — Bug Report

Formulário de reporte de bugs na app. Canal de destino a definir: e-mail, GitHub Issues ou ClickUp.

---

## Pendente — Prioridade Baixa / Futuro

### INFRA-03 — Dockerfile + Compose

Containerização para deploy reproduzível. Para o Render (PaaS) atual, a ausência não é bloqueante. Relevante para migração futura para VPS/Proxmox.

### SEC-06 — Política de Logs — Sem PII em Produção

Garantir que tokens e PII não são impressos em produção. Verificar que `DEBUG` não está ativo no Render.

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

### TEST-02 — Testes Automatizados

Unit tests, integration tests, e2e tests. Objetivos: estabilidade, prevenção de regressões, validação auth e modelo CHICHORRO.

### INFRA-02 — Pipeline CI/CD

GitHub Actions + Render Deploy Hooks. Objetivos: deploy automático, testes automáticos, linting, validação de build.

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
