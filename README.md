# FireRiskApp

**Avaliação de risco de incêndio em edifícios históricos**

FireRiskApp é uma aplicação web que implementa o método **CHICHORRO** (FEUP) para calcular o Risco de Incêndio (RI) em edifícios existentes com valor patrimonial.

O método combina quatro fatores independentes:

```text
RI = f(POI, CTI, DPI, ESCI)
```

| Fator | Descrição |
| --- | --- |
| **POI** | Potencial Ocorrência de Incêndio |
| **CTI** | Consequências do Incêndio para os Utilizadores |
| **DPI** | Desenvolvimento e Propagação do Incêndio |
| **ESCI** | Eficácia de Socorro e Combate ao Incêndio |

O resultado é classificado numa escala de 12 classes, de **A++** (risco muito baixo) a **F** (risco muito elevado).

---

## Projeto

- [Visão Geral](PROJECT_OVERVIEW.md) — objetivos, stack, estado das fases
- [PRD](PRD.md) — requisitos de produto, escopo, critérios de aceitação e roadmap
- [Arquitetura](ARCHITECTURE.md) — estrutura de ficheiros, endpoints, sessionStorage
- [Método de Cálculo](METODO_CALCULO.md) — fórmulas, fatores e subvariáveis do CHICHORRO
- [Histórico do Método](HISTORY_AI.md) — evolução das versões CHICHORRO 2.0 → 3.1

## Desenvolvimento

- [Guia Local](DEV_LOCAL.md) — como correr o projeto em desenvolvimento
- [Serviços & APIs](SERVICES.md) — Supabase, Sentry, Render, Cloudflare
- [Ferramentas](TOOLS.md) — scripts utilitários em `tools/`
- [Design](DESIGN.md) — paleta, tipografia, componentes
- [Alterações UX/UI](FRONTEND_UX_MODIFICATIONS.md) — histórico de melhorias de interface
- [Guia de Utilização](USER_GUIDE.md) — como usar a aplicação
- [Guidelines Backend](guidelines/BACKEND_GUIDELINES.md) — convenções FastAPI/Python
- [Guidelines Frontend](guidelines/FRONTEND_GUIDELINES.md) — convenções React/TypeScript

## Deploy & Infraestrutura

- [Opções de Hosting](HOSTING_OPTIONS.md) — comparação de plataformas
- [Deploy](deploy/DEPLOY.md) — passos de deploy em Render e Cloudflare Pages
- [Variáveis de Ambiente](deploy/ENV_VARS.md) — todas as variáveis necessárias

## Planeamento

- [Próximos Passos](NEXT_STEPS.md) — tarefas em curso e concluídas
- [TODO](TODO.md) — lista de tarefas geral
- [Tarefas por ID](TODO_LIST.md) — tarefas organizadas por ID Linear
- [Tarefas por Prioridade](TODO_PRIORITIES.md) — tarefas ordenadas por prioridade
- [Plano Auth](plans/main/AUTH_PLAN.md) — plano de autenticação
- [Plano Segurança](plans/main/SECURITY_PLAN.md) — plano de segurança

## Decisões & Histórico

- [Decisões Técnicas](DECISIONS_LOG.md) — registo de decisões de arquitetura
- [Changelog](CHANGELOG.md) — histórico de versões e alterações
- [Avaliação de Segurança](security/SECURITY_ASSESSMENT.md) — análise de riscos
- [Auditoria Inicial](security/SECURITY_AUDIT_INITIAL.md) — auditoria de segurança inicial
- [Auditoria 2026-05-12](audits/AUDIT-2026-05-12.md) — auditoria mais recente

## Migração v3.1

- [Mapeamento Backend](migration/PAGE_BACKEND_MAPPING.md) — páginas ↔ endpoints
- [Diff Analysis](migration/V3_1_DIFF_ANALYSIS.md) — diferenças entre v3.0 e v3.1
- [Matriz de Correspondência](migration/V3_1_MATCHUP_MATRIX.md) — variáveis v3.0 vs v3.1

---

## Versão atual

**v3.1** — implementação completa do modelo CHICHORRO 3.1 (dissertação Rui Sobral, 2019).

- Backend: Python FastAPI/ASGI → Render
- Frontend: React + TypeScript + Vite + Tailwind CSS → Cloudflare Pages

---

## Autores

- **João Teixeira** — CHICHORRO v3.0, arquitetura da aplicação web
- **Rui Sobral** — CHICHORRO v3.1 (dissertação FEUP, 2019)
- **Ricardo Ferreira** — CHICHORRO v2.0 (base do método simplificado, Fase 3)
