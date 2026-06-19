# Estado do Projeto — CHICHORRO 3.1

> Gerado por `/plans-missing` em 2026-06-19.
> Fonte: `docs/TODO_LIST.md` · Subplans: `docs/plans/subplans/`

## Tarefas

| ID | FIR | Descrição | Estado | Plano | Data |
| --- | --- | --- | --- | --- | --- |
| SEC-14 | — | SOPS + age — gestão de secrets encriptados em Git | ❌ Pendente | [✅ Sim](plans/subplans/SEC/SEC-14_UNDONE.md) | — |
| UI-02 | — | Página de Documentação integrada na app | ❌ Pendente | ❌ Não | — |
| UI-03 | — | Página de Ajuda integrada na app | ❌ Pendente | ❌ Não | — |
| UI-04 | — | FAQs — Perguntas Frequentes | ❌ Pendente | ❌ Não | — |
| UI-05 | — | Bug Report — formulário de reporte (e-mail/GitHub/ClickUp) | ❌ Pendente | ❌ Não | — |
| UI-07 | — | Dark Mode — revisão completa de todas as vistas | ❌ Pendente | [✅ Sim](plans/subplans/UI/UI-07_UNDONE.md) | — |
| UI-08 | FIR-33 | Ícones ℹ️ nos subfatores — painel com descrição e tabela RT-SCIE | ❌ Pendente | ❌ Não | — |
| UI-09 | — | Badge de lápis persistente no avatar (mobile-friendly) | ❌ Pendente | [✅ Sim](plans/subplans/UI/UI-09_UNDONE.md) | — |
| UI-10 | — | Sidebar direita persistente — resumo da sessão e subfatores | ❌ Pendente | ❌ Não | — |
| UI-11 | FIR-52 | Formulário de suporte técnico na LoginPage | ❌ Pendente | [✅ Sim](plans/subplans/UI/UI-11_UNDONE.md) | — |
| UI-12 | FIR-53 | Modal "Sobre" na LoginPage | ❌ Pendente | [✅ Sim](plans/subplans/UI/UI-12_UNDONE.md) | — |
| FEAT-01 | FIR-24 | Gráfico de impacto de intervenções (tornado chart, Recharts) | ❌ Pendente | ❌ Não | — |
| FEAT-02 | FIR-25 | Guardar edifício — morada, GPS, resultados por utilizador | ❌ Pendente | [✅ Sim](plans/subplans/FEAT/FEAT-02_UNDONE.md) | — |
| FEAT-03 | FIR-26 | Chatbot AI assistente CHICHORRO (Claude API ou similar) | ❌ Pendente | ❌ Não | — |
| FEAT-04 | — | Geração de relatório em PDF após cálculo completo | ❌ Pendente | ❌ Não | — |
| TEST-04 | — | Smoke tests Docker Compose — health, login, logout, CSRF, build | ❌ Pendente | [✅ Sim](plans/subplans/TEST/TEST-04_UNDONE.md) | — |
| CALC-AUDIT | — | Golden tests do código de cálculo vs. tese3.1 (~280 tests) | ❌ Pendente | ❌ Não | — |
| MODEL-01 | — | Método simplificado baseado no CHICHORRO 2.0 | ❌ Pendente | ❌ Não | — |
| MODEL-02 | — | Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo) | ❌ Pendente | ❌ Não | — |
| MODEL-03 | — | Afinação de custos €/m² via PRONIC | ❌ Pendente | ❌ Não | — |
| MODEL-04 | — | Intervenções adicionais: Gerador, Bombagem, Cablagem, Evacuação | ❌ Pendente | ❌ Não | — |
| MODEL-05 | — | Georreferenciação e base de dados de edifícios | ❌ Pendente | ❌ Não | — |
| MODEL-06 | — | Tratamento de edifícios devolutos | ❌ Pendente | ❌ Não | — |
| MODEL-07 | — | Integração com Firecheck 2.0 | ❌ Pendente | ❌ Não | — |
| AI-02a | — | Curation manual do vault Obsidian — definições, verificar fontes | ❌ Pendente | [✅ Sim](plans/subplans/AI/AI-02a_UNDONE.md) | — |
| AI-03 | — | RAG — pgvector + routers/rag.py + botão "Explicar" por subfator | ❌ Pendente | ❌ Não | — |
| REL-01 | — | Release baseline v3.1.0 — tag git, release notes, snapshot estável | ✅ Concluído | [✅ Sim](plans/subplans/REL/REL-01.md) | 2026-06-12 |
| AUTH-01 | — | Log de acessos — tabela `access_log`, `/admin/log`, `/admin/users` | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-01.md) | — |
| AUTH-02 | — | Registo com verificação de e-mail (Resend SDK, thread daemon) | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-02.md) | — |
| AUTH-03 | — | Frontend de registo — SignUpPage, banners LoginPage | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-03.md) | — |
| AUTH-04 | — | Recuperação de palavra-passe — ForgotPasswordPage, ResetPasswordPage | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-04.md) | — |
| AUTH-05 | — | Modal "sessão expirada" — SESSION_EXPIRED_EVENT, AppLayout | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-05.md) | — |
| AUTH-06 | — | Hardening cookies: HTTPONLY, SECURE, SAMESITE + anti-fingerprinting | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-06.md) | 2026-05-22 |
| AUTH-07 | — | Rate limiting slowapi + Upstash Redis + fail-fast Redis | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-07.md) | 2026-05-22 |
| AUTH-08 | — | Regenerar sessão após login (mitigação session fixation) | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-08.md) | 2026-05-22 |
| AUTH-09 | — | Editar perfil: backend routes (username, e-mail, password, apagar) | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-09.md) | 2026-05-13 |
| AUTH-09a | — | ProfilePage redesign — card layout, accordion, ícones MDI | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-09a.md) | 2026-05-13 |
| AUTH-09b | — | Avatar — coluna DB, rota upload, canvas resize | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-09b.md) | 2026-05-13 |
| AUTH-09c | — | ProfilePage card compacto — 4 rows expansíveis inline | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-09c.md) | 2026-05-13 |
| AUTH-09d | — | Avatar WebP 128 px, limite 100 KB — reduz armazenamento ~80% | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-09d.md) | 2026-06-12 |
| AUTH-10 | — | Sistema de roles/permissões: `role`, `require_admin`, admin UI | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-10.md) | 2026-05-26 |
| AUTH-11 | — | Validar modal sessão expirada em produção | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-11.md) | 2026-05-08 |
| AUTH-12 | — | Merge feat/access-log → 3.1-dev | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-12.md) | 2026-05-08 |
| AUTH-13 | — | Hardening sessão: max_age, Secure flag, CSRF protection | ✅ Concluído | [✅ Sim](plans/subplans/AUTH/AUTH-13.md) | 2026-05-18 |
| DB-01 | — | Neon PostgreSQL em produção | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-01.md) | 2026-05-08 |
| DB-02 | — | Migração Neon → Supabase — elimina cold start 45s | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-02.md) | 2026-05-15 |
| DB-03 | — | Estratégia de backups — scripts, GitHub Actions, restore | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-03.md) | 2026-05-22 |
| DB-04 | — | Migrations Alembic — versioning de schema, rollback | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-04.md) | 2026-05-22 |
| DB-05 | — | Least privilege DB — chichorro_runtime, DATABASE_URL_MIGRATIONS | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-05.md) | 2026-05-24 |
| DB-06 | — | SQLAlchemy ORM — autogenerate Alembic, connection pooling | ✅ Concluído | ❌ Não | 2026-06-09 |
| DB-07 | — | Backups PostgreSQL local — cron diário, restore testado | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-07.md) | 2026-06-15 |
| DB-08 | — | Runbook migração Supabase → PostgreSQL local | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-08.md) | 2026-06-15 |
| DB-09 | — | Roles BD (admin/runtime/readonly) + backups diferenciados | ✅ Concluído | [✅ Sim](plans/subplans/DB/DB-09.md) | 2026-06-17 |
| SEC-01 | — | CORS estrito em produção | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-01.md) | 2026-05-22 |
| SEC-02 | — | HTTPS obrigatório em produção — fail-fast URLs | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-02.md) | 2026-05-21 |
| SEC-03 | — | X-Content-Type-Options, X-Frame-Options, Referrer-Policy | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-03.md) | 2026-05-12 |
| SEC-04 | — | Argon2id password hashing + upgrade-on-login | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-04.md) | 2026-05-27 |
| SEC-05 | — | SHA-256 tokens de reset/verificação na BD | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-05.md) | 2026-05-27 |
| SEC-06 | — | Política de logs — sem tokens/PII em produção | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-06.md) | 2026-05-22 |
| SEC-07 | — | Magic bytes no upload de avatar (JPEG/PNG/WebP/GIF) | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-07.md) | 2026-05-27 |
| SEC-08 | — | Remover legacyLogin.ts e VITE_LOGIN_* do .env | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-08.md) | 2026-05-21 |
| SEC-09 | — | CSP + Permissions-Policy backend e Cloudflare Pages | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-09.md) | 2026-05-22 |
| SEC-10 | — | Fail-fast secrets em produção | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-10.md) | 2026-05-21 |
| SEC-11 | — | Gestão de secrets — política, rotação, backup Bitwarden | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-11.md) | 2026-06-16 |
| SEC-12 | — | Nginx Basic Auth para pgAdmin/Adminer | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-12.md) | 2026-06-16 |
| SEC-13 | — | Docker hardening: Gitleaks CI, redes internas, migrate, systemd | ✅ Concluído | [✅ Sim](plans/subplans/SEC/SEC-13.md) | 2026-06-18 |
| UI-06 | — | Preferências / Definições — dark mode, avisar antes de sair | ✅ Concluído | [✅ Sim](plans/subplans/UI/UI-06.md) | 2026-05-13 |
| UX-01 | — | Campos em falta com ring vermelho; card "Valor desatualizado" | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-01.md) | — |
| UX-02 | — | Aviso vermelho na RiPage quando inputs mudam após cálculo | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-02.md) | — |
| UX-03 | — | Colapsar/expandir subfatores com botão chevron animado | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-03.md) | — |
| UX-04 | — | Persistência do estado colapsado em sessionStorage | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-04.md) | — |
| UX-05 | — | Aviso de sucesso com fade (3s) na RiPage | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-05.md) | — |
| UX-06 | — | Persistência de error/warning/stale entre navegações | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-06.md) | — |
| UX-07 | — | Warning âmbar ao limpar subfator; banner ERRO na RiPage | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-07.md) | — |
| UX-08 | — | Auto-atualização de resultados na RiPage | ✅ Concluído | [✅ Sim](plans/subplans/UX/UX-08.md) | — |
| BACK-01 | — | Migração Flask → FastAPI: routers, schemas, services, uvicorn | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-01.md) | 2026-05-14 |
| BACK-02 | — | Melhorar logging: failed logins, user-agent, request IDs | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-02.md) | 2026-05-12 |
| BACK-03 | — | ASCII enum values — remover ç/ã dos values DPI e aliases CTI | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-03.md) | 2026-05-14 |
| BACK-04 | — | Deploy FastAPI no Render (Supabase, 1.5s login) | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-04.md) | 2026-05-15 |
| BACK-05 | — | Pydantic Literal types nos schemas DPI/ESCI/CTI/POI | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-05.md) | 2026-05-27 |
| BACK-06 | — | Error handler JSON normalizado — JSONResponse 500 | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-06.md) | 2026-05-27 |
| BACK-07 | — | Naming de rotas API — aliases legacy removidos | ✅ Concluído | [✅ Sim](plans/subplans/BACK/BACK-07.md) | 2026-05-24 |
| INFRA-01 | — | Sentry (frontend + backend) + UptimeRobot + X-Request-ID | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-01.md) | 2026-05-19 |
| INFRA-02 | — | Pipeline CI/CD: GitHub Actions test.yml + build.yml | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-02.md) | 2026-05-27 |
| INFRA-03 | — | Dockerfile + Compose local/prod — containerização | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-03.md) | 2026-06-09 |
| INFRA-04 | — | Endpoint /health/db — query real à BD | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-04.md) | 2026-05-22 |
| INFRA-05 | — | Cache-Control headers: no-store + assets immutable | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-05.md) | 2026-05-22 |
| INFRA-06 | — | Separação de ambientes + deploy Proxmox/Debian 13 | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-06.md) | 2026-06-11 |
| INFRA-07 | — | Staging Proxmox completo — Nginx + PostgreSQL local | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-07.md) | 2026-06-15 |
| INFRA-08 | — | Monitorização self-hosted: health, disco, backup + alertas Resend | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-08.md) | 2026-06-18 |
| INFRA-09 | — | Cloudflare Tunnel — chichorro.joaopmteixeira.net HTTPS | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-09.md) | 2026-06-15 |
| INFRA-10 | — | pgAdmin removido, Adminer em porta 5050 | ✅ Concluído | [✅ Sim](plans/subplans/INFRA/INFRA-10.md) | 2026-06-17 |
| TEST-01 | — | Teste e2e em produção: registo → verificação → login → reset | ✅ Concluído | [✅ Sim](plans/subplans/TEST/TEST-01.md) | 2026-05-08 |
| TEST-02 | — | Testes automatizados: pytest 12/12 | ✅ Concluído | [✅ Sim](plans/subplans/TEST/TEST-02.md) | 2026-05-27 |
| TEST-03 | — | Parity checker + 338 golden tests Literal | ✅ Concluído | [✅ Sim](plans/subplans/TEST/TEST-03.md) | 2026-05-28 |
| DOCS-01 | — | VitePress — docs.chichorrofireriskapp.joaopmteixeira.net | ✅ Concluído | [✅ Sim](plans/subplans/DOCS/DOCS-01.md) | 2026-05-20 |
| DOCS-02 | — | Uniformizar headers de todos os subplans | ✅ Concluído | [✅ Sim](plans/subplans/DOCS/DOCS-02.md) | 2026-05-28 |
| AI-01 | FIR-34 | Setup Graphify — grafos backend, frontend, cross-stack | ✅ Concluído | [✅ Sim](plans/subplans/AI/AI-01.md) | 2026-06-01 |
| AI-02 | FIR-35 | Setup Obsidian vault — 50 notas, 27 subfatores × 8 fontes | ✅ Concluído | [✅ Sim](plans/subplans/AI/AI-02.md) | 2026-06-05 |
| B-01 | — | Consolidação docs de deploy e naming de rotas API | ✅ Concluído | [✅ Sim](plans/subplans/B/B-01.md) | 2026-05-24 |

---

## Workflow Atual

**Sem tarefa ativa** neste momento.

**Próximas 3 sugestões:**

1. **UI-08** (FIR-33) — ícones ℹ️ nos subfatores; maior impacto imediato para utilizadores sem formação no modelo
2. **UI-05** — formulário de Bug Report; complementa UI-11 (suporte técnico) e fecha o ciclo de feedback
3. **FEAT-01** (FIR-24) — gráfico tornado de intervenções; backend já tem os dados, Recharts já no projeto

> CALC-AUDIT = bloqueado até Excel da tese3.1 disponível.
> MODEL-01…07 = backlog pós-3.1, fora do âmbito atual.

---

*Total: 97 · Em Progresso: 0 · Pendentes: 26 · Concluídos: 71 · Com plano: 78*
