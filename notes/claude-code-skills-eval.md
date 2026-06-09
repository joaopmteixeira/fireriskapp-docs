# Avaliacao de Claude Code Skills (do video "These 6 Are The Best")

> Origem: video [I Tried 100+ Claude Code Skills. These 6 Are The Best](https://www.youtube.com/watch?v=eRS3CmvrOvA).
> Avaliado para o contexto do projeto CHICHORRO em 2026-06-08.

As 6 skills do video sao de *meta-workflow* (melhoram como o Claude Code trabalha), nao de
dominio. Tres delas ja estao no setup atual; das outras tres, so o Context Mode foi adotado.

## Veredicto rapido

| # | Skill | O que faz | Ja disponivel? | Adotar? |
|---|-------|-----------|----------------|---------|
| 1 | Skill Creator | Cria skills a partir de linguagem natural | Sim (`anthropic-skills:skill-creator`) | Ja temos |
| 2 | Superpowers | Metodologia dev: brainstorm -> plano -> TDD -> review | Sim (v5.1.0) | Ja temos |
| 3 | /review + /ultra review | Code review do diff; ultra = agentes na cloud | Sim (`/code-review`) | Ja temos |
| 4 | Context Mode | Comprime output de ferramentas (~98%) para SQLite local | Nao | **Sim** |
| 5 | ClaudeMem | Memoria persistente automatica (SQLite + vetores) | Nao | Nao (por agora) |
| 6 | GSD | Context engineering via sub-agents | Nao | Nao |

## Detalhe e instalacao

### 1. Skill Creator (ja temos)

Cria novas skills a partir de descricao em linguagem natural (frontmatter, testes, packaging).
Uso: `/skill-creator` ou pedir "cria uma skill que ...".

### 2. Superpowers (ja temos)

Metodologia completa de desenvolvimento sobre skills compostas: brainstorm -> plano -> TDD ->
review. Instalado via marketplace oficial (`superpowers@claude-plugins-official` v5.1.0).
Uso: `/superpowers:brainstorm`, depois planeamento e execucao.

Nota: nao forca por si "rever antes de codigo" — isso depende do Plan Mode ou de um hook
dedicado (ver [hooks de guardrail](#follow-ups-de-workflow-hooks)).

### 3. /review + /ultra review (ja temos)

Reve o **diff atual** (branch/working tree), nao apenas PRs:

- `/code-review` -> diff local da branch.
- `/code-review ultra` -> review multi-agente na cloud da branch atual.
- `/code-review ultra <PR#>` -> review de um PR do GitHub.
- Flags: `--comment` (comentarios inline no PR), `--fix` (aplica correcoes).

### 4. Context Mode (INSTALADO)

Comprime os blocos brutos que as ferramentas devolvem (test logs, snapshots Playwright,
`graph.json`, payloads GitHub/Linear), isolando-os num indice local (SQLite + FTS5) e
passando so summaries + handles de recuperacao. Reduz uso de contexto ~98% e prolonga
sessoes longas. E um plugin que inclui um MCP server local (sem config MCP manual, sem
servico em background). Licenca MIT. Repo: <https://github.com/mksglu/context-mode>.

Instalacao (Claude Code v1.0.33+):

```text
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode   # user scope
```

Reiniciar (ou `/reload-plugins`) e validar com `/context-mode:ctx-doctor` (tudo `[OK]`).

Estado (2026-06-08): instalado em **user scope**, v1.0.162; `ctx-doctor` todo `[OK]`.
Bun 1.3.14 instalado (`irm bun.sh/install.ps1 | iex`) -> performance passou de `NORMAL`
para `FAST (Bun)` (3-5x mais rapido na compressao). Os hooks do Context Mode coexistem
com os guardrails locais (arrays de hooks fazem merge).

Comandos: `/context-mode:ctx-stats`, `/context-mode:ctx-search`, `/context-mode:ctx-index`,
`/context-mode:ctx-purge` (destrutivo), `/context-mode:ctx-upgrade`.

### 5. ClaudeMem (nao adotado)

Memoria persistente entre sessoes: captura automatica + compressao por IA, armazenada em
SQLite + Chroma (vetores), com injecao de contexto no arranque.
Repo: <https://github.com/thedotmack/claude-mem>. Instalacao: `npx claude-mem install`.

Porque nao (por agora): sobrepoe-se ao sistema de memoria ja existente (`memory/MEMORY.md`).
Nao toca nos brain files nem nos daily summaries. O sintoma "MEMORY.md desatualizado" e de
disciplina de escrita e resolve-se melhor com um hook leve (ver follow-ups) do que trocar
memoria curada-a-mao por captura automatica (mais ruido, menos controlo, dois sistemas a
injetar contexto).

### 6. GSD - Get Shit Done (nao adotado)

Framework de context engineering com sub-agents para evitar "context rot".
Repo: <https://github.com/open-gsd/get-shit-done-redux>. Instalacao: `npx get-shit-done-cc@latest`.

Porque nao: e um framework de workflow concorrente do Superpowers (mesmas fases: planeamento,
sub-agents, execucao, gestao de contexto). Da para instalar os dois, mas competem em slash
commands, metodologia e hooks — friccao sem ganho num projeto solo ja padronizado em Superpowers.
So valeria para um A/B consciente.

## Follow-ups de workflow (hooks)

Dois guardrails decididos a partir desta analise (implementados em `.claude/settings.local.json`,
scripts em `.claude/hooks/`):

- **Plano antes de editar**: hook PreToolUse em `Edit`/`Write` que trava a primeira edicao da
  sessao ate o Claude confirmar que apresentou plano — rede de seguranca para quando o Plan
  Mode e esquecido.
- **Atualizar MEMORY.md**: hook Stop que lembra (uma vez por sessao, quando ha mudancas no
  working tree) de rever e atualizar o `MEMORY.md` antes de fechar.

## Fontes

- Video: <https://www.youtube.com/watch?v=eRS3CmvrOvA>
- Geeky Gadgets: <https://www.geeky-gadgets.com/best-claude-code-skills/>
- Context Mode: <https://github.com/mksglu/context-mode>
- Superpowers: <https://github.com/obra/superpowers>
- ClaudeMem: <https://github.com/thedotmack/claude-mem>
- GSD redux: <https://github.com/open-gsd/get-shit-done-redux>
