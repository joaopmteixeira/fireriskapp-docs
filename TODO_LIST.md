# TODO List — Por ID

Listagem completa de todas as ações do projeto, ordenadas por prefixo e número de ID.
Para prioridades e detalhes ver [TODO_PRIORITIES.md](TODO_PRIORITIES.md).

Última atualização: 2026-05-08

Legenda: ✅ concluído · 🔄 em progresso · ❌ pendente

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
| AUTH-07 | ✅ | Rate limiting com Flask-Limiter + Upstash Redis nos endpoints /auth/* | feat/security |
| AUTH-08 | ✅ | Regenerar sessão após login (mitigação session fixation) | feat/security |
| AUTH-09 | ❌ | Editar perfil: username, e-mail, password, apagar conta | — |
| AUTH-10 | ❌ | Sistema de roles/permissões: admin, engineer, viewer, demo | — |
| AUTH-11 | ✅ | Validar modal sessão expirada em produção (apagar cookie) | feat/access-log |
| AUTH-12 | ✅ | Merge `feat/access-log` → `3.1-dev` | 3.1-dev |

---

## DB — Base de Dados e Persistência

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| DB-01 | ✅ | Neon PostgreSQL em produção — env vars, deploy, TEST-01 aprovado | feat/access-log |
| DB-02 | ❌ | Estratégia de backups: PostgreSQL Neon, env vars, configs | — |

---

## SEC — Segurança e Hardening

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| SEC-01 | ✅ | Rever configuração CORS — allow_headers, métodos, max_age, fallback dev explícito | feat/security |
| SEC-02 | ✅ | HTTPS confirmado no Render + HSTS via `@app.after_request` quando `SESSION_SECURE=1` | feat/security |
| SEC-03 | ✅ | X-Content-Type-Options, X-Frame-Options, Referrer-Policy via `@app.after_request`; CSRF coberto por camadas existentes | feat/security |

---

## UI — Interface e Experiência

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| UI-01 | ❌ | Gráfico impacto intervenções (tornado chart, Recharts) | — |
| UI-02 | ❌ | Página de Documentação integrada na app | — |
| UI-03 | ❌ | Página de Ajuda integrada na app | — |
| UI-04 | ❌ | FAQs — Perguntas Frequentes | — |
| UI-05 | ❌ | Bug Report — formulário de reporte (destino: e-mail/GitHub/ClickUp) | — |
| UI-06 | ❌ | Preferências / Definições do utilizador | — |
| UI-07 | ❌ | Dark Mode | — |
| UI-08 | ❌ | Chatbot AI assistente CHICHORRO (Claude API ou similar) | — |

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
| BACK-01 | ❌ | Reestruturar Flask.py em módulos: routes/, services/, models/, auth/, db/ | — |
| BACK-02 | ❌ | Melhorar logging: failed logins, user-agent, request IDs, erros backend | — |
| BACK-03 | ❌ | Avaliar migração Flask → FastAPI (não prioritário) | — |

---

## INFRA — Infraestrutura e DevOps

| ID | Estado | Descrição | Branch |
| --- | --- | --- | --- |
| INFRA-01 | ❌ | Monitorização: Sentry / BetterStack / UptimeRobot | — |
| INFRA-02 | ❌ | Pipeline CI/CD: GitHub Actions + Render Deploy Hooks | — |

---

## TEST — Testes e Validação

| ID | Estado | Descrição |
| --- | --- | --- |
| TEST-01 | ✅ | Teste e2e em produção: registo → e-mail → verificação → login → reset password (aprovado 2026-05-08) |
| TEST-02 | ❌ | Testes automatizados: unit, integration, e2e |

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

## CHICHORRO 3.1 — Implementação (Blocos A/B/C)

Todos os itens concluídos. Detalhe completo em [NEXT_STEPS.md](NEXT_STEPS.md).

| ID | Estado | Descrição |
| --- | --- | --- |
| A1 | ✅ | Análise CTI 3.1 — diferenças identificadas |
| A1b | ✅ | Atualizar Chichorro_CTI.py (assinatura 3.1, sympy fix, paridade 11/11) |
| A3 | ✅ | Batch: substituir POI / ESCI / DPI + completar RI |
| A4 | ✅ | Flask.py + Chichorro_RI_inter.py — endpoints 3.1 + /RI/interv |
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
