# DECISIONS_LOG — Registo de Decisões de Projeto

Registo cronológico de decisões técnicas e de produto relevantes tomadas durante o desenvolvimento.
Formato: data, tema, decisão, razão.

---

## 2026-06-29 — UI-11: arquitetura do modal de suporte

**Decisão 1:** Modal colocado fora do `<form>` de login.
Razão: O modal estava dentro do `<form>`, o que causava um submit não intencional ao clicar em "Enviar" no formulário de suporte. Mover para fora elimina a interferência.

**Decisão 2:** `fetch` direto em vez de `postJson` no `SupportModal.tsx` (inicial — revertida no dia seguinte).
Razão: Utilizador não tem sessão activa na LoginPage, pelo que o header CSRF seria inútil.

**Decisão 3:** FAB ("Suporte") em vez de link de texto no rodapé da LoginPage.
Razão: Maior visibilidade; evita confundir com link de navegação.

**Decisão 4:** Rate limit 3 pedidos/hora no `POST /support/request`.
Razão: Prevenir spam sem penalizar utilizadores legítimos com problemas de acesso.

**Decisão 5:** Migration `0004_create_db_roles.py` corrigida para usar `current_database()` em vez de nome de BD hardcoded nos GRANT/REVOKE.
Razão: Portabilidade entre ambientes (dev SQLite, staging, produção) sem editar a migration.

---

## 2026-06-30 — UI-11: split-origin, email HTML, ENUM, UI-13

**Decisão 6:** Substituir `fetch` direto por `postJson` no `SupportModal.tsx`.
Razão: Arquitetura split-origin (Cloudflare Pages frontend + Render backend) exige que os pedidos passem por `VITE_API_BASE_URL`; `fetch` direto com URL relativa funciona em dev (proxy Vite) mas falha em produção.

**Decisão 7:** Email de confirmação com tabela HTML colorida (`#c0392b` header) em vez de texto simples.
Razão: Pedido explícito do utilizador; melhora a experiência e credibilidade do serviço.

**Decisão 8:** Assunto do email com ID do pedido: `[#<ID>] Pedido de suporte - CHICHORRO`.
Razão: Facilita rastreio e resposta a pedidos específicos.

**Decisão 9:** Validação de telemóvel restrita a números portugueses (`9[1236]\d{7}`).
Razão: O campo é opcional; quando preenchido deve ser válido; o projeto é nacional.

**Decisão 10:** Coluna `status` convertida para ENUM PostgreSQL `support_status` (open/pending/working/closed).
Razão: Integridade de dados — garante que só valores válidos são aceites a nível de BD; prepara para UI-13 (filtros por status).

**Decisão 11:** Migration `0006` usa `DROP DEFAULT` → `ALTER COLUMN TYPE USING` → `SET DEFAULT`.
Razão: PostgreSQL não faz cast automático de `server_default` varchar para ENUM; tentativa sem DROP DEFAULT resulta em `DatatypeMismatch`.

**Decisão 12:** UI-13 planeado (subplan UNDONE) mas não implementado nesta sessão.
Razão: Pedido explícito do utilizador — só elaborar o plano, não implementar.

---

## 2026-07-01 — UI-11: merge e encerramento

**Decisão 13:** Merge de `feat/ui-11-support-modal` com `--no-ff`.
Razão: Padrão do projeto para features com ID Linear — preserva o histórico da branch no grafo git.

**Decisão 14:** TODO_LIST.md atualizado manualmente em vez de tool automática.
Razão: Permitiu revisão explícita pelo utilizador antes de confirmar.
