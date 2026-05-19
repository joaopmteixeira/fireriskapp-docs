# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-05-15

---

## Estado Atual da Arquitetura

### Frontend

- React
- TypeScript
- Vite
- TailwindCSS

### Backend

- Flask (Python)

### Base de Dados

- PostgreSQL (Neon)

### Sistema de Autenticação

- Flask Session Cookies
- Sessões server-side
- Verificação de e-mail
- Recuperação de palavra-passe
- Logging de acessos

---

## Avaliação Geral

O backend atual já apresenta uma arquitetura relativamente moderna e segura.

Já foram identificados:

- hashing de passwords
- proteção SQL injection
- sessões Flask
- verificação e-mail
- reset password
- logging acessos
- frontend desacoplado React

A prioridade atual NÃO deve ser mudar de linguagem ou reescrever tudo.

A prioridade deve ser:

```text
Hardening segurança
+
Melhoria arquitetura
+
Deployment
+
Testes
+
Monitorização
```

---

## Prefixos de ID

- **`AUTH`** — Autenticação e sessões (AUTH-01…05 já concluídos — ver CHANGELOG)
- **`DB`** — Base de dados e persistência
- **`SEC`** — Segurança e hardening (não-auth)
- **`UI`** — Interface e experiência do utilizador
- **`UX`** — Micro-melhorias de experiência (UX-01…08 concluídos — ver CHANGELOG)
- **`FEAT`** — Funcionalidades novas da aplicação
- **`BACK`** — Arquitetura e código backend
- **`INFRA`** — Infraestrutura, deploy e DevOps
- **`TEST`** — Testes e validação
- **`MODEL`** — Modelo CHICHORRO (backlog pós-3.1)

---

## Concluído Recentemente

### ✅ DB-01 — Neon PostgreSQL — Validação em Produção `Prioridade Alta`

Neon configurado no Render ✅ · Deploy verde ✅ · TEST-01 aprovado ✅

### ✅ TEST-01 — Teste End-to-End em Produção `Prioridade Alta`

Fluxo completo validado: registo → e-mail → verificação → login → reset password ✅

### ✅ AUTH-11 — Modal de Sessão Expirada — Validação Produção `Prioridade Baixa`

Modal aparece corretamente ao apagar cookie de sessão manualmente ✅

### ✅ AUTH-12 — Merge `feat/access-log` → `3.1-dev` `Prioridade Alta`

Merge concluído em `3.1-dev` · push para GitHub ✅ · sync docs disparado ✅

### ✅ AUTH-07 — Rate Limiting nos Endpoints de Autenticação `Prioridade Alta`

Flask-Limiter + Upstash Redis EU (free tier) · validado em produção dev ✅ · contadores visíveis no Data Browser Upstash ✅

### ✅ AUTH-08 — Regenerar Sessão Após Login `Prioridade Alta`

`session.clear()` adicionado nos 3 pontos de login em `Flask.py` · mitigação session fixation (OWASP ASVS V3.3) ✅

### ✅ AUTH-06 — Hardening de Cookies de Sessão `Prioridade Alta`

HTTPONLY ✅ · SECURE via `CHICHORRO_SESSION_SECURE=1` ✅ · SAMESITE=Lax ✅ · cookie renomeado para `chichorro_session` (anti-fingerprinting) ✅

### ✅ SEC-01 — Revisão da Configuração CORS `Prioridade Alta`

`allow_headers` restringido a `["Content-Type"]` ✅ · métodos limitados a GET/POST/OPTIONS ✅ · `max_age=86400` ✅ · fallback dev explícito (`localhost:5173`) ✅

### ✅ SEC-02 — HTTPS Obrigatório em Produção `Prioridade Alta`

Render força HTTPS no reverse proxy ✅ · `CHICHORRO_SESSION_SECURE=1` ativo ✅ · HSTS via `@app.after_request` em produção ✅

### ✅ SEC-03 — Headers de Segurança `Prioridade Alta`

`X-Content-Type-Options: nosniff` ✅ · `X-Frame-Options: DENY` ✅ · `Referrer-Policy: strict-origin-when-cross-origin` ✅ · CSRF coberto por camadas existentes ✅ · CSP diferida para Cloudflare Pages ✅

---

## ✅ `feat/security` mergeado em `3.1-dev` (2026-05-12)

Auditoria de segurança e usabilidade concluída. Branch mergeado.

---

## ✅ AUTH-09 — Editar Perfil (concluído 2026-05-13)

Implementação completa em `3.1-dev`:

- **AUTH-09** — Backend: 5 novas rotas (`/auth/profile/username`, `/auth/profile/email`, `/auth/verify-email-change/<token>`, `/auth/profile/password`, `/auth/profile/delete`); migração DB colunas `new_email`, `new_email_token`, `new_email_token_expires_at`; rate limit 5/hora; fix `ALTER TABLE IF NOT EXISTS` → `try/except` para compatibilidade SQLite
- **AUTH-09a** — ProfilePage redesign: card compacto `max-w-sm`, header gradient `brand-900→brand-800`, avatar circular com initials fallback, menu accordion com ícones MDI (`mdiAccount`, `mdiLock`, `mdiAlertCircleOutline`, `mdiLogout`) e chevron animado; modal de eliminação com texto de confirmação
- **AUTH-09b** — Avatar de utilizador: coluna `avatar TEXT` na tabela `users`, rota `POST /auth/profile/avatar` (valida `data:image/`, limite 700 KB base64, rate limit 20/hora), upload frontend com canvas resize 256×256 JPEG 0.85
- **AUTH-09c** — ProfilePage redesign card compacto: 4 rows expansíveis inline (nome de utilizador, e-mail, palavra-passe, apagar conta); pencil overlay no avatar; sem "Zona de perigo" separada; sem botão "Sair"

### ✅ UI-06 — Página de Definições (concluído 2026-05-13)

- `src/lib/prefs.ts` — store de preferências em localStorage; `Prefs = {theme, warnOnExit, decimalPlaces}`; `usePrefs()` hook reactivo via `PREFS_CHANGED_EVENT`; `applyTheme()` com suporte system/claro/escuro
- `SettingsPage.tsx` — 3 secções: Aparência (radio), Sessão (toggle), Resultados (radio casas decimais)
- `AppLayout.tsx` — `shouldWarnOnExit` usa `prefs.warnOnExit`; sidebar username via `/auth/me`
- `tailwind.config.js` — `darkMode: "class"`; paleta ink estendida (400, 800, 950)
- `RiPage.tsx` + `CtiPage.tsx` — `toFixed(getPrefs().decimalPlaces)` em todos os resultados numéricos
- Fix 405 avatar: `_serve_spa_or_asset` em Flask.py exclui agora `auth`, `admin`, `login`, `logout`, `me` do catch-all GET

---

## Prioridade Média

### ❌ UI-02 — Docs — Página de Documentação

Criar página de DOCS na app com documentação e manuais de utilização.

### ❌ UI-03 — Help — Página de Ajuda

Criar página HELP integrada na app.

### ❌ UI-04 — FAQs — Perguntas Frequentes

Criar página de perguntas frequentes.

### ❌ UI-05 — Bug Report — Sistema de Reporte

Sistema de reporte de bugs na app: formulário que o utilizador submete quando encontra um problema. A definir canal de destino: e-mail, GitHub Issues ou ClickUp.

### ✅ AUTH-09 — Editar Perfil *(ver secção de concluídos acima)*

- ✅ AUTH-09 — backend: username, e-mail c/ re-verificação, password, apagar conta, avatar
- ✅ AUTH-09a — ProfilePage: card layout, header gradient, accordion menu, MDI icons
- ✅ AUTH-09b — Avatar: upload canvas resize 256×256, rota Flask, DB
- ✅ AUTH-09c — ProfilePage card compacto: 4 rows expansíveis inline, pencil overlay no avatar

### ✅ UI-06 — Preferências / Definições *(ver secção de concluídos acima)*

### ❌ AUTH-10 — Implementar Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`

**IMPORTANTE:** As permissões devem ser verificadas no backend. Frontend NÃO é segurança.

### ✅ BACK-01 — Migração Flask → FastAPI *(concluído — ver CHANGELOG)*

Migração completa do `Flask.py` para FastAPI com estrutura modular. 11/11 PASS. Branch `feat/flask-to-fastapi`.

### 🔄 BACK-04 — Deploy FastAPI no Render *(em progresso)*

Passos 1-3 concluídos (fixes `database.py`, merge, paridade). Passo 4 (deploy Render) em curso após fixes `itsdangerous` e conexões per-request para Neon free tier.
Ver `docs/plans/BACK-04.md`.

### ✅ BACK-02 — Melhorar Logging *(concluído — ver CHANGELOG)*

### ❌ INFRA-01 — Implementar Monitorização

Possíveis ferramentas: Sentry, BetterStack, UptimeRobot, Grafana, Render monitoring.

**Objetivos:** detetar erros, uptime, debugging, auditoria.

### ✅ DB-03 — Criar Estratégia de Backups *(concluído 2026-05-19)*

`tools/backup_db.py` (export JSON por psycopg2), `docs/deploy/ENV_VARS.md` (referência completa de env vars), `docs/plans/subplans/DB-03.md`.

---

## Prioridade Baixa / Futuro

### 🔄 UI-07 — Dark Mode (em progresso)

Infra concluída: `darkMode: "class"` no Tailwind, `applyTheme()` em `main.tsx`, paleta `ink` estendida.
Componentes com dark mode: sidebar, ProfilePage, SettingsPage, Card, Field, Button, ModuleGlobalValueCard, PoiFactorSection, DpiFactorSection, EsciFactorSection.
**Pendente (UI-07 completo):** RiPage, CtiPage, InterventionsPage, páginas de autenticação (Login, SignUp, ForgotPassword, ResetPassword).

### ❌ FEAT-01 — Gráfico de Impacto de Intervenções

No módulo de Intervenções, mostrar bar chart horizontal (tornado chart) com o impacto individual de cada intervenção selecionada: quanto reduziria o RI se fosse aplicada isoladamente.

- Backend: novo endpoint `POST /RI/interv/impact`
- Frontend: Recharts (já disponível no projeto)
- Custo: ~34 cálculos de RI por chamada (aceitável no backend Python)

### ❌ FEAT-02 — Guardar Edifício

Após cálculo completo, permitir ao utilizador guardar a avaliação associada a um edifício identificado por:

- Nome do projeto (texto livre)
- Morada (texto livre)
- Código postal (formato XXXX-XXX)
- Distrito / Concelho / Freguesia (três dropdowns em cascata; Distrito inclui Regiões Autónomas dos Açores e da Madeira)
- Latitude / Longitude + pin interativo no mapa

Os resultados (POI, CTI, DPI, ESCI, RI) ficam guardados associados ao utilizador e numa tabela geral da base de dados.

### ❌ FEAT-03 — Chatbot AI

Assistente de IA para ajudar os utilizadores a compreender os conceitos do CHICHORRO e a utilizar a aplicação (exclusivamente; possivelmente via Claude API ou similar).

### ❌ TEST-02 — Adicionar Testes Automatizados

**Objetivos:** garantir estabilidade, evitar regressões, validar auth, validar cálculo modelo CHICHORRO.

Tipos: unit tests, integration tests, e2e tests.

### ❌ INFRA-02 — Criar Pipeline CI/CD

**Objetivo:** deploy automático, testes automáticos, linting, validação build.

Possível stack: GitHub Actions + Render Deploy Hooks.

---

## Backlog — Versão Futura (pós-3.1)

Propostas de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1:

- ❌ MODEL-01 — Método simplificado baseado no CHICHORRO 2.0
- ❌ MODEL-02 — Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo)
- ❌ MODEL-03 — Afinação de custos €/m² via PRONIC
- ❌ MODEL-04 — Intervenções adicionais: Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa
- ❌ MODEL-05 — Georreferenciação e base de dados de edifícios
- ❌ MODEL-06 — Tratamento de edifícios devolutos
- ❌ MODEL-07 — Integração com Firecheck 2.0

---

## JWT — Notas Importantes

O projeto atual NÃO usa JWT. Isto NÃO é um problema.

A arquitetura atual (React + Flask + sessões Flask) é totalmente válida.

JWT NÃO é automaticamente:

- mais moderno
- mais seguro
- melhor

Sessões Flask podem até ser mais seguras e simples neste tipo de arquitetura.

---

## Arquitetura Atual Recomendada

Manter:

```text
React
+
Flask Sessions
+
PostgreSQL Neon
```

E focar em: hardening, organização, deployment, testes, monitorização.
