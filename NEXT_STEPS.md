# Estado do Projeto e Próximos Passos

Última atualização: 2026-05-18

> **Issues tracked in Linear** — team [FireRiskApp](https://linear.app/fireriskapp), projeto **CHICHORRO 3.1** (FIR-5 a FIR-29).
> Usar o Linear como fonte de verdade para estado de tarefas. Este ficheiro mantém-se como referência rápida.

---

## Estado atual

| Área | Estado |
| --- | --- |
| Modelo CHICHORRO 3.1 | ✅ Completo (11/11 paridade backend, e2e aprovado) |
| Autenticação e sessões | ✅ Completo (AUTH-01..09c, AUTH-11, AUTH-12) |
| Hardening de segurança | ✅ Completo (SEC-01..03, feat/security mergeado) |
| Auditoria segurança/UX | ✅ Completo (S-01..02, U-01..04) |
| Perfil de utilizador | ✅ Completo (AUTH-09, AUTH-09a, AUTH-09b, AUTH-09c) |
| Preferências / Definições | ✅ Completo (UI-06: dark mode, avisar-antes-de-sair, casas decimais) |
| Dark Mode (UI-07) | ✅ Completo — todas as páginas cobertas (commit `d2d6492`) |
| Migração Flask → FastAPI (BACK-01) | ✅ Completo — 11/11 PASS (`feat/flask-to-fastapi`) |
| ASCII enums DPI/CTI (BACK-03) | ✅ Completo (`feat/flask-to-fastapi`) |
| Deploy FastAPI em produção (BACK-04) | ✅ Completo — FastAPI em produção (Render + Supabase); merge em `3.1-dev` |
| Migração Neon → Supabase (DB-02) | ✅ Completo — cold start 45s → 1.5s; per-request connections (PgBouncer) |
| Branch ativo | `3.1-dev` (produção + desenvolvimento) |

Detalhe completo de tudo o que foi implementado: ver [CHANGELOG.md](CHANGELOG.md).

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

### AUTH-10 — Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`.

**Importante:** verificação de permissões sempre no backend. Frontend não é segurança.

### UI-06 — Preferências / Definições

Página de configurações do utilizador (conteúdo a especificar).

### INFRA-01 — Monitorização

Ferramentas candidatas: Sentry, BetterStack, UptimeRobot, Render monitoring.
Objetivos: detetar erros, uptime, debugging, auditoria.

### DB-02 — Estratégia de Backups

Garantir backup de: PostgreSQL Neon, env vars, configs de deployment.

---

## Pendente — Prioridade Baixa / Futuro

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

### UI-07 — Dark Mode

Tema escuro na aplicação.

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
