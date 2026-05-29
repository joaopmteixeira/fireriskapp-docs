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

- [Visão Geral](project/PROJECT_OVERVIEW.md) — objetivos, stack, estado das fases
- [PRD](project/PRD.md) — requisitos de produto, escopo, critérios de aceitação e roadmap
- [Arquitetura](project/ARCHITECTURE.md) — estrutura de ficheiros, endpoints, sessionStorage
- [Método de Cálculo](method/METODO_CALCULO.md) — fórmulas, fatores e subvariáveis do CHICHORRO

## Desenvolvimento

- [Serviços & APIs](project/SERVICES.md) — Supabase, Sentry, Render, Cloudflare
- [Ferramentas](guides/TOOLS.md) — scripts utilitários em `scripts/`
- [Design](project/DESIGN.md) — paleta, tipografia, componentes
- [Alterações UX/UI](project/FRONTEND_UX_MODIFICATIONS.md) — histórico de melhorias de interface
- [Guia de Utilização](guides/USER_GUIDE.md) — como usar a aplicação
- [Guidelines Backend](guides/BACKEND_GUIDELINES.md) — convenções FastAPI/Python
- [Guidelines Frontend](guides/FRONTEND_GUIDELINES.md) — convenções React/TypeScript

## Infraestrutura

- [Opções de Hosting](deploy/HOSTING_OPTIONS.md) — comparação de plataformas

## Planeamento

- [Próximos Passos](NEXT_STEPS.md) — tarefas em curso e concluídas
- [TODO](TODO.md) — lista de tarefas geral
- [Tarefas por ID](TODO_LIST.md) — tarefas organizadas por ID Linear
- [Tarefas por Prioridade](TODO_PRIORITIES.md) — tarefas ordenadas por prioridade

## Decisões & Histórico

- [Decisões Técnicas](changelog/DECISIONS_LOG.md) — registo de decisões de arquitetura
- [Changelog](changelog/CHANGELOG.md) — histórico de versões e alterações

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
