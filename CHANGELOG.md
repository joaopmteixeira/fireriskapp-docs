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
