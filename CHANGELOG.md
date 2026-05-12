# Changelog

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
- Backend: Python Flask → Render

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
