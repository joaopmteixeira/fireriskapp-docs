# Decisions Log

> Nota de contexto: documento historico pre-migracao FastAPI. Referencias a Flask/Flask.py descrevem o estado antigo; o backend atual e FastAPI/ASGI em `app/backend/main.py`.

---

## 2026-06-18 — SEC-13 · INFRA-08

Decisao `sec13-ssh-cloudflare-tunnel-revertido`: SSH via Cloudflare Tunnel tentado e revertido — removido do scope SEC-13.
Razao: Cloudflare Free plan nao emite certificados TLS para third-level subdomains (`ssh.chichorro.joaopmteixeira.net`); TLS handshake falha mesmo com Access Application configurada; OTP por email adiciona fricao sem melhorar workflow real; VPN local e suficiente para acesso SSH a VM.

Decisao `infra08-docker-exec-backup-check`: `backup_check.sh` usa `docker compose exec -T backup` para inspecionar o volume de backups em vez de aceder ao path do host.
Razao: o path do host onde o volume Docker esta montado nao e deterministico (depende do Docker daemon e configuracao); aceder via `docker exec` e robusto e independente do sistema de ficheiros do host.

Decisao `infra08-dot-over-source-sh`: scripts de monitorizacao usam `. /etc/chichorro-monitoring.env` (dot) em vez de `source`.
Razao: `source` e um builtin bash e nao existe em `/bin/sh` POSIX; os scripts usam `#!/bin/sh` para maxima portabilidade; `source: not found` foi o erro real na VM (Debian com dash como sh).

Decisao `infra08-monitoring-env-owner-deploy`: `/etc/chichorro-monitoring.env` com `chown deploy:deploy` em vez de `root:root`.
Razao: os scripts de monitorizacao correm no crontab do utilizador `deploy`; se o ficheiro e owned por root com chmod 600, o utilizador `deploy` nao consegue le-lo e o script falha silenciosamente.

---

## 2026-06-01 — AI-01 · Graphify setup · AI tooling strategy

Decisão `graphify-local-only-artifacts`: artefactos do Graphify (`graph.html`, `graph.json`, `GRAPH_REPORT.md`, `.graphify/`, `graphify-out/`) e `docs/vault/` adicionados ao `.gitignore` como local-only.
Razão: ficheiros gerados automaticamente, dezenas de MB, sem valor em CI ou para colegas que não usem estas ferramentas localmente.

Decisão `graphify-refresh-rules-documented`: regras de quando refrescar vs. não refrescar documentadas em `CLAUDE.md` na raiz.
Razão: sem regras explícitas, o Graphify tenderia a ser recorrido em qualquer edição; as regras restringem o refresh a mudanças estruturais.

Decisão `ai-tooling-prefix-ai`: tarefas de IA separadas com prefixo `AI-NN` em vez de misturar com BACK/UI/etc.
Razão: as ferramentas de IA são categoria distinta (suporte ao desenvolvimento, não features da aplicação); prefixo próprio facilita triagem no Linear.

Decisão `obsidian-vault-handoff-first`: vault Obsidian documentado em `HANDOFF_OBSIDIAN_VAULT.md` antes de implementar.
Razão: implementação envolve múltiplos scripts e decisões de schema; documentar primeiro reduz erros e facilita retoma após pausa.

---

## 2026-05-31 — docs(ai) · estratégia IA

Decisão `ai-strategy-three-layers`: estratégia de IA do projeto definida em três camadas sequenciais: Graphify (grafo do código) → Obsidian (base de conhecimento) → RAG (assistente de perguntas).
Razão: cada camada valida a anterior; não faz sentido construir RAG sem as fontes estruturadas que o Obsidian vai fornecer.

Decisão `rag-blocked-on-obsidian`: plano RAG (AI-03) documentado em `docs/research/RAG_FUTURE.md` mas não iniciado até AI-02 (Obsidian) validado.
Razão: o RAG precisa de um corpus bem estruturado; o vault Obsidian é esse corpus; implementar RAG antes seria construir sobre areia.

---

## 2026-05-28 — SEC-04b · session-remount · POI conditional fields · DOCS-02

Decisão `sec04b-remove-werkzeug-confirmed`: werkzeug removido do `_verify_password` após confirmação visual na BD Supabase que ambos os utilizadores ativos têm hashes `$argon2id`.
Razão: o fallback werkzeug era temporário por design (SEC-04); quando todos os hashes estão migrados, manter werkzeug aumenta a superfície de ataque e introduz código morto.

Decisão `sec04b-requirements-cleanup`: `werkzeug>=3.0,<4` removido de `requirements.txt`.
Razão: werkzeug só era usado no fallback; sem fallback, a dependência é completamente desnecessária e reduz o footprint de dependências.

Decisão `session-remount-key-on-outlet`: `key={sessionKey}` adicionado ao `<Outlet>` no `AppLayout.tsx` em vez de forçar reload de página.
Razão: importar ou limpar uma sessão actualizava o sessionStorage mas a página React não remontava — componentes mantinham estado antigo em memória; o `key` é a abordagem idiomática React para forçar unmount/mount sem reload de página.

Decisão `poi-payload-filter-by-options-length`: payload filtrado por `opts.length > 0` em vez de `!f.visibleWhen || f.visibleWhen(values)`.
Razão: a primeira correção filtrava todos os campos escondidos incluindo campos com opções estáticas (ex: `POI_IA_Conduta`) que o backend exige como obrigatórios; o problema original só afetava campos `getOptions` dinâmicos que retornam `[]` quando não aplicáveis.

Decisão `poi-conditional-fields-optional-backend`: `POI_IA_TipoInst2` e `POI_ATIV_TipoEdif2` tornados `Optional[Literal[...]] = None` no backend.
Razão: campos dinâmicos com `getOptions` que retorna `[]` são excluídos do payload pelo frontend; o backend deve aceitar a ausência destes campos sem falha de validação; a lógica de cálculo em `Chichorro_POI.py` já os ignora quando não aplicáveis.

Decisão `cti-ativ-bidirectional-sync-via-module-inputs`: sincronização CTI↔ATIV TipoEdif implementada actualizando module inputs de ambos os lados antes de `setValues` (antes do disparo de `SESSION_DATA_UPDATED_EVENT`).
Razão: os listeners de sync lêem `getModuleInputs()` para decidir o valor correcto; se os module inputs estiverem já actualizados quando o evento dispara, os listeners encontram valores consistentes e fazem no-op sem sobrepor a mudança do utilizador.

Decisão `cti-tipodedif-not-disabled`: `disabled={isTipoEdifSynced}` removido do campo TipoEdif na CtiPage.
Razão: o utilizador quer poder editar CTI TipoEdif directamente; o campo estava bloqueado enquanto POI ATIV tivesse um valor — comportamento não intencional; o sync bidirecional garante consistência sem precisar de bloquear o campo.

Decisão `docs02-canonical-subplan-header`: formato canónico `Estado → Data de conclusão → Branch` adoptado para todos os subplans; YAML frontmatter e datas inline no H1 proibidos.
Razão: os 58 subplans tinham 4+ formatos distintos (YAML frontmatter, `*(concluído YYYY-MM-DD)*` no H1, `**Data:**` sem "de conclusão"); uniformização facilita leitura e geração de relatórios automáticos.

Decisão `parity-checker-static-tool`: `tools/check_option_parity.py` criado como verificador estático permanente frontend↔backend em vez de testes manuais por subfator.
Razão: sem ferramenta automática, qualquer alteração a um `Literal` no schema ou a uma opção no TypeScript pode criar divergências silenciosas que só se manifestam em HTTP 422 em produção; a ferramenta corre em segundos e deteta o problema imediatamente.

Decisão `tests-individual-endpoints-not-combined`: `test_valid_options.py` usa endpoints individuais (`/POI/CC`, `/POI/IA`, etc.) em vez dos endpoints combinados (`/POI`, `/DPI`).
Razão: os endpoints combinados agregam os resultados dos subfatores e tentam `if subfator_result > 0`; quando um subfator retorna `'ERRO'` (string) para combinações matematicamente impossíveis mas Pydantic-válidas, o Python lança `TypeError: '>' not supported between 'str' and 'int'`; os endpoints individuais retornam HTTP 200 independentemente do valor calculado.

Decisão `schema-poi-cc-idade-no-spaces`: `POI_CC_Idade` Literal values corrigidos sem espaços (`"1991-2008"` em vez de `"1991 - 2008"`).
Razão: o frontend enviava os valores sem espaços; o backend Literal exigia com espaços; qualquer utilizador que selecionasse um ano entre 1951 e 2008 recebia HTTP 422 silencioso; o campo não entra no cálculo (só registo) mas o 422 bloqueava o submit.

Decisão `schema-dpi-ogs-aplica-phantom-removed`: `"Nao Existe"` removido do `DPI_OGS_Aplica` Literal.
Razão: o valor não consta da tabela do modelo (Quadro 3.5 da dissertação), nunca é oferecido pelo frontend, e o código de cálculo `DPI_OGS()` não tem branch para ele — cai sempre em `_DPI_OGS = None → return 'ERRO'`; é um phantom value que só podia causar confusão.

Decisão `calc-audit-blocked-on-tese31-excel`: plano CALC_AUDIT criado mas execução bloqueada até tabelas Excel da tese3.1 estarem disponíveis.
Razão: a fonte de verdade para validar o código v3.1 deve ser a dissertação 3.1 (Rui Sobral), não a 3.0 (João Teixeira); os Excel existentes são da tese3.0 e têm diferenças estruturais (ex. DPI_OGS com 3 sub-scores vs. tabela unificada no v3.1).

---

## 2026-04-18

Decisão: `app/frontend/` é a base ativa principal da interface moderna.
Razão: já possui estrutura modular por páginas, rotas, autenticação, componentes de domínio e UI reutilizável.

Decisão: `app/backend/` é a base ativa principal do backend e da lógica técnica.
Razão: já possui separação clara por módulos CTI, DPI, ESCI, POI e RI.

Decisão: `reference/chichorro-3.0-jt/` é a referência legacy completa da v3.0.
Razão: serve de comparação histórica, funcional e de rastreabilidade.

Decisão: `reference/chichorro-3.1-rs/` é uma referência funcional viva para implementação da v3.1.
Razão: será necessária para matchup entre a stack moderna e o comportamento esperado da próxima fase.

Decisão: `reference/chichorro-2.0-rf/` é uma referência metodológica futura para a v4.0.
Razão: ajudará a recriar ou reinterpretar um método simplificado + completo.

Decisão: o projeto deve distinguir explicitamente quatro modos de trabalho:

- `active_build`
- `v3_0_legacy_compare`
- `v3_1_matchup`
- `v4_0_research`

Razão: evita confusão entre app ativa, referências funcionais e investigação futura.

Decisão: o padrão de componentes por domínio deve ser preservado.

Exemplos:

- `FactorSection.tsx`
- `definitions.ts`

Razão: melhora consistência e facilita expansão para novos módulos.

Decisão: a camada de UI reutilizável deve servir de base comum.

Exemplos:

- `Button.tsx`
- `Card.tsx`
- `Field.tsx`
- `ModuleGlobalValueCard.tsx`

Razão: evita duplicação visual e estrutural.

Decisão: o fluxo de autenticação atual inclui componentes transitórios/legacy.

Exemplos:

- `legacyLogin.ts`
- `AuthPendingScreen.tsx`

Razão: isso deve ser tratado como compatibilidade temporária e não como arquitetura final desejada.

---

## 2026-04-20 — Análise 3.0 → 3.1 (v3_1_matchup)

Decisão: `POI_CC_Idade` é um novo campo em 3.1 que não altera o score do subfator CC mas é usado pela função RI() para calcular o limite de aceitabilidade `RI_RIA`.
Razão: o campo já existe na app ativa (em RiPage.tsx como seletor separado), mas em 3.1 pertence conceptualmente ao subfator CC do POI. A migração deve consolidá-lo aí.

Decisão: `ESCI_EXT_OGS` e `ESCI_RIA_OGS` têm valores renomeados em 3.1.
Razão: `PP+F` passa a `R+PP`. Não é só cosmético — os valores das strings mudam, o que quebra endpoints existentes se não forem atualizados em simultâneo no frontend e backend.

Decisão: `DPI_OGS` é uma substituição completa de 7 campos por 4 em 3.1.
Razão: o modelo simplificou o subfator OGS. Os campos antigos (`P_Emergencia_Exigencia`, etc.) desaparecem por completo. A lógica de cálculo é totalmente nova, incluindo um ajuste pós-score baseado em `DPI_OGS_Regulamento`.

Decisão: a escala RI passa de 6 classes (A1/A2/B/C/D/E) para 12 classes (A++/A+/A/B+/B/B-/C+/C/C-/D/E/F) em 3.1.
Razão: a referência `reference/chichorro-3.1-rs/Chichorro_RI.py` e `Chichorro_RI_inter.py` confirmam a nova escala. A mudança é de modelo, não estética.

Decisão: o Módulo de Intervenções é uma feature nova de raiz em 3.1 — não é uma extensão de algo existente.
Razão: `Chichorro_RI_inter.py` é um ficheiro independente que recebe todos os parâmetros do modelo + 34 flags booleanas, modifica os parâmetros conforme as intervenções selecionadas, e recalcula o RI completo. Requer novo endpoint Flask, novo módulo backend e nova página frontend.

Decisão: as alterações backend 3.0→3.1 devem ser feitas substituindo os `Chichorro_*.py` ativos, não criando versões paralelas.
Razão: o contrato de API deve evoluir (não bifurcar). A paridade pode ser validada com `parity_runner.py` após a substituição.

Decisão: `Chichorro_CTI.py` 3.1 não pode ser substituído diretamente — requer merge.
Razão: o ficheiro ativo tem refactors locais (fumo, clarabóia, VVE ascendente) ausentes na referência 3.1. A substituição direta apagaria correções funcionais. A estratégia é aplicar a nova assinatura 3.1 preservando os refactors do ativo.

Decisão: `RI_interv_21_efetivo` não é um input do utilizador no fluxo CTI normal.
Razão: é um flag injetado exclusivamente pelo módulo de intervenções (intervenção 21 = redução de efetivo). No endpoint CTI padrão, deve defaultar a `0`. Não deve aparecer no formulário `CtiPage.tsx`.

Decisão: o bug `sympy` no `Chichorro_CTI.py` ativo deve ser corrigido no mesmo handoff da atualização CTI 3.1.
Razão: `Symbol`/`solve` são chamados sem `import sympy` no ramo `SistemaExtincao == 'Com'`. Gera `NameError` em runtime para qualquer sessão com sistema de extinção ativo. É um bug crítico de produção.

---

## 2026-04-21 — Decisões UX frontend (v3_1_matchup)

Decisão: `POI_CC_Idade` move para o subfator CC do POI e é removido da RiPage (Opção A).
Razão: a referência 3.1 coloca o campo dentro do subfator CC. O backend calcula `RI_RIA` e devolve-o no response dict. Manter na RiPage criaria inconsistência e dívida técnica. As sessões 3.0 já ficam inválidas pelo rename dos OGS do ESCI.

Decisão: a página de Intervenções implementa ambos os modos em simultâneo — seleção individual das 34 intervenções E conjuntos predefinidos (1-6), como a referência 3.1.
Razão: a referência 3.1 já implementa os dois modos em paralelo. Não há razão para limitar.

---

## 2026-04-22 — Correções POI_EF / POI_IA, sync CTI↔POI_ATIV e aviso RI desatualizado (UX-02)

Decisão: valores de `POI_EF_Altura` usam notação `"<=9m"` / `">9m"` em vez de `"Menor9m"` / `"Maior9m"`.
Razão: consistência com os restantes campos de distância que usam operadores `<=`/`>`.

Decisão: ordem dos campos no subfator POI_EF alterada para: Aplicabilidade → UT → ElemConstr → CI → Altura → DistEdif.
Razão: reflete a dependência lógica — CI e Altura condicionam DistEdif; Altura depende de ElemConstr que depende de Aplica.

Decisão: `POI_IA_TipoInst2` passa de opções estáticas para `getOptions` dinâmico filtrado por `TipoInst`.
Razão: os subtipos só fazem sentido no contexto do tipo de instalação selecionado; apresentar opções irrelevantes induzia erro de preenchimento.

Decisão: `POI_EF_Altura.visibleWhen` exclui o caso UT=XII + CI > 5000.
Razão: quando UT=XII e CI > 5000, a tabela de referência 3.1 não discrimina por Altura — o campo é semanticamente irrelevante neste ramo.

Decisão: o sync CTI↔POI_ATIV para `TipoEdif` é unidirecional ao nível de `moduleInputs`.
Razão: antes, `syncTipoEdifFromCti` e `syncTipoEdifFromPoi` escreviam ambos em `moduleInputs`, criando um deadlock após import de sessão — nenhum dos campos ficava editável. A correção: `syncTipoEdifFromCti` atualiza apenas o form (display) sem escrever em `moduleInputs.poi`; só o clique explícito ou o botão "Calcular" escreve em `moduleInputs`.

Decisão: o botão "Limpar" de POI ATIV e CTI limpa ambos os lados da sincronização (moduleInputs + form).
Razão: sem isso, limpar um lado deixava o outro com o valor antigo, que na reativação seguinte causava re-lock do campo.

Decisão: quando qualquer input de subfator é alterado e já existe um resultado de RI calculado, aparece um aviso vermelho na RiPage a indicar que o RI pode não estar atualizado.
Razão: o utilizador pode alterar inputs em POI/CTI/DPI/ESCI sem recalcular o RI, tornando o valor apresentado desatualizado sem aviso visual. A implementação usa `SESSION_DATA_UPDATED_EVENT` com um `loadingRef` para suprimir o evento durante o próprio cálculo do RI.

## 2026-04-22 — UX de invalidação de resultados calculados (UX-01)

Decisão: ao alterar ou apagar qualquer input de POI, DPI, ESCI ou CTI, o resultado calculado anteriormente deixa de ser considerado atual, mas continua visível no frontend em cinza translúcido.
Razão: apagar o valor antigo remove contexto ao utilizador; manter o valor com estado visual desatualizado deixa claro que existe um cálculo anterior, mas obriga a recalcular antes de confiar nele.

Decisão: os cartões globais `ModuleGlobalValueCard` também devem mostrar estado desatualizado.
Razão: quando um subfator é alterado, o valor global do módulo deixa de representar os inputs atuais. O cartão global mantém o último valor válido em cinza translúcido e mostra `Valor desatualizado`.

Decisão: o estado desatualizado global fica num store separado em `resultsStore.ts` (`chichorro:module-results-stale`), em vez de permanecer em `module-results`.
Razão: isto evita que módulos dependentes consumam um resultado inválido como se fosse atual, mas permite ao UI renderizar o último valor válido para orientação visual.

Decisão: `clearModuleFactorResult(..., { recomputeModule: false })` é usado durante alterações de inputs em POI/DPI/ESCI.
Razão: recomputar automaticamente a média global com um subfator removido criaria um valor parcial potencialmente enganador. O estado correto após alteração é "desatualizado" até novo cálculo.

---

## 2026-05-08 — Autenticação e base de dados (AUTH-01…AUTH-05, DB-01)

Decisão `AUTH-02`: e-mail de verificação e de reset enviados em `threading.Thread(daemon=True)` com `app.app_context()` dentro da thread.
Razão: o worker gunicorn era morto por SIGKILL quando o SMTP da Resend demorava mais que o timeout do worker. `except Exception` não captura `SystemExit` — corrigido para `except BaseException`. O envio em background elimina o bloqueio do worker.

Decisão `AUTH-02`: `url_root = request.url_root.rstrip('/')` capturado antes de spawnar a thread; passado como parâmetro à função de envio.
Razão: o contexto de pedido Flask não existe dentro da thread — `request.url_root` lança `RuntimeError: Working outside of request context` se chamado lá dentro.

Decisão `AUTH-02`: o link de verificação usa o `url_root` do backend, não `APP_BASE_URL` (frontend). `APP_BASE_URL` é reservado para o link de reset (rota React).
Razão: `/auth/verify/<token>` é uma rota Flask — usar o URL do frontend gerava 404.

Decisão `AUTH-02`: envio via SDK Resend (`resend.Emails.send()`), não Flask-Mail SMTP.
Razão: o Render free tier bloqueia SMTP (porta 587). O `urllib` nativo foi descartado porque a Cloudflare WAF bloqueia o fingerprint TLS do Python com erro 1010; o SDK Resend usa `httpx` com TLS moderno que passa.

Decisão `AUTH-04`: `POST /auth/forgot-password` responde sempre `{"ok": true}`, mesmo que o e-mail não exista na DB.
Razão: revelar se um e-mail está registado constitui user enumeration. O comportamento silencioso é o padrão correto para recuperação de palavra-passe.

Decisão `AUTH-05`: `SESSION_EXPIRED_EVENT` despachado pelo `postJson` a cada resposta 401; modal bloqueante em `AppLayout` é o único ponto de resposta.
Razão: centralizar a detecção no ponto de chamada HTTP evita duplicar lógica em cada página. Padrão pub/sub via DOM.

Decisão `DB-01`: base de dados migrada de SQLite efémero para PostgreSQL Neon (serverless, free tier permanente).
Razão: o Render free tier usa disco efémero — a SQLite é apagada a cada redeploy. `libsql-experimental` (Turso) foi descartado: requer compilação Rust/maturin, que falha no Render (sistema de ficheiros read-only durante build). `psycopg2-binary` tem wheels pré-compilados.

Decisão `DB-01`: wrapper `_PGConn` converte automaticamente `?` → `%s` e `AUTOINCREMENT` → `SERIAL PRIMARY KEY`.
Razão: permite manter toda a lógica em sintaxe sqlite3 sem alterar queries; comutação SQLite (dev) / PostgreSQL (prod) é automática via presença de `NEON_DATABASE_URL`.

Decisão `DB-01`: migrações de coluna via `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`.
Razão: `IF NOT EXISTS` funciona em SQLite 3.37+ e PostgreSQL — permite migrações automáticas em `_init_db()` sem recriar a tabela nem perder registos.

---

## 2026-05-19 — Auditoria de segurança SECURITY_AUDIT_INITIAL

Decisão `SEC/prefixos`: novos IDs de segurança distribuídos por domínio (SEC-04..09, DB-04, INFRA-03..04, BACK-05..06) em vez de criar prefixo novo `HARD-`.
Razão: "HARD" não é intuitivo fora de contexto. Os domínios existentes cobrem os gaps e mantêm consistência com o vocabulário do projeto.

Decisão `docs/security/ gitignored`: ficheiros de auditoria de segurança mantidos apenas localmente, excluídos do repositório.
Razão: documentos de auditoria descrevem vulnerabilidades em detalhe — não devem ser públicos enquanto os problemas não estiverem corrigidos.

Decisão `C-03 reclassificado CRÍTICO+`: qualquer utilizador autenticado (não apenas admin) consegue aceder a `/admin/users` e `/admin/log` — verificado no código (`require_auth` sem role check em `routers/admin.py`). Prioridade máxima de correção.
Razão: não requer conhecimento técnico — basta conhecer o URL. Expõe e-mail, username e logs de acesso de todos os utilizadores registados.

---

## 2026-05-20 — Reorganização retroativa do histórico git

Decisão `retroactive-branch-extraction`: commits feitos inline em `3.1-dev` foram isolados
em branches próprias (`auth/profile`, `db/backup`, `infra/sentry`, `docs/vitepress`) e o
histórico de `3.1-dev` foi reescrito com merges `--no-ff`.
Razão: o grafo git não refletia o trabalho por feature; branches visíveis facilitam code
review, navegação e auditoria futura.

Decisão `git-commit-tree para feat/flask-to-fastapi`: em vez de re-merger `feat/flask-to-fastapi`
(o que causaria conflitos com os commits da B-section já cherry-picked), usou-se
`git commit-tree <tree> -p <tip> -p <original-merge-parent>` para criar um merge commit
com o tree exato do original sem executar nenhum merge real.
Razão: re-merge tinha common ancestor diferente do original; `commit-tree` cria o commit
diretamente sem resolver conflitos, preservando o conteúdo byte-a-byte.

Decisão `git-rebase-onto para auth/profile`: após cherry-pick da B-section, o base original
de `auth/profile` (`3ce018f`) tinha equivalente cherry-picked (`8347187`); usou-se
`git rebase --onto 8347187 3ce018f auth/profile` para re-assentar a branch no novo base.
Razão: sem o rebase, o merge de `auth/profile` conflituaria (common ancestor `070c66a`
causava ambos os lados a conterem as mesmas alterações da B-section).

Decisão `force-with-lease em todas as branches reconstruídas`: `--force-with-lease` em vez
de `--force` para todas as branches reescritas (incluindo `3.1-dev`).
Razão: garante que não se sobrescreve trabalho que possa ter sido pushado entretanto
por outro processo; verificação de segurança mínima num force push.

---

## 2026-05-21 — Ciclo de audit segurança cloud (branch audit-fix)

Decisão `audit-fix-single-branch`: durante o ciclo de audit Codex, todos os planos vão para uma única branch `audit-fix` sem branches por plano; merge único em `3.1-dev` no final.
Razão: o ciclo de audit tem muitos planos pequenos e inter-relacionados; uma branch por plano geraria excesso de overhead de merge e tornaria difícil visualizar o estado do audit completo.

Decisão `C-04-redis-unconditional`: `UPSTASH_REDIS_URL` exigido incondicionalmente em produção (não apenas quando a feature está ativa).
Razão: `_limiter.py` é importado incondicionalmente; o fallback `"memory://"` silencioso não é distribuído entre instâncias e dá falsa sensação de segurança. Não existe cenário de produção válido sem Redis.

Decisão `C-04-email-unconditional`: `RESEND_API_KEY` e `MAIL_DEFAULT_SENDER` exigidos incondicionalmente em produção.
Razão: `services/email.py` imprime links no stdout quando sem API key — utilizadores nunca recebem e-mails de verificação/reset mas o app não dá erro, tornando o problema silencioso e difícil de diagnosticar.

Decisão `C-02-uvicorn-flags`: em vez de `ProxyHeadersMiddleware` no Starlette (removido na versão 1.0.0 instalada), usar flags `--proxy-headers --forwarded-allow-ips='*'` do uvicorn.
Razão: `starlette.middleware.proxy_headers` não existe no Starlette 1.0.0; as flags do uvicorn são a abordagem oficial recomendada e equivalente — o uvicorn actualiza o scope ASGI antes de qualquer middleware Starlette.

Decisão `C-02-trusted-hosts-wildcard`: `trusted_hosts="*"` (ou equivalente uvicorn) para Render; `"127.0.0.1"` para VPS futura com nginx em localhost.
Razão: o Render nunca expõe o porto interno do uvicorn diretamente — todo o tráfego passa pelo proxy. Para VPS, o nginx corre em localhost pelo que o IP de origem é sempre `127.0.0.1`.

Decisão `_CLAUDE.md-implementation-summary`: após implementar cada plano, adicionar secção "Resumo de implementação" no final do `_CLAUDE.md` correspondente antes do commit.
Razão: rastreabilidade entre o que foi planeado e o que foi efetivamente implementado, especialmente quando há desvios (ex: API removida, workaround necessário).

---

## 2026-05-22 — Auditoria cloud audit-fix (planos A-01, A-06, A-02, M-01, M-02, A-03, A-05, A-04, DB-06)

Decisão `A-01-cors-frontend-url`: CORS não aceita `*` nem origens `http://`; `FRONTEND_URL` deve estar explicitamente incluída nas origins.
Razão: mesmo com Cloudflare Pages em HTTPS, uma CORS origin `*` ou sem `FRONTEND_URL` não dá erro mas não cobre o domínio canónico da app — o browser rejeitaria pedidos do frontend em produção.

Decisão `A-06-health-db-sync`: `/health/db` implementado como rota síncrona (thread pool) em vez de `async`.
Razão: `_get_db()` usa psycopg2 que é bloqueante; chamar a partir de uma co-rotina `async def` bloquearia o event loop do uvicorn.

Decisão `A-02-redis-type-not-str`: em `_check_redis_startup()`, o catch usa `type(exc).__name__` em vez de `str(exc)` para o log.
Razão: `str(exc)` de erros Redis inclui o URL completo com credenciais/token — expô-lo nos logs do Render seria uma fuga de segredos.

Decisão `A-03-alembic-no-sqlalchemy-orm`: Alembic configurado com psycopg2 puro (`psycopg2.connect`), sem SQLAlchemy ORM.
Razão: SQLAlchemy ORM implicaria refactor completo da camada de dados (~300-400 linhas); fora do âmbito do ciclo de audit de segurança. Alembic sem ORM dá versionamento de schema com custo mínimo.

Decisão `A-03-if-not-exists`: migration `0001_initial_schema.py` usa `IF NOT EXISTS` em todos os `CREATE TABLE` e `ALTER TABLE`.
Razão: a Supabase já tem o schema em produção; sem `IF NOT EXISTS` a migration falha na primeira execução com erro "relation already exists".

Decisão `A-04-alembic-version-excluded`: `alembic_version` excluída dos backups de dados (incluindo a descoberta dinâmica via `information_schema`).
Razão: é metadata de schema Alembic, não dados de utilizador; para restore, primeiro corre-se `alembic upgrade head` que recria `alembic_version`, depois restauram-se os dados.

Decisão `A-04-tools-gitignored`: `tools/restore_db.py` e `tools/backup_db.py` ficam locais (gitignored), apenas `.github/scripts/backup_db.py` está commitado.
Razão: `.gitignore` exclui toda a pasta `tools/`; os scripts de CI estão em `.github/scripts/` que é a localização correcta para artefactos de CI.

Decisão `DEPLOY-rename`: `docs/deploy/DEPLOY_RENDER_CLOUDFLARE.md` renomeado para `server/cloud_vps_audit_plans/DEPLOY_PRODUCTION.md`.
Razão: toda a documentação operacional de deploy e audit fica centralizada em `server/cloud_vps_audit_plans/`; o nome `DEPLOY_PRODUCTION.md` é agnóstico ao provider e mais adequado a uma futura migração para VPS.

Decisão `DB-06-backlog`: SQLAlchemy ORM registado como DB-06 no backlog, fora do ciclo audit-fix.
Razão: implica refactor de camada de dados com 300-400 linhas em código de produção; o risco de regressão é desproporcionado face ao benefício durante um ciclo de hardening de segurança.

---

## 2026-05-24 — Audit-fix final: C-03, M-04, B-02, B-01 + merge 3.1-dev

Decisão `C-03-runtime-user-alembic-env`: Alembic usa `DATABASE_URL_MIGRATIONS` (superuser `postgres`) quando disponível; fallback para `DATABASE_URL` quando não definida.
Razão: separação entre utilizador de migrations (DDL + DML pleno) e utilizador runtime (só DML nas tabelas da app). A env var de migrations não deve existir em produção sem o utilizador runtime criado — a ordem obrigatória é: Supabase SQL (criar role) → Render (atualizar vars) → deploy.

Decisão `M-04-request-id-before-csrf`: middleware `add_request_id` inserido antes do `CSRFMiddleware` na stack de middlewares.
Razão: o UUID deve estar disponível nos logs e no scope Sentry mesmo quando um pedido é rejeitado por CSRF; inserir depois do CSRF não cobriria pedidos rejeitados.

Decisão `M-04-resend-github-actions`: notificação de falha de backup usa Resend API (não e-mail via SMTP, não `gh` CLI, não GitHub mail).
Razão: Resend já é a dependência de e-mail do projeto; endpoint simples via `curl`; independente da conta GitHub; inclui link direto para o run falhado.

Decisão `B-02-no-api-prefix`: rotas da app mantidas sem prefixo `/api`; subdomain `api.*` fornece contexto suficiente; nginx VPS usa prefix-strip (`proxy_pass http://127.0.0.1:8000/;` com trailing slash).
Razão: prefixo `/api` no código da app acoplaria o código a uma decisão de infraestrutura; nginx é o ponto correto para este concern; backend permanece deployment-agnostic (funciona com ou sem prefixo no proxy).

Decisão `B-01-delete-not-deprecate`: `DEPLOY_CLOUD_VPS.md` apagado com `git rm` em vez de marcado como deprecated.
Razão: o ficheiro cobria apenas C-01 (TLS); todo o conteúdo estava já em `DEPLOY_PRODUCTION.md`; manter um ficheiro legado com aviso de deprecated é fonte de confusão para quem procura documentação operacional.

Decisão `merge-audit-fix-3.1-dev`: merge final de `audit-fix` → `3.1-dev` com `--no-ff`; merge anterior parcial (C-01+C-04) já existia em `3.1-dev`; os 37 commits restantes integrados sem conflitos.
Razão: branch única de audit conforme decidido em 2026-05-21; merge único no final do ciclo completo.

Decisão `alembic-env-sqlalchemy-engine`: substituir `psycopg2.connect()` por `sqlalchemy.create_engine()` + `engine.connect()` no `alembic/env.py`.
Razão: alembic 1.18.4 requer um objecto `Connection` SQLAlchemy em `context.configure(connection=...)` — a API mudou na migração para SQLAlchemy 2.0; `psycopg2.extensions.connection` não tem atributo `.dialect` e lançava `AttributeError`. Bug invisível em dev (alembic não corre localmente); só apareceu em produção.

Decisão `pythonunbuffered-diagnostico`: adicionar `PYTHONUNBUFFERED=1` como env var no Render para forçar output imediato nos logs.
Razão: Python faz buffer do stdout em containers sem TTY; o traceback do alembic estava a ser descartado antes de ser escrito para o log do Render, tornando o diagnóstico impossível sem Shell (funcionalidade paga).

Decisão `cherry-pick-fix-3.1-dev`: aplicar o fix `a07fe55` em `3.1-dev` via `git cherry-pick` em vez de aguardar o próximo merge de `audit-fix`.
Razão: `3.1-dev` é a branch de produção futura; o bug estaria presente no próximo deploy se não fosse corrigido; cherry-pick é mais seguro que re-merge parcial.

---

## 2026-05-26 — AUTH-10, estratégia de roles, CSRF split-domain e RLS Supabase

Decisão `auth10-admin-only-first`: implementar apenas o check de admin (coluna `role`, `require_admin`); não enforçar viewer/demo nesta iteração.
Razão: viewer e demo estão subespeficicados; corrigir a vulnerabilidade crítica (Codex finding #1) não requer a estrutura completa de roles; a coluna `role` fica extensível sem migration adicional.

Decisão `auth10-env-var-users-always-admin`: utilizadores hardcoded via `CHICHORRO_AUTH_USER_N` recebem `role = "admin"` diretamente no código, sem linha na BD.
Razão: estes utilizadores não têm entrada na tabela `users`; a BD não é consultada no path de login por env var; é o comportamento operacionalmente correto.

Decisão `auth10-frontend-role-ux-only`: o frontend usa o role apenas para UX (esconder links admin no sidebar); o controlo de acesso real é exclusivamente no backend via `require_admin`.
Razão: princípio de defesa em profundidade — o frontend pode ser contornado; o `require_admin` é a única garantia válida.

Decisão `auth10-consolidate-subplan`: `AUTH-10_CLAUDE.md` em `server/cloud_vps_audit_plans/` removido; conteúdo integrado em `docs/plans/subplans/AUTH/AUTH-10.md`.
Razão: evitar duplicação entre dois ficheiros; o subplan em `docs/plans/` é o local canónico para documentação de implementação.

Decisão `audit-fix-2-branch`: findings 2-7 do Codex review tratados numa branch dedicada `audit-fix-2` após o merge de `auth/roles`.
Razão: isolar as correções do Codex de outras features; manter o histórico de audit organizado por ciclo.

Decisão `csrf-cookie-domain-split-subdomain`: adicionar `cookie_domain` ao `CSRFMiddleware` derivado do hostname de `FRONTEND_URL`.
Razão: frontend (`chichorrofireriskapp.joaopmteixeira.net`) e backend (`api.*`) em subdomínios diferentes; o browser não partilha cookies entre subdomínios; `document.cookie` no frontend não conseguia ler o `csrftoken` → `getCsrfToken()` sempre vazia → 403 em todos os POST não isentos. Em dev ambos correm em `localhost` e o bug não se manifestava.

Decisão `supabase-rls-disable-app-tables`: desativar RLS nas tabelas `users` e `access_log` em vez de criar políticas permissivas.
Razão: RLS do Supabase foi concebido para proteger acesso direto via Supabase JS Client (clientes no browser); a app acede exclusivamente via backend com `chichorro_runtime`; criar políticas `USING (true)` seria equivalente a desativar mas mais verboso. Migração Alembic `0002` torna o estado reproduzível.

Decisão `rls-fix-alembic-not-code`: o fix RLS é uma migração de schema (Alembic 0002), não lógica de arranque da app.
Razão: `chichorro_runtime` não tem `ALTER TABLE` — o DDL tem de correr via `DATABASE_URL_MIGRATIONS` (postgres superuser) que é exatamente o que o Alembic faz. Centralizar no Alembic garante que qualquer re-deploy futuro aplica o fix automaticamente.

Decisão `audit-fix-2-positive-url-validation`: substituir validação negativa `startswith("http://")` por validação positiva com `urlparse` (scheme=="https" e netloc presente).
Razão: a validação negativa aceitava `ftp://`, URLs sem esquema (example.com) e protocol-relative (//example.com); em especial, `FRONTEND_URL` malformada afeta o cálculo do domínio do cookie CSRF.

Decisão `audit-fix-2-db-migrations-required`: tornar `DATABASE_URL_MIGRATIONS` obrigatória em produção (config.py + alembic/env.py).
Razão: o fallback silencioso para `DATABASE_URL` permitia que o Alembic corresse com a credencial runtime (chichorro_runtime) que não tem DDL; fail-fast garante que um re-deploy sem a credencial correta é detetado imediatamente.

Decisão `audit-fix-2-backup-role-select-only`: criar role `chichorro_backup` (SELECT apenas) para o workflow backup-db.yml, separado de `chichorro_runtime` (DML).
Razão: uma fuga do secret `DATABASE_URL_BACKUP` não dá escrita na BD; separação de credenciais por função é princípio de least privilege.

---

## 2026-05-27 — audit-fix-3 · SEC-04 · SEC-05 · SEC-07 · BACK-05 · BACK-06 · BACK-05d · TEST-02 · INFRA-02

Decisão `audit-fix-3-gitignore-tools-exception`: `.gitignore` usa regra `tools/*` com excepção explícita `!tools/backup_db.py` em vez de ignorar todo o diretório.
Razão: `tools/` contém scripts utilitários versionados; a regra anterior removia-os silenciosamente do índice git.

Decisão `audit-fix-3-backup-script-sync`: `tools/backup_db.py` sincronizado com `.github/scripts/backup_db.py` (idênticos após a sessão).
Razão: os dois scripts divergiram após audit-fix-2; `tools/` não tinha a descoberta de PK via `information_schema` nem `psycopg2.sql.Identifier`; manter duas versões distintas era fonte de bugs silenciosos em backups locais.

Decisão `sec04-argon2id-over-werkzeug`: `argon2-cffi` substitui werkzeug PBKDF2/scrypt como algoritmo de hash de passwords.
Razão: Argon2id é o algoritmo recomendado pelo OWASP e pelo RFC 9106; werkzeug usa PBKDF2-HMAC-SHA256, menos resistente a ataques de GPU; a mudança não quebra contas existentes graças ao fallback.

Decisão `sec04-upgrade-on-login`: re-hash automático no login quando o hash existente não é Argon2id (fallback werkzeug bem-sucedido → UPDATE atómico na BD).
Razão: migração gradual e transparente; evita migration forçada que tornaria contas legadas inacessíveis; a conversão acontece no próximo login sem intervenção manual.

Decisão `sec04-werkzeug-fallback-temporary`: fallback werkzeug mantido para hashes `$pbkdf2`/`$scrypt$` existentes até todos os utilizadores migrarem.
Razão: utilizadores activos com hashes legados conseguem autenticar-se enquanto a migração gradual decorre; remoção diferida para quando todos os registos forem `$argon2`.

Decisão `sec05-sha256-token-storage`: tokens de verificação/reset/email-change guardados como `sha256(token)` na BD; token em claro apenas no URL do e-mail enviado ao utilizador.
Razão: uma fuga da BD não exporia tokens activos; o princípio é análogo ao das passwords — o servidor só precisa de comparar hashes; `hashlib.sha256` sem dependência adicional.

Decisão `sec05-csrf-exempt-auth-routes`: `/auth/register`, `/auth/forgot-password`, `/auth/reset-password` adicionados a `_CSRF_EXEMPT` em `main.py`.
Razão: estas rotas são invocadas antes de o cookie CSRF ser semeado (utilizador sem sessão); sem isenção, o registo e o reset retornavam 403 em vez de processar o pedido.

Decisão `sec07-magic-bytes-not-mime-type`: validação do avatar por magic bytes (primeiros 12 bytes) em vez de `Content-Type` declarado pelo cliente.
Razão: o campo `Content-Type` e a extensão do ficheiro podem ser adulterados; os magic bytes revelam o tipo real independentemente do que o cliente declara.

Decisão `sec07-svg-rejected`: SVG rejeitado mesmo quando bem formado.
Razão: SVG é XML e pode conter scripts embutidos (XSS stored); o projeto não tem sanitizador de SVG; rejeição total é mais segura do que tentar sanitizar.

Decisão `back05-literal-over-strenuum`: `Literal[...]` da stdlib em vez de `StrEnum` para validação de valores de campo em dpi.py, esci.py, cti.py.
Razão: `Literal` é nativamente suportado pelo Pydantic v2 sem boilerplate adicional; `StrEnum` exigiria classes separadas para cada campo com valores distintos; Pydantic valida e devolve HTTP 422 com detalhe de campo automaticamente.

Decisão `back05-cti-model-validator-preserved`: em `cti.py`, o `model_validator(mode="before")` existente é preservado; os `Literal` usam os valores pós-normalização.
Razão: cti.py normaliza `Dispositivo` e `ReacaoFogo` antes da validação Pydantic; aplicar `Literal` antes do validator causaria rejeição de valores válidos que seriam normalizados; a ordem correcta é normalizar → validar.

Decisão `back06-500-json-envelope`: `unhandled_exception_handler` devolve `JSONResponse({"error":"INTERNAL_ERROR","request_id":...}, 500)` em vez de re-raise.
Razão: re-raise em FastAPI resultava em resposta de texto plano, quebrando clientes que esperam JSON; o `request_id` permite correlação nos logs Sentry.

Decisão `back06-http-exception-reraise`: `HTTPException` é re-lançada pelo handler genérico (não tratada).
Razão: FastAPI tem handler próprio para `HTTPException` com formatação correcta; interceptar duplicaria o tratamento e poderia mascarar o código HTTP original.

Decisão `back05d-literal-flat-union-tipoedif2`: `POI_ATIV_TipoEdif2` usa union flat de todos os 19 valores possíveis em vez de validação cruzada com `TipoEdif`.
Razão: Pydantic Literal não suporta cross-field validation sem `model_validator`; poi.py não tem `model_validator` (ao contrário de cti.py); a union flat rejeita valores completamente inválidos e o cruzamento correto fica a cargo da lógica de cálculo.

Decisão `test02-csrf-seed-via-get`: fixture `client` faz `GET /health` antes de ceder o cliente para semear o cookie CSRF; pedidos POST usam `{"x-csrftoken": client.cookies.get("csrftoken")}`.
Razão: `CSRFMiddleware` corre antes da validação Pydantic — sem o header CSRF, mesmo um body inválido devolve 403 (não 422); o `GET /health` é isento de CSRF e planta o cookie sem efeitos secundários.

Decisão `test02-auth-override-dependency`: `app.dependency_overrides[require_auth] = lambda: "test_user"` em vez de login real nos testes de cálculo.
Razão: os endpoints de cálculo não tocam na BD; forçar um login real exigiria BD de teste ou mock de psycopg2; o override é a abordagem idiomática do FastAPI para testes unitários de rotas protegidas.

Decisão `test02-health-db-tolerant`: `test_health_db` aceita HTTP 200 ou 503.
Razão: em CI (GitHub Actions) não há BD de teste configurada; o teste verifica que o endpoint responde com o formato correto, não que a BD está acessível — esse check é feito pelo UptimeRobot em produção.

Decisão `infra02-python312-not-314`: CI usa Python 3.12 em vez de 3.14 (versão local).
Razão: o Render usa Python 3.12; o CI deve espelhar o ambiente de produção, não o ambiente de desenvolvimento local.

Decisão `infra02-no-render-deploy-hook`: Render Deploy Hook não incluído no INFRA-02.
Razão: o hook URL requer acesso ao dashboard Render; deploy permanece manual por decisão do utilizador; o hook pode ser adicionado a `test.yml` numa tarefa dedicada quando o utilizador confirmar o URL.

---

## 2026-05-29 — Reorganização do repositório e docs/

Decisão `repo-reorg-server-dissolve`: `server/` dissolvido — conteúdo (56 ficheiros Markdown) movido para `docs/audits/` (auditorias) e `docs/ai/handoffs/` (handoffs de IA).
Razão: o nome `server/` sugeria código de servidor; os ficheiros eram exclusivamente documentação; `docs/` é a localização correta para arquivos Markdown.

Decisão `repo-reorg-tools-to-scripts`: pasta `tools/` renomeada para `scripts/` via `git mv` (histórico preservado).
Razão: `scripts/` é a convenção estabelecida para scripts utilitários de projeto; `tools/` era ambíguo e confundia com binários externos.

Decisão `repo-reorg-sessions-to-var`: `sessions/` movido para `var/sessions/`; `.gitignore` atualizado de `sessions/` para `var/`.
Razão: dados de runtime local pertencem a uma pasta isolada; `var/` segue a convenção Unix para dados variáveis/runtime; evita confusão com código de sessão de utilizador.

Decisão `repo-reorg-deploy-subdirs`: `deploy/` reestruturado com subdirs `env/` e `nginx/`.
Razão: três ficheiros planos em `deploy/` não eram escaláveis; subdirs por função (variáveis de ambiente, configuração nginx) melhoram a navegabilidade e antecipam mais configs futuras.

Decisão `docs-reorg-internal-subdirs`: 15 ficheiros na raiz de `docs/` movidos para `project/`, `method/`, `guides/`, `changelog/`, `deploy/`.
Razão: 20 ficheiros planos em `docs/` era difícil de navegar; agrupamento por função espelha a estrutura da sidebar VitePress; separação entre docs vivos (raiz) e docs de referência (subdirs).

Decisão `restore-db-tracking`: `scripts/restore_db.py` adicionado ao git tracking (estava sem seguimento).
Razão: backup e restore são um par funcional — manter apenas `backup_db.py` versionado sem o `restore_db.py` criava risco de perda do script de restore em caso de reinstalação; o par deve ser versionado em conjunto.

Decisão `research-tables-gitignore`: `docs/research/tables/` adicionado ao `.gitignore`; ficheiros Excel removidos do índice git.
Razão: ficheiros binários Excel não têm diff útil em git; são dados de investigação local não destinados ao repositório público.

Decisão `research-full-gitignore`: regra expandida para `docs/research/**` (toda a pasta) e 15 ficheiros desrastreados (PDFs teses, ai.md, chunks.jsonl, Python de referência).
Razão: toda a pasta `docs/research/` contém material local de investigação — teses, processamento AI, código de referência legado; nenhum destes ficheiros faz parte do produto nem deve estar no repositório público.

---

## 2026-06-02 — AI-02: pipeline de investigacao + vault Obsidian

Decisao `ai02-docling-over-pypdf`: docling em vez de pypdf para converter as 3 dissertacoes.
Razao: dissertacoes CHICHORRO têm tabelas de calculo coloridas (Tabela 5.4/5.5/5.6, Figura 3.33) que pypdf garble; docling produz markdown table legivel; textos single-column sao equivalentes em ambas.

Decisao `ai02-vault-root-docs`: vault Obsidian root em `docs/` em vez de `docs/vault/`.
Razao: os ficheiros `.ai.md` das teses estao em `docs/research/` e os artigos RT-SCIE em `docs/regulations/`; mover o vault root para `docs/` torna-os acessiveis sem duplicar ficheiros; os links `[[art_xxx_...]]` gerados pelo `map_sources.py` passam a resolver (deixam de ser orfaos no Graph View); nao ha alteracao a estrutura das notas em `docs/vault/`.

Decisao `ai02-fonte-notes-direct-edit`: notas fonte das teses editadas diretamente em vez de regenerar com `--force`.
Razao: `build_vault.py --force` regeneraria todas as 48 notas, incluindo as 27 de subfatores preenchidas por `map_sources.py`; editar apenas as 3 notas fonte afetadas e mais cirurgico e preserva o conteudo gerado.

Decisao `ai02-onde-mencionado-no-accent`: header `## Onde e mencionado` sem acento em `e`.
Razao: `map_sources.py` usa o string literal `"## Onde e mencionado"` para localizar a seccao nas notas; inconsistencia de acento causaria falha silenciosa.

Decisao `ai02-gitignore-both-obsidian-paths`: `.gitignore` com `docs/.obsidian/` e `docs/vault/.obsidian/` ambos ignorados.
Razao: ao mover o vault root de `docs/vault/` para `docs/`, o Obsidian cria `docs/.obsidian/`; o `docs/vault/.obsidian/` (config do vault anterior) tambem existe localmente; ambos sao state local do Obsidian e nao devem ser commitados.

Decisao `ai02-page-markers-chunk-level`: marcadores `<!-- page: N -->` sao ao nivel do chunk (N = primeira pagina do chunk), nao por pagina individual.
Razao: docling processa PDFs em chunks de 12 paginas; granularidade exacta por pagina nao e necessaria — citacoes aproximadas (pag. +-12) sao suficientes para orientar a leitura.

---

## 2026-06-05 - AI-02 encerramento + /plans-missing

Decisao `ai02-prs-manual-checkout`: PRs #2 e #4 incorporados via `git checkout origin/<branch> -- <file>` em vez de merge das branches.
Razao: as branches dos PRs tinham conflitos logicos com a versao local (TODO_PRIORITIES.md tinha AI-02 Passo 8 que o PR nao conhecia); incorporacao seletiva de ficheiros preserva ambos os conjuntos de alteracoes sem conflitos git.

Decisao `ai02a-separate-subplan`: curation manual do vault documentada num subplan proprio (AI-02a) em vez de ficar como nota dentro do AI-02.
Razao: o AI-02 esta concluido a nivel tecnico; a curation e trabalho continuo sem prazo definido; um subplan proprio permite rastrear progresso independentemente e aparece no /plans-missing.

Decisao `plans-missing-command-not-skill`: /plans-missing implementado como Claude Code custom command em `.claude/commands/plans-missing.md` (nao como skill em `~/.claude/skills/`).
Razao: o utilizador pediu explicitamente "command"; commands sao ficheiros .md simples sem estrutura de pasta adicional; o conteudo e a instrucao direta enviada ao Claude ao invocar o comando.

Decisao `plans-missing-local-only`: `.claude/commands/` esta no `.gitignore` do projeto (consistente com outros comandos existentes).
Razao: configuracao local-only do Claude Code nao deve ser versionada; outros comandos (checkpoint, good-morning, update-brain) ja seguem o mesmo padrao; o comando funciona imediatamente apos criacao sem necessidade de commit.

Decisao `feat-obsidian-vault-merge-now`: feat/obsidian-vault mergeado em 3.1-dev em 2026-06-05.
Razao: utilizador pediu explicitamente o merge; todos os passos do AI-02 estavam concluidos; AI-02a documenta o trabalho manual residual mas nao bloqueia o merge.

---

## 2026-06-08 — Roadmap VPS + organizacao de tarefas

Decisao `roadmap-vps-dual-track`: manter Render+Cloudflare como producao activa enquanto se constroi VM Proxmox local como staging; migrar para VPS apenas quando staging estiver validado.
Razao: nao faz sentido migrar producao antes de ter staging validado; Render+Cloudflare continuam a funcionar sem custo extra durante a transicao.

Decisao `roadmap-vps-12-phases`: roadmap de migracao estruturado em 12 fases sequenciais com prereqs explicitos entre fases (REL-01 → DB-06 → INFRA-03 → INFRA-06 → DB-07/08 → staging → SEC → monitoring → testes → features).
Razao: phasing permite validar cada componente antes do proximo; cada fase tem entregaveis claros e pode ser pausada sem perder estado.

Decisao `infra03-db06-as-alta-priority`: INFRA-03 e DB-06 promovidos de Prioridade Baixa para Prioridade Alta nos TODOs.
Razao: sao pre-requisitos directos para o roadmap VPS e para o staging Proxmox; estavam mal classificados.

---

## 2026-06-09 — DB-06 SQLAlchemy ORM + INFRA-03 Docker

Decisao `db06-sqlalchemy-nullpool`: engine SQLAlchemy configurado com `NullPool` (sem pool de conexoes na aplicacao).
Razao: Neon usa PgBouncer em modo transaction; connection pooling na aplicacao conflitua com o PgBouncer e causa erros de transacao; o PgBouncer faz o pooling externo.

Decisao `db06-migrate-sqlite-try-except`: `migrate_sqlite()` usa `try/except` por coluna em vez de verificar `IF NOT EXISTS`.
Razao: SQLite nao suporta `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`; try/except e o padrao correcto para migracao incremental sem reset de base de dados.

Decisao `db06-code-review-6-fixes`: 6 fixes (F1-F6) aplicados apos code review ao DB-06.
Razao: F1 (IntegrityError → 409), F2 (guard target=None → 401), F3 (guard new_email=None) e F5 (projecao de colunas sem hash/avatar) sao correccoes de seguranca e robustez; F4/F6 sao limpeza de imports e logs.

Decisao `starlette-sessions-no-redis`: Starlette SessionMiddleware nao precisa de Redis para escala horizontal.
Razao: SessionMiddleware armazena os dados na propria cookie (assinada com SECRET_KEY), sem estado no servidor; qualquer replica pode servir qualquer pedido; Redis e apenas para rate limiting (slowapi/Upstash), nao para sessoes.

Decisao `infra03-docker-non-root`: imagem Docker usa utilizador `appuser` nao-root.
Razao: boas praticas de seguranca para containers em producao; reduz superficie de ataque em caso de comprometimento da aplicacao.

---

## 2026-06-11 — INFRA-03 Python 3.12 + INFRA-06 env setup + Proxmox staging

Decisao `infra03-python-312`: Dockerfile migrado de Python 3.14-slim para Python 3.12-slim.
Razao: Python 3.14 nao tem imagem Docker estavel; Python 3.12 e a versao LTS com imagem slim disponivel e suportada; Dockerfile e test.yml actualizados em sincronia.

Decisao `infra03-split-dev-deps`: pytest e pytest-cov movidos para `requirements-dev.txt` separado.
Razao: dependencias de teste nao devem entrar na imagem de producao; Dockerfile usa apenas `requirements.txt`; reduz tamanho e superficie de ataque da imagem.

Decisao `infra07-env-file-required-false`: `env_file` no docker-compose.yml com `required: false`.
Razao: garante que o compose funciona em CI e em producao sem ficheiro `.env` local; apenas dev local precisa do ficheiro.

Decisao `infra07-proxmox-staging-vm`: VM Debian 13 no Proxmox ("chichorro-staging", 192.168.0.7) usada como ambiente de staging Docker.
Razao: permite testar deploy containerizado antes de migrar producao para VPS; estrategia dual-track (Render+Cloudflare producao + Proxmox staging) definida em ROADMAP_SELF_HOSTED_VPS.md.

Decisao `infra07-portainer-staging`: Portainer Community Edition instalado na VM chichorro-staging (:9000).
Razao: interface web para monitorizar contentores sem acesso SSH para operacoes rotineiras; facilita verificacao visual de estado (healthy/running) e logs.

---

## 2026-06-12 — REL-01 release baseline + reorganizacao docs + correcao IDs

Decisao `rel01-changelog-v310`: seccao `## [v3.1.0] — 2026-06-12` criada no CHANGELOG com sumario completo de todas as funcionalidades 3.1 (modelo, auth, seguranca, infra, AI tooling).
Razao: REL-01 era a unica Prioridade Alta pendente; snapshot documentado antes de avancar para infraestrutura VPS e alteracoes de base de dados.

Decisao `8-new-ids-roadmap-vps`: 8 novos IDs criados com subplans iniciais (DB-07, DB-08, SEC-11, SEC-12, INFRA-07, INFRA-08, TEST-04, REL-01).
Razao: roadmap em 12 fases requer IDs para todas as tarefas futuras; IDs permitem tracking no Linear e referencia cruzada entre docs.

Decisao `subplans-13-category-folders`: subplans/ reorganizado em 13 pastas de categoria (AI/, AUTH/, B/, BACK/, DB/, DOCS/, FEAT/, INFRA/, REL/, SEC/, TEST/, UI/, UX/).
Razao: com 80+ subplans numa pasta plana a navegacao tornara-se dificil; categorias espelham os prefixos dos IDs; `tools/update_subplan_links.py` criado para actualizar referencias.

Decisao `infra-id-renumbering-06-07`: IDs INFRA-06 e INFRA-07 trocados — INFRA-06 passa a ser env separation (concluido), INFRA-07 passa a ser staging Proxmox completo com Nginx + PostgreSQL (pendente).
Razao: convencao exige que o prerequisito tenha numero mais baixo; env separation (INFRA-06) e prerequisito directo de staging VPS (INFRA-07).

Decisao `frontend-typecheck-npm-script`: script `typecheck: "tsc --noEmit"` adicionado ao package.json do frontend.
Razao: permite verificacao de tipos sem build completo; essencial para CI e pre-commit rapido; documentado em `.claude/rules/verification.md`.


---

## 2026-06-15 — INFRA-07 · DB-07 · DB-08 · INFRA-09 · INFRA-10

Decisao `infra07-staging-separate-compose`: ficheiro separado `docker-compose.staging.yml` em vez de override.
Razao: nao quebra `docker compose up` em dev local; staging e dev sao ambientes distintos com requisitos diferentes (PostgreSQL vs SQLite, Nginx vs acesso direto).

Decisao `db07-pg-dump-cron-retention-7`: backup via `pg_dump` com cron diario 02:00 UTC e retencao de 7 dumps.
Razao: simples, sem dependencias externas, adequado para staging; retencao de 7 dias cobre uma semana de trabalho sem acumular espaco.

Decisao `db08-pgpassword-env-migrate`: script de migracao usa `PGPASSWORD` em vez de `.pgpass` ou prompt interativo.
Razao: mais simples para uso one-shot em staging; nao ha risco de exposicao pois o script e local e o env e controlado.

Decisao `infra09-cloudflare-tunnel-over-port-forward`: Cloudflare Tunnel escolhido em vez de port forwarding no router.
Razao: sem exposicao de IP publico, sem configuracao no router, HTTPS automatico via Cloudflare, outbound-only (mais seguro); desvantagem: dependencia do servico Cloudflare.

Decisao `infra09-cloudflared-etc-path`: config do cloudflared colocada em `/etc/cloudflared/` em vez de `~/.cloudflared/`.
Razao: `cloudflared service install` corre como root via systemd; o servico procura config em `/etc/cloudflared/` e nao no home do utilizador.

Decisao `infra10-avaliar-pgadmin-adminer-ambos`: instalar pgAdmin e Adminer em paralelo em vez de escolher um a priori.
Razao: utilizador nunca usou nenhuma das ferramentas; avaliacao pratica e mais fiavel do que comparacao teorica; qualquer uma pode ser removida sem afetar a outra ou a stack principal.

Decisao `infra10-dbeaver-descartado`: DBeaver descartado como opcao para administracao de BD em staging.
Razao: DBeaver e uma aplicacao desktop, nao uma ferramenta web; nao e adequado para acesso por multiplos utilizadores num servidor; pgAdmin e Adminer sao ambos web-based.

---

## 2026-06-16 — SEC-11 · SEC-12 · SEC-13 · SEC-14

Decisao `sec11-policy-doc-only`: SEC-11 implementado como politica documental (SECRETS_POLICY.md), sem ferramentas de encriptacao.
Razao: projeto de 1 developer; secrets ja estao fora do Git (Render env vars, .env local gitignored); overhead de SOPS/age nao justificado nesta fase.

Decisao `sec12-basic-auth-nginx`: Basic Auth via Nginx escolhido para proteger pgAdmin e Adminer em vez de VPN, Tailscale ou IP allowlist.
Razao: mais simples de configurar e manter; Cloudflare Tunnel ja garante HTTPS (credenciais protegidas em transito); sem dependencias externas adicionais; rotacao de password simples (htpasswd).

Decisao `sec12-htpasswd-repo-gitignored`: ficheiro .htpasswd guardado em `infra/nginx/.htpasswd` dentro do repo (gitignored) em vez de `/etc/nginx/` no host.
Razao: `/etc/nginx/` nao existe no host da VM — o Nginx corre dentro do container Docker; o caminho `./infra/nginx/.htpasswd` e relativo ao repo e montado no container via volume; gitignored para nunca commitar passwords.

Decisao `sec13-sops-diferido-backlog`: SOPS + age diferido para SEC-14 (backlog/futuro) em vez de incluir em SEC-13.
Razao: adicionar encriptacao de secrets em Git so faz sentido com multiplos developers ou GitOps; por agora SEC-13 cobre hardening pratico sem complexidade operacional excessiva.

Decisao `sec14-subplan-de-chatgpt`: plano SOPS+age (originalmente `docs/plans/main/SECRETS_MANAGEMENT_PLAN.md`, elaborado com ChatGPT) convertido em subplan SEC-14 e ficheiro original removido (era untracked).
Razao: o conteudo e valido como referencia futura mas nao e uma tarefa ativa; subplan SEC-14 e o lugar correto para backlog com plano detalhado.

---

## 2026-06-17 — DB-09 · INFRA-10 · SEC-13 (pgAdmin servers.json)

Decisao `infra10-adminer-over-pgadmin`: Adminer escolhido como ferramenta de administracao de BD em detrimento do pgAdmin; pgAdmin removido sem rastros (servico, volume, nginx, GUIDE_PGADMIN.md).
Razao: utilizador avaliou ambas as ferramentas em staging e concluiu que o pgAdmin e demasiado complexo para o caso de uso do projeto (consultas pontuais, inserts, ver tabelas); Adminer cobre tudo com UI mais simples, sem estado persistente, e sem configuracao adicional.

Decisao `infra10-adminer-port-5050`: Adminer movido da porta 5051 para a porta 5050 apos remocao do pgAdmin.
Razao: a porta 5050 estava previamente atribuida ao pgAdmin; reutiliza-la para o Adminer mantem consistencia com o modelo mental do utilizador e com a documentacao existente.

Decisao `db09-pgpassword-over-pgpass`: tentativa de usar ficheiro `pgpass` para pre-autenticar pgAdmin falhou; substituido por variavel de ambiente `PGPASSWORD` no servico pgAdmin.
Razao: o pgAdmin corre como uid 5050 dentro do container e ignora ficheiros `pgpass` com permissoes incorretas do host; `PGPASSWORD` como env var e mais simples e fiavel (decisao relevante para contextos futuros com outras ferramentas PostgreSQL).

Decisao `db09-three-roles-if-not-exists`: roles de BD criados via migration Alembic `0004_create_db_roles.py` com bloco `DO $$` e `IF NOT EXISTS` para cada role.
Razao: garantir idempotencia — a migration pode ser re-executada sem erro se os roles ja existirem; compativel com upgrades e re-deploys em staging.

Decisao `db09-backup-tiered-triennial-monthly`: politica de backups diferenciada com 3 niveis (daily 7d, triennial 30d, monthly permanente) em vez de backup unico diario.
Razao: backup diario com retencao de 7 dias nao cobre o periodo de 3 semanas entre sessoes de trabalho; triennial (a cada 3 dias) garante 30 dias de historico; mensal permanente cobre auditorias e requisitos de dissertacao.

---

## 2026-06-19 — Docs · Dev Local

Decisao `undone-suffix-pending-subplans`: subplans de tarefas ainda nao implementadas renomeados de `<ID>.md` para `<ID>_UNDONE.md`.
Razao: sinalizar visualmente que o plano existe mas a implementacao nao comecou; evita confundir ficheiros de planeamento com implementacoes concluidas; ficheiros historicos (CHANGELOG, HISTORY_AI) ficam intactos — so links operacionais atualizados.

Decisao `project-status-md-central-table`: criado `docs/PROJECT_STATUS.md` gerado pelo `/plans-missing` como tabela central de todos os IDs do projeto.
Razao: nenhum documento existente agregava todos os 97 IDs com estado, FIR lookup e link para subplan numa unica vista; PROJECT_STATUS.md preenche essa lacuna sem duplicar os TODOs.

Decisao `seed-dev-admin-admin`: utilizador de desenvolvimento `admin`/`admin` (role=admin, email=admin@dev.local) criado via `seed_dev.py` idempotente.
Razao: em dev local a BD SQLite esta sempre vazia no primeiro arranque; ter um utilizador pre-criado elimina o passo manual de registo e verificacao de email (que requer Resend em producao).

Decisao `dev-ps1-one-command-startup`: script `dev.ps1` criado para arranque com um comando (seed + backend + frontend + browser).
Razao: passos manuais repetitivos (3 terminais, ordem correta, seed) sao fonte de erro e fricao; o script encapsula tudo e serve de referencia para novos developers.
