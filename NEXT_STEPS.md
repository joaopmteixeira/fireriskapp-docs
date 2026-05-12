# Estado do Projeto e Próximos Passos

Última atualização: 2026-05-08
Estado: CHICHORRO 3.1 implementado (Blocos A+B+C1 ✅). Autenticação completa (AUTH-01…12 ✅) mergeada em `3.1-dev`. Hardening ativo (AUTH-07 ✅, AUTH-08 ✅, AUTH-06 ✅). Branch ativo: `feat/security`. Próximo: SEC-01 (CORS review), SEC-02 (HTTPS).

---

## Fase atual: v3_1_matchup — implementação

A análise completa está em `docs/migration/V3_1_DIFF_ANALYSIS.md`.
As decisões técnicas estão registadas em `docs/ai/DECISIONS_LOG.md`.
O registo de alterações UX/UI está em `docs/FRONTEND_UX_MODIFICATIONS.md`.

---

## Tarefas por ordem de execução recomendada

### Bloco A — Backend (sem dependências de frontend)

#### A1. ✅ Análise CTI 3.1 — CONCLUÍDA

**Resultado:** diferenças encontradas. Ver `V3_1_MATCHUP_MATRIX.md` secção CTI.
**Pontos críticos identificados:**

- `RI_interv_21_efetivo`: novo parâmetro injetado pelo módulo de intervenções (default `0` no fluxo normal)
- `VHE_Dispositivos` / `VVE_Dispositivos`: dispositivos separados por veia em vez de global
- **Bug crítico no ativo:** `Symbol`/`solve` chamados sem `import sympy` no ramo `SistemaExtincao == 'Com'`
- Refactors locais do ativo (fumo, clarabóia, VVE ascendente) devem ser preservados — CTI não pode ser substituição direta

#### A1b. ✅ Atualizar Chichorro_CTI.py — CONCLUÍDO

**Resultado:** assinatura 3.1 aplicada, sympy fixo, refactors locais preservados, parity 11/11.
**Bonus:** Codex também atualizou `Chichorro_RI.py` — escala 3.1 (A++..F) implementada + CTI call corrigida.
**Estado parcial em RI.py:** escala e CTI call ✅, mas POI_CC_Idade / DPI_OGS 3.1 / ESCI 3.1 ainda em falta na assinatura `RI()`.
**Nota:** `CtiPage.tsx` ainda não expõe `VHE_Dispositivos`/`VVE_Dispositivos` — backend tem fallback temporário.

#### A3. ✅ Batch: substituir POI/ESCI/DPI + completar RI — CONCLUÍDO

**Resultado:** 4 módulos Python 3.1 confirmados. Imports OK. RI_RIA calculado e no dict de retorno.

#### A4. ✅ Flask.py + Chichorro_RI_inter.py — CONCLUÍDO

**Resultado:** todos os endpoints atualizados para assinaturas 3.1; `Chichorro_RI_inter.py` criado; `/RI/interv` adicionado.

---

### Bloco B — Frontend

#### B1. ✅ Atualizar poiDefinitions.ts — POI_CC_Idade — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/components/poi/poiDefinitions.ts`
**Ação:** adicionar campo `POI_CC_Idade` ao subfator `cc`
**Responsável:** Codex

#### B2. ✅ Atualizar esciDefinitions.ts — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/components/esci/esciDefinitions.ts`
**Ações:**

- Subfator `gp`: adicionar `ESCI_GP_Auto` com `visibleWhen: DetAler === 'Automatico'`
- Subfator `ext`: atualizar opções OGS (PP+F → R+PP); adicionar `ESCI_EXT_Formacao`
- Subfator `ria`: atualizar opções OGS; adicionar `ESCI_RIA_Formacao`; adicionar `ESCI_RIA_CS`

**Responsável:** Codex

#### B3. ✅ Atualizar dpiDefinitions.ts — DPI_OGS — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/components/dpi/dpiDefinitions.ts`
**Ação:** substituição completa do subfator `ogs` — de 7 campos para 4
**Responsável:** Codex

#### B4. ✅ Atualizar RiPage.tsx — nova escala + remover seletor período — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/pages/RiPage.tsx`
**Ações:**

- Substituir labels da escala (A1/A2/B/C/D/E → A++..F)
- Remover seletor de período de construção (passa a vir do subfator CC do POI)

**Responsável:** Codex

#### B5. ✅ Criar InterventionsPage.tsx — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/pages/InterventionsPage.tsx` (novo)
**Resultado:** UI criada com seleção individual, conjuntos predefinidos extraídos de `RI_I.js`, rota `/app/interventions` e menu.
**Nota:** `VHE_Dispositivos`/`VVE_Dispositivos` continuam com fallback para `Dispositivos` até serem expostos no CTI.
**Responsável:** Codex

#### B7. ✅ Correções POI_EF e POI_IA — CONCLUÍDO

**Modo:** `active_build`
**Ficheiros:**

- `app/frontend/src/components/poi/poiDefinitions.ts`
- `app/backend/Chichorro_POI.py`

**Resultado:**

- `POI_EF_Altura`: valores `"Menor9m"`/`"Maior9m"` → `"<=9m"`/`">9m"` (frontend + backend)
- `POI_EF_ElemConstr` label e ordem de campos: Aplica → UT → ElemConstr → CI → Altura → DistEdif
- `POI_EF_Altura.visibleWhen`: corrigido para excluir o caso UT=XII + CI > 5000
- `POI_IA_TipoInst2`: opções estáticas → `getOptions` dinâmico filtrado por `TipoInst`
- Backend: `'<=16m'` (incorreto) → `'<=4m'` em 7 ocorrências no bloco POI_EF
- Arrays de distâncias EF reescritos sem spread redundante

#### B8. ✅ Fix sync bidirecional CTI↔POI_ATIV (TipoEdif) — CONCLUÍDO

**Modo:** `active_build`
**Ficheiros:**

- `app/frontend/src/components/poi/PoiFactorSection.tsx`
- `app/frontend/src/pages/CtiPage.tsx`

**Resultado:**

- `syncTipoEdifFromCti` deixa de escrever em `moduleInputs.poi` — apenas atualiza o form (display)
- `clearAll` em POI_ATIV limpa CTI primeiro, depois POI (ordem correta para evitar re-sync indesejado)
- `onClear` em CTI agora também limpa `POI_ATIV_TipoEdif` em moduleInputs e form
- Campo `POI_ATIV_TipoEdif` nunca fica bloqueado (removido `disabled`); mantém nota informativa

#### B11 / UX-03, UX-04. ✅ Colapsar/expandir subfatores em POI, DPI e ESCI — CONCLUÍDO

**Modo:** `active_build`
**Ficheiros:**

- `app/frontend/src/components/poi/PoiFactorSection.tsx`
- `app/frontend/src/components/dpi/DpiFactorSection.tsx`
- `app/frontend/src/components/esci/EsciFactorSection.tsx`
- `app/frontend/src/components/ui/Card.tsx`

**Resultado:**

- Botão "Colapsar menu" / "Expandir menu" com chevron animado adicionado ao cabeçalho de cada cartão de subfator via `CardHeader.right`
- Animação de altura com `grid-rows-[0fr]` / `grid-rows-[1fr]` + `transition-[grid-template-rows]` (sem max-height fixo)
- Ao receber `highlightKey`, o cartão expande automaticamente e faz scroll até si
- Inline styles (`style={{ color: ... }}`) substituídos por classe Tailwind `text-ink-500/55`

#### B9 / UX-02. ✅ Aviso de RI desatualizado na RiPage — CONCLUÍDO

**Modo:** `active_build`
**Ficheiro:** `app/frontend/src/pages/RiPage.tsx`

**Resultado:**

- Quando qualquer input de subfator é alterado após um cálculo de RI, aparece aviso vermelho: *"Os dados de entrada foram alterados desde o último cálculo. O valor de RI apresentado pode não estar atualizado — recalcule para obter o resultado correto."*
- Implementado via `SESSION_DATA_UPDATED_EVENT` + `loadingRef` (suprime evento durante o próprio cálculo)
- Aviso limpa ao recalcular RI com sucesso, ao importar sessão ou ao limpar sessão

#### B6 / UX-01. ✅ UX de validação e invalidação de resultados — CONCLUÍDO

**Modo:** `active_build`
**Ficheiros principais:**

- `app/frontend/src/components/poi/PoiFactorSection.tsx`
- `app/frontend/src/components/dpi/DpiFactorSection.tsx`
- `app/frontend/src/components/esci/EsciFactorSection.tsx`
- `app/frontend/src/pages/CtiPage.tsx`
- `app/frontend/src/components/ui/ModuleGlobalValueCard.tsx`
- `app/frontend/src/lib/resultsStore.ts`

**Resultado:**

- Campos obrigatórios em falta mostram mensagem específica: `Preenche "<campo>" antes de calcular.`
- O input em falta recebe destaque visual com `ring-2 ring-red-400`.
- Quando um input já calculado é alterado ou apagado, o resultado local mantém o valor antigo mas fica em cinza translúcido.
- A página mostra aviso âmbar: `Um ou mais valores foram alterados ou apagados. Por favor, volte a calcular.`
- O valor global do módulo no canto superior direito mantém o último valor válido em cinza translúcido e mostra `Valor desatualizado`.
- Ao recalcular com sucesso, o estado desatualizado é limpo.

**Validação:** `npm run build` em `app/frontend` passou.
**Responsável:** Codex

---

#### B10. ✅ Expor VHE_Dispositivos / VVE_Dispositivos em CtiPage.tsx — CONCLUÍDO

**Modo:** `active_build`
**Ficheiros alterados:**

- `app/frontend/src/pages/CtiPage.tsx`
- `app/backend/Flask.py`

**Resultado:**

- `VHE_Dispositivos` e `VVE_Dispositivos` adicionados a `CtiValues`, `defaultValues`, `normalizeSavedValues`, UI (selects dentro de VHE/VVE, visíveis quando `Aplica_X === "Existe"`), `validate()` e payload do `onCalculate`
- Fallback `VHE_Dispositivos = VHE_Dispositivos or Dispositivos` removido do `Flask.py` (era medida temporária; app nova não tem sessões legadas)
- `RiPage.tsx` não necessitou alterações

---

### Análise de lacunas 3.1 — CONCLUÍDA (2026-04-27)

Revisão completa da dissertação de Rui Sobral (2019) e da referência `reference/chichorro-3.1-rs/` para verificar se alguma alteração 3.1 ficou por implementar.

**Alterações do modelo 3.1 (secção 3.4 da dissertação):**

| Alteração | Backend | Frontend | Estado |
| --- | --- | --- | --- |
| CTI – VHE_Dispositivos / VVE_Dispositivos distintos por cenário | ✅ | ✅ | Done |
| DPI_OGS – 7→4 campos, lógica de formação e regulamento | ✅ | ✅ | Done |
| ESCI_GP – novo campo ESCI_GP_Auto (Aspiração/Ótico/Termovelocimétrico) | ✅ | ✅ | Done |
| ESCI_EXT – novo campo ESCI_EXT_Formacao (Sem/Com) | ✅ | ✅ | Done |
| ESCI_RIA+CS – novos campos ESCI_RIA_Formacao e ESCI_RIA_CS | ✅ | ✅ | Done |
| RI – escala de 12 classes (A++…F) | ✅ | ✅ | Done |
| RI – aceitabilidade via POI_CC_Idade → RI_RIA | ✅ | ✅ | Done |
| Intervenções – 34 ativas e passivas + conjuntos predefinidos | ✅ | ✅ | Done |

**Conclusão:** B10 é a única lacuna de modelo. Todos os restantes 7 itens da secção 3.4 estão implementados.

**Desenvolvimentos futuros referidos na dissertação (secção 7.2) — fora do âmbito 3.1:**

- Método simplificado (CHICHORRO 2.0 como base)
- Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo)
- Afinação de custos €/m² via PRONIC
- Intervenções adicionais (Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa)
- Representação gráfica das consequências por intervenção *(ver D4 abaixo)*
- Georreferenciação e base de dados de edifícios
- Tratamento de edifícios devolutos
- Integração com Firecheck 2.0

Estes itens não pertencem ao modelo 3.1 — são propostas de versão futura por Rui Sobral.

---

## Autenticação — branch `feat/access-log`

### AUTH-01. ✅ Log de acessos (base de dados) — CONCLUÍDO

PostgreSQL (Neon) em produção, SQLite local em dev. Tabela `access_log`, endpoints `/admin/log` e `/admin/users`. Wrapper `_PGConn` para compatibilidade sqlite3/psycopg2.

### AUTH-02. ✅ Registo com verificação de e-mail — CONCLUÍDO

Tabela `users`, `/auth/register`, `/auth/verify/<token>`. E-mail via SDK Resend em thread daemon. `url_root` capturado antes de spawnar a thread.

### AUTH-03. ✅ Frontend de registo — CONCLUÍDO

`SignUpPage.tsx`, banner `?verified=` em `LoginPage.tsx`, link "Criar conta".

### AUTH-04. ✅ Recuperação de palavra-passe — CONCLUÍDO

`/auth/forgot-password` + `/auth/reset-password`. `ForgotPasswordPage.tsx`, `ResetPasswordPage.tsx`.
Migração automática das colunas `reset_token` / `reset_token_expires_at`.

### AUTH-05. ✅ Modal "sessão expirada" — CONCLUÍDO

`SESSION_EXPIRED_EVENT` despachado pelo `postJson` em qualquer 401. Modal bloqueante em `AppLayout` com botão de recarga.

### Concluído em produção ✅ (2026-05-08)

- **DB-01** ✅ — Neon PostgreSQL configurado no Render; env vars activas; deploy verde
- **TEST-01** ✅ — Fluxo e2e aprovado: registo → e-mail → verificação → login → reset password
- **AUTH-11** ✅ — Modal sessão expirada validado ao apagar cookie manualmente em DevTools
- **ProxyFix** ✅ — `ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)` adicionado; IP real agora registado no `access_log` (antes estava sempre `127.0.0.1`)

### Concluído em `feat/security` ✅ (2026-05-08)

- **AUTH-12** ✅ — Merge `feat/access-log` → `3.1-dev` concluído; push para GitHub; sync docs disparado
- **AUTH-07** ✅ — Rate limiting com Flask-Limiter + Upstash Redis; validado em produção dev
- **AUTH-08** ✅ — `session.clear()` nos 3 pontos de login; mitigação session fixation (OWASP ASVS V3.3)
- **AUTH-06** ✅ — HTTPONLY ✅ · SECURE via `CHICHORRO_SESSION_SECURE=1` ✅ · SAMESITE=Lax ✅ · cookie renomeado para `chichorro_session` (anti-fingerprinting)

### Pendente — próximos passos (`feat/security`)

- **SEC-01** — Rever configuração CORS (origins, credentials, métodos)
- **SEC-02** — HTTPS obrigatório em produção, redirects HTTP→HTTPS

---

## Melhorias pós-3.1 (backlog UI/UX)

### UI-01 — Gráfico de impacto individual por intervenção

**Contexto:** proposta de RS, dissertação secção 7.2.
**O que é:** no módulo de Intervenções, além do RI agregado resultante das N intervenções selecionadas, mostrar um gráfico (bar chart horizontal / tornado chart) com o impacto individual de cada intervenção — i.e., quanto reduziria o RI se fosse aplicada isoladamente.
**Valor:** permite ao utilizador priorizar intervenções por impacto e fazer análise de custo-benefício por medida.

**Implementação sugerida:**

- Backend: novo endpoint `POST /RI/interv/impact` que recebe a lista de intervenções selecionadas e devolve, para cada uma, o RI resultante se só essa estivesse ativa.
- Frontend: gráfico com Recharts (já disponível no projeto) ou similar — barras ordenadas por delta RI decrescente.
- Custo: ~34 cálculos de RI por chamada (aceitável no backend Python).

**Branch sugerido:** `feat/interv-impact-chart` (a partir de `3.1-dev` após C2 concluído).

---

### Bloco C — Validação

#### C1. ✅ Paridade backend 3.1 — CONCLUÍDO

`parity_runner.py` correu: **11/11 checks — 0 falhas.**

#### TEST-01 — C2 — Teste end-to-end

**Ação:** percorrer todos os módulos no browser com valores conhecidos
**Critério:** aprovação pelo João
