# Architecture

## Estrutura de repositório

```text
chichorro4Cursor/
├── app/
│   ├── frontend/src/
│   │   ├── pages/
│   │   │   ├── AppLayout.tsx            → layout + navegação pós-login
│   │   │   ├── LoginPage.tsx            → autenticação
│   │   │   ├── PoiPage.tsx              → /app/poi
│   │   │   ├── CtiPage.tsx              → /app/cti  (inputs numéricos, física complexa)
│   │   │   ├── DpiPage.tsx              → /app/dpi
│   │   │   ├── EsciPage.tsx             → /app/esci
│   │   │   ├── RiPage.tsx               → /app/resultados
│   │   │   ├── InterventionsPage.tsx    → /app/interventions
│   │   │   └── PlaceholderPage.tsx      → páginas em construção
│   │   ├── auth/
│   │   │   ├── AuthPendingScreen.tsx    → estado intermédio de autenticação
│   │   │   ├── legacyLogin.ts           → compatibilidade transitória com fluxo antigo
│   │   │   └── session.ts               → gestão de sessão
│   │   ├── routes/
│   │   │   └── RequireAuth.tsx          → guard: protege páginas autenticadas
│   │   ├── components/
│   │   │   ├── poi/
│   │   │   │   ├── PoiFactorSection.tsx
│   │   │   │   └── poiDefinitions.ts
│   │   │   ├── dpi/
│   │   │   │   ├── DpiFactorSection.tsx
│   │   │   │   └── dpiDefinitions.ts
│   │   │   ├── esci/
│   │   │   │   ├── EsciFactorSection.tsx
│   │   │   │   └── esciDefinitions.ts
│   │   │   └── ui/
│   │   │       ├── Button.tsx
│   │   │       ├── Card.tsx             → CardHeader aceita prop `right` para conteúdo alinhado à direita
│   │   │       ├── Field.tsx
│   │   │       └── ModuleGlobalValueCard.tsx
│   │   └── lib/
│   │       ├── api.ts                   → postJson helper, VITE_API_BASE_URL
│   │       └── resultsStore.ts          → sessionStorage + eventos globais
│   └── backend/
│       ├── main.py                      → FastAPI app, middleware, routers, SPA serving
│       ├── config.py                    → pydantic-settings (Settings)
│       ├── database.py                  → _get_db() dual-mode SQLite/PostgreSQL
│       ├── deps.py                      → Depends: require_auth
│       ├── _limiter.py                  → instância slowapi partilhada
│       ├── routers/
│       │   ├── auth.py                  → /auth/*, /login, /logout, /me (16 rotas)
│       │   ├── admin.py                 → /admin/users, /admin/log
│       │   ├── poi.py                   → /POI/* + /POI (13 rotas)
│       │   ├── cti.py                   → /CTI/* + /CTI (4 rotas)
│       │   ├── dpi.py                   → /DPI/* + /DPI (6 rotas)
│       │   ├── esci.py                  → /ESCI/* + /ESCI (8 rotas)
│       │   └── ri.py                    → /RI, /RI/interv (3 rotas)
│       ├── schemas/
│       │   ├── auth.py                  → modelos de auth e perfil
│       │   ├── poi.py                   → POICCRequest … POIRequest
│       │   ├── cti.py                   → CTIPayload com @model_validator
│       │   ├── dpi.py                   → DPIREICRequest … DPIRequest
│       │   ├── esci.py                  → ESCIGPRequest … ESCIRequest
│       │   └── ri.py                    → RIRequest, RIIntervRequest
│       ├── services/
│       │   └── email.py                 → send_verification_email, send_reset_email, …
│       ├── calc/
│       │   ├── Chichorro_POI.py
│       │   ├── Chichorro_CTI.py         → física complexa, numpy/sympy
│       │   ├── Chichorro_DPI.py
│       │   ├── Chichorro_ESCI.py
│       │   ├── Chichorro_RI.py
│       │   └── Chichorro_RI_inter.py    → RI pós-intervenção (34 intervenções)
│       ├── wsgi.py                      → entrypoint de deployment (uvicorn/gunicorn)
│       └── parity_runner.py             → validação de paridade entre versões
├── reference/
│   ├── chichorro-3.0-jt/               → legacy v3.0 (autor: João Teixeira)
│   ├── chichorro-3.1-rs/               → referência v3.1 (autor: Rui Sobral)
│   └── chichorro-2.0-rf/               → referência v2.0 (autores: RF + Bruno Silva)
└── docs/
    ├── PROJECT_OVERVIEW.md             → o quê, porquê, estado, modelo, fases
    ├── ARCHITECTURE.md                 → este ficheiro — como o código está organizado
    ├── NEXT_STEPS.md                   → tarefas em curso, estado, decisões
    ├── FRONTEND_UX_MODIFICATIONS.md   → registo cronológico de alterações UX/UI
    ├── DECISIONS_LOG.md               → decisões técnicas passadas com contexto
    ├── guidelines/
    │   ├── FRONTEND_GUIDELINES.md
    │   └── BACKEND_GUIDELINES.md
    ├── migration/
    │   ├── V3_1_MATCHUP_MATRIX.md     → estado de implementação 3.0→3.1 por campo
    │   ├── V3_1_DIFF_ANALYSIS.md
    │   └── PAGE_BACKEND_MAPPING.md
    ├── ai/
    │   ├── prompt.md                   → template de prompt para agentes AI
    │   └── handoffs/                   → handoffs por tarefa (A1, A2, …, B5, …)
    ├── deploy/
    │   └── DEPLOY.md
    └── research/
        ├── tese_extract_3.0.txt        → extrato da dissertação de João Teixeira (3.0)
        ├── tese_extract_3.1.txt        → extrato da dissertação de Rui Sobral (3.1)
        └── *.pdf                       → dissertações em PDF
```

---

## Padrão FactorSection (POI / DPI / ESCI)

Cada módulo POI/DPI/ESCI segue este padrão de dois ficheiros:

**`*definitions.ts`** — declaração estática de todos os subfatores:

```ts
{ key, title, resultKey, formKey, fields: [...] }
```

- `fields[]` tem `key`, `label`, `type` (select/number), `options[]`, `visibleWhen` (string JS avaliada)
- Toda a lógica de visibilidade condicional está aqui — o componente só avalia

**`*FactorSection.tsx`** — componente genérico que recebe uma definição e:

- Gere form state (`values`) inicializado do sessionStorage
- Aplica `visibleWhen` para mostrar/esconder campos
- Faz POST ao backend com o payload do subfator
- Guarda resultado em `resultsStore` (fator + módulo global)
- Persiste estados `error`, `warning`, `isResultStale`, `missingFieldKey` em sessionStorage

Se CTI ou RI precisarem do mesmo padrão, seguir esta convenção.

---

## `resultsStore.ts` — sessionStorage keys

| Chave sessionStorage | Conteúdo |
|-----------------------------------------|-------------------------------------------------------|
| `chichorro:module-results` | `{ poi, cti, dpi, esci }` — último valor global válido por módulo |
| `chichorro:module-results-stale` | Idem, mas para o último valor antes de ser invalidado |
| `chichorro:module-factor-results` | Resultado por subfator `{ poi: { POI_CC: 1.2, … }, … }` |
| `chichorro:module-inputs` | Inputs submetidos por módulo |
| `chichorro:form:<formKey>` | Estado atual do formulário de cada subfator |
| `chichorro:computed:<key>` | Resultados intermédios calculados (ex: CI, VHE, VVE) |
| `chichorro:session-storage-hydrated` | Flag: sessão importada de JSON |
| `collapse:<module>:<subfactorKey>` | Estado colapsado/expandido de cada cartão de subfator |
| `err:<formKey>` / `warn:<formKey>` | Mensagem de erro/aviso persistida entre navegações |
| `miss:<formKey>` | Campo em falta (key do input) persistido |
| `stale:<formKey>` | Flag `isResultStale` persistida |

**Eventos globais (window):**

- `chichorro:module-results-updated` — disparado quando `module-results` ou `module-factor-results` mudam
- `chichorro:session-data-updated` — disparado quando inputs de módulo mudam (usado pela RiPage para detetar invalidação)

---

## Endpoints FastAPI

| Endpoint | Método | Descrição |
| -------------------------------- | ------ | -------------------------------------------- |
| `/health` | GET | Health check |
| `/POI/CC` … `/POI/ATIV` | POST | Subfatores POI individuais |
| `/POI` | POST | Calcula todos os subfatores POI + valor global |
| `/CTI/CTI_CI`, `/CTI/CTI_VHE`, `/CTI/CTI_VVE` | POST | Subfatores CTI individuais |
| `/CTI` | POST | Calcula CI, VHE, VVE e valor global CTI |
| `/DPI/REIC` … `/DPI/OGS` | POST | Subfatores DPI individuais |
| `/DPI` | POST | Calcula todos os subfatores DPI + valor global |
| `/ESCI/GP` … `/ESCI/CPB` | POST | Subfatores ESCI individuais |
| `/ESCI` | POST | Calcula todos os subfatores ESCI + valor global |
| `/RI` | POST | Calcula RI final a partir dos 4 módulos |
| `/RI/interv` | POST | Calcula RI pós-intervenção (34 intervenções) |
| `/auth/login`, `/login` | POST | Autenticação (cookie `chichorro_session`) |
| `/auth/logout`, `/logout` | POST | Terminar sessão |
| `/auth/me` | GET | Estado da sessão + username/email/avatar |
| `/me` | GET | Estado da sessão (legado) |
| `/auth/register` | POST | Registo de utilizador + e-mail de verificação |
| `/auth/verify/{token}` | GET | Ativação de conta |
| `/auth/forgot-password` | POST | Gerar token de reset de password |
| `/auth/reset-password` | POST | Redefinir password com token |
| `/auth/profile/username` | POST | Alterar username |
| `/auth/profile/email` | POST | Alterar e-mail (com verificação) |
| `/auth/profile/password` | POST | Alterar password |
| `/auth/profile/delete` | POST | Eliminar conta |
| `/auth/profile/avatar` | POST | Atualizar avatar (base64) |
| `/auth/verify-email-change/{token}` | GET | Confirmar alteração de e-mail |
| `/admin/users` | GET | Lista de utilizadores (requer auth) |
| `/admin/log` | GET | Log de acessos (requer auth) |

---

## Regra operacional

Cada tarefa deve indicar explicitamente o seu modo:

- `active_build` → editar `app/frontend/` e/ou `app/backend/`
- `v3_0_legacy_compare` → ler `reference/chichorro-3.0-jt/`
- `v3_1_matchup` → ler `reference/chichorro-3.1-rs/`; implementar em `app/`
- `v4_0_research` → ler `reference/chichorro-2.0-rf/`; não alterar base ativa sem decisão

Sem esta distinção, o risco de alterar o sítio errado é alto.
