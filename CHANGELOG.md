# Changelog

---

## v3.1.1 — Autenticação e segurança (2026-05)

### AUTH-01 — Log de acessos (SQLite)
- Base de dados SQLite (`data/chichorro.db`) com WAL mode para suporte a múltiplos workers
- Tabela `access_log`: registo de eventos `login`/`logout` com username, timestamp UTC e IP
- Endpoints `GET /admin/log` e `GET /admin/users` (requerem autenticação)
- `DB_DIR` configurável via variável de ambiente (suporte a Render Persistent Disk)

### AUTH-02 — Registo de utilizadores com verificação de e-mail
- Tabela `users` com password hashing (`werkzeug.security`), token de verificação e expiração de 24h
- `POST /auth/register` — validação, unicidade e-mail/username, envio de e-mail em thread daemon
- `GET /auth/verify/<token>` — activa conta e redireciona para o frontend com `?verified=ok/expired/invalid/already`
- Envio de e-mail via Flask-Mail (SMTP Resend); fallback para terminal quando `MAIL_SERVER` não está definido
- Link de verificação usa `request.url_root` (URL do backend), não `APP_BASE_URL` (frontend)

### AUTH-03 — Página de registo no frontend
- `SignUpPage.tsx` — formulário com e-mail, username, palavra-passe e confirmação
- Validação PT-PT no browser (`setCustomValidity`)
- Banner de sucesso com redirect para login
- `LoginPage.tsx` — banner `?verified=ok/expired/invalid/already`; link "Criar conta"

### AUTH-04 — Recuperação de palavra-passe
- Colunas `reset_token` e `reset_token_expires_at` adicionadas via migração automática (`_init_db`)
- `POST /auth/forgot-password` — gera token (1h), envia e-mail em background thread; sempre responde `{"ok":true}` (não revela existência do e-mail)
- `POST /auth/reset-password` — valida token, actualiza hash, limpa token
- `ForgotPasswordPage.tsx` e `ResetPasswordPage.tsx` — novas páginas com estilo consistente
- `LoginPage.tsx` — link "Esqueceu a palavra-passe?" e banner `?reset=ok`

### Sessão expirada
- `postJson` despacha `SESSION_EXPIRED_EVENT` em qualquer resposta 401
- `AppLayout` escuta o evento e mostra modal bloqueante: "Sessão expirada — Recarregar página"
- Cobre o caso de cookies apagadas manualmente pelo utilizador

---

## v3.1 — Aplicação Web (2026)

Primeira versão pública do FireRiskApp como aplicação web, implementando o modelo CHICHORRO 3.1.

### Modelo implementado
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

### Funcionalidades de interface
- Navegação por módulos com persistência de sessão (sessionStorage)
- Exportar / importar sessão em formato JSON
- Resultados desatualizados assinalados visualmente (cinzento + aviso âmbar) quando inputs são alterados após cálculo
- Campos obrigatórios em falta com destaque visual e mensagem específica
- Módulo de Intervenções com cálculo de custo estimado (€/m²)

### Stack técnica
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
