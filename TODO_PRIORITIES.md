# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-05-19

---

## Estado Atual da Arquitetura

### Frontend

- React
- TypeScript
- Vite
- TailwindCSS

### Backend

- FastAPI (Python)

### Base de Dados

- PostgreSQL (Neon)

### Sistema de Autenticação

- Starlette Session Cookies
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
- sessões FastAPI/Starlette
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

slowapi + Upstash Redis EU (free tier) · validado em produção dev ✅ · contadores visíveis no Data Browser Upstash ✅

### ✅ AUTH-08 — Regenerar Sessão Após Login `Prioridade Alta`

Sessao limpa nos pontos de login do backend FastAPI · mitigação session fixation (OWASP ASVS V3.3) ✅

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
- Fix 405 avatar: `_serve_spa_or_asset` no backend FastAPI exclui agora `auth`, `admin`, `login`, `logout`, `me` do catch-all GET

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
- ✅ AUTH-09b — Avatar: upload canvas resize 256×256, rota FastAPI, DB
- ✅ AUTH-09c — ProfilePage card compacto: 4 rows expansíveis inline, pencil overlay no avatar

### ✅ UI-06 — Preferências / Definições *(ver secção de concluídos acima)*

### ❌ AUTH-10 — Implementar Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`

**IMPORTANTE:** As permissões devem ser verificadas no backend. Frontend NÃO é segurança.

### ❌ SEC-08 — Remover `legacyLogin.ts` e Limpar `.env`

Ficheiro `legacyLogin.ts` lê `VITE_LOGIN_USER_*` e `VITE_LOGIN_PASS_*`. Variáveis `VITE_*` são incluídas no bundle JS compilado e ficam visíveis em texto claro no browser. Remover antes de qualquer utilizador externo ter acesso à plataforma.

### ❌ BACK-05 — Validação de Enums/Tamanhos nos Schemas Pydantic

Campos como `POI_CC_Comb`, `DPI_OGS_*` são `str` livres — devem ser `Literal["Sim", "Não"]` ou enum Pydantic. Payloads malformados podem causar cálculos de risco silenciosamente errados.

### ❌ DB-04 — Migrations Alembic

Substituir DDL no arranque da app (`CREATE TABLE`, `ALTER TABLE`) por migrations versionadas com rollback e histórico auditável. Necessário antes de deploy definitivo em produção.

### ❌ SEC-07 — Hardening do Upload de Avatar

Bloquear `data:image/svg+xml` e validar magic bytes em `/auth/profile/avatar`. SVG pode conter JavaScript inline e causar XSS se renderizado diretamente no browser.

### ❌ SEC-09 — CSP Header Completo

Adicionar `Content-Security-Policy` header no backend ou proxy. Bloquear `inline scripts` e `unsafe-eval`. Pré-requisito para deploy com utilizadores externos.

### ❌ INFRA-04 — Endpoint `/health/db`

Health check com query real à BD. O `/health` atual responde `ok` mesmo com BD em baixo — impede restart automático no Render em caso de falha de ligação ao Supabase.

### ❌ SEC-04 — Política Explícita de Password Hashing

Documentar e fixar parâmetros de hashing (`werkzeug` PBKDF2-SHA256 com iterações explícitas, ou migrar para Argon2id). Previne mudança silenciosa se a versão do `werkzeug` mudar.

### ❌ SEC-05 — Hash dos Tokens de Reset/Verificação na BD

Guardar `hashlib.sha256(token).hexdigest()` em vez do token em claro. Previne uso direto de tokens ativos se a BD for comprometida.

### ❌ BACK-06 — Error Handler JSON Normalizado

Envelope uniforme `{"error": "INTERNAL_ERROR"}` para respostas 5xx. O handler atual re-lança a exceção sem garantir formato JSON.

### ✅ BACK-01 — Migração Flask → FastAPI *(concluído — ver CHANGELOG)*

Migracao completa do backend legado para FastAPI com estrutura modular. 11/11 PASS. Branch `feat/flask-to-fastapi`.

### ✅ BACK-04 — Deploy FastAPI no Render *(concluído — ver CHANGELOG)*

### ✅ BACK-02 — Melhorar Logging *(concluído — ver CHANGELOG)*

### ✅ INFRA-01 — Implementar Monitorização *(concluído 2026-05-19)*

Sentry (frontend + backend) + UptimeRobot `/health` a cada 5 min. Session Replay em erros.

### ✅ DB-03 — Criar Estratégia de Backups *(concluído 2026-05-19)*

`tools/backup_db.py` (export JSON por psycopg2), `docs/deploy/ENV_VARS.md` (referência completa de env vars), `docs/plans/subplans/DB-03.md`.

---

## Prioridade Baixa / Futuro

### ❌ INFRA-03 — Dockerfile + Compose

Containerização para deploy reproduzível. Para o Render (PaaS) atual, a ausência não é bloqueante. Relevante para migração futura para VPS/Proxmox.

### ❌ SEC-06 — Política de Logs — Sem PII em Produção

Garantir que tokens e PII não são impressos em produção. Verificar que `DEBUG` não está ativo no Render. Links de reset/verificação devem ser suprimidos quando o provider de e-mail está configurado.

### ✅ UI-07 — Dark Mode *(concluído 2026-05-18 — ver CHANGELOG)*

Todas as páginas cobertas: sidebar, cards POI/DPI/ESCI, ProfilePage, SettingsPage, RiPage, CtiPage, InterventionsPage, páginas de autenticação.

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

### ✅ DOCS-01 — Migrar documentação para VitePress (FIR-31) *(concluído 2026-05-20)*

VitePress ^1.6.4 em produção em `docs.chichorrofireriskapp.joaopmteixeira.net`.
Cloudflare Pages via `fireriskapp-docs` (repo público); sync automático via GitHub Actions.

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

A arquitetura atual (React + FastAPI + sessões Starlette) é totalmente válida.

JWT NÃO é automaticamente:

- mais moderno
- mais seguro
- melhor

Sessões Starlette/FastAPI podem até ser mais seguras e simples neste tipo de arquitetura.

---

## Arquitetura Atual Recomendada

Manter:

```text
React
+
FastAPI + Starlette Sessions
+
PostgreSQL Supabase
```

E focar em: hardening, organização, deployment, testes, monitorização.
