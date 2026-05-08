# TODO — Prioridades

Listagem de tarefas organizada por prioridade. Para listagem completa por ID ver [TODO_LIST.md](TODO_LIST.md).

Última atualização: 2026-05-08

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

---

## Próxima Fase — `feat/security`

Hardening de segurança a implementar num branch dedicado após o merge do AUTH-12.

### ❌ AUTH-06 — Verificar Hardening dos Cookies de Sessão

Confirmar existência das seguintes configurações:

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
```

**Objetivo:** proteção XSS; proteção CSRF parcial; obrigar HTTPS.

### ❌ AUTH-07 — Implementar Rate Limiting

Instalar: `Flask-Limiter`

Aplicar em:

- `/auth/login`
- `/auth/register`
- `/auth/forgot-password`
- `/auth/reset-password`

Exemplo: 5 tentativas login/minuto; 3 resets password/hora.

**Objetivo:** Mitigar brute force, spam e abuso de endpoints auth.

### ❌ AUTH-08 — Regenerar Sessão Após Login

Limpar sessão antiga e regenerar sessão após autenticação bem-sucedida.

**Objetivo:** Mitigar session fixation.

### ❌ SEC-01 — Rever Configuração CORS

Verificar: origins permitidos, credentials, headers, métodos permitidos.

**Objetivo:** Evitar CORS demasiado permissivo e exposição de APIs.

### ❌ SEC-02 — Rever Configuração HTTPS Produção

Garantir: HTTPS obrigatório, redirects HTTP → HTTPS, cookies secure.

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

### ❌ AUTH-09 — Editar Perfil

Área de perfil com as seguintes opções:

- ❌ Alterar nome de utilizador
- ❌ Alterar e-mail (com re-verificação via link enviado para o novo endereço)
- ❌ Alterar palavra-passe (requer palavra-passe atual)
- ❌ Apagar conta — eliminação permanente com dupla confirmação (utilizador tem de escrever texto específico para formalizar o pedido)

### ❌ UI-06 — Preferências / Definições

Página de configurações do utilizador (a especificar com o Claude o que recomenda incluir).

### ❌ AUTH-10 — Implementar Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`

**IMPORTANTE:** As permissões devem ser verificadas no backend. Frontend NÃO é segurança.

### ❌ BACK-01 — Melhorar Estrutura Backend Flask

A estrutura atual está centralizada em `Flask.py`. Objetivo futuro:

```text
backend/
├── routes/
├── services/
├── models/
├── auth/
├── db/
├── utils/
├── middleware/
└── tests/
```

**Benefícios:** manutenção, escalabilidade, legibilidade, testes.

### ❌ BACK-02 — Melhorar Logging

Adicionar: failed logins, IP origem, user-agent, request IDs, logs erro backend.

### ❌ INFRA-01 — Implementar Monitorização

Possíveis ferramentas: Sentry, BetterStack, UptimeRobot, Grafana, Render monitoring.

**Objetivos:** detetar erros, uptime, debugging, auditoria.

### ❌ DB-02 — Criar Estratégia de Backups

Garantir backup de: PostgreSQL Neon, env vars, configs de deployment.

---

## Prioridade Baixa / Futuro

### ❌ UI-07 — Dark Mode

Implementar tema escuro na aplicação.

### ❌ UI-08 — Chatbot AI

Assistente de IA para ajudar os utilizadores a compreender os conceitos do CHICHORRO e a utilizar a aplicação (exclusivamente; possivelmente via Claude API ou similar).

### ❌ UI-01 — Gráfico de Impacto de Intervenções

No módulo de Intervenções, mostrar bar chart horizontal (tornado chart) com o impacto individual de cada intervenção selecionada: quanto reduziria o RI se fosse aplicada isoladamente.

- Backend: novo endpoint `POST /RI/interv/impact`
- Frontend: Recharts (já disponível no projeto)
- Custo: ~34 cálculos de RI por chamada (aceitável no backend Python)

### ❌ BACK-03 — Avaliar Migração Flask → FastAPI

**NÃO prioritário. Flask continua válido.**

FastAPI vantagens: tipagem moderna, OpenAPI automático, melhor async, arquitetura moderna.

Só considerar quando: backend crescer bastante, APIs aumentarem, necessidade async real, múltiplos serviços.

### ❌ TEST-02 — Adicionar Testes Automatizados

**Objetivos:** garantir estabilidade, evitar regressões, validar auth, validar cálculo modelo CHICHORRO.

Tipos: unit tests, integration tests, e2e tests.

### ❌ INFRA-02 — Criar Pipeline CI/CD

**Objetivo:** deploy automático, testes automáticos, linting, validação build.

Possível stack: GitHub Actions + Render Deploy Hooks.

### ❌ SEC-03 — Melhorar Segurança Geral

Investigar: CSRF tokens, Content Security Policy (CSP), Helmet headers equivalentes Flask, proteção APIs admin.

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
