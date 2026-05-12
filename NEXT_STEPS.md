# Estado do Projeto e Próximos Passos

Última atualização: 2026-05-12

---

## Estado atual

| Área | Estado |
| --- | --- |
| Modelo CHICHORRO 3.1 | ✅ Completo (11/11 paridade backend, e2e aprovado) |
| Autenticação e sessões | ✅ Completo (AUTH-01..08, AUTH-11, AUTH-12) |
| Hardening de segurança | ✅ Completo (SEC-01..03, feat/security mergeado) |
| Auditoria segurança/UX | ✅ Completo (S-01..02, U-01..04) |
| Branch ativo | `3.1-dev` |

Detalhe completo de tudo o que foi implementado: ver [CHANGELOG.md](CHANGELOG.md).

---

## Pendente — Prioridade Média

### AUTH-09 — Editar Perfil

Área de perfil do utilizador com as seguintes opções:

- Alterar nome de utilizador
- Alterar e-mail (com re-verificação via link enviado para o novo endereço)
- Alterar palavra-passe (requer palavra-passe atual)
- Apagar conta — eliminação permanente com dupla confirmação (utilizador tem de escrever texto específico)

### BACK-02 — Melhorar Logging

Adicionar ao `access_log`:

- Registo de tentativas de login falhadas
- IP de origem e User-Agent
- Request IDs para correlação de erros 500

### UI-02 — Página de Documentação

Página de DOCS integrada na app com documentação e manuais de utilização.

### UI-03 — Página de Ajuda

Página HELP integrada na app.

### UI-04 — FAQs

Página de perguntas frequentes integrada na app.

### UI-05 — Bug Report

Formulário de reporte de bugs na app. Canal de destino a definir: e-mail, GitHub Issues ou ClickUp.

### AUTH-10 — Sistema de Roles/Permissões

Estrutura sugerida: `admin`, `engineer`, `viewer`, `demo`.

**Importante:** verificação de permissões sempre no backend. Frontend não é segurança.

### UI-06 — Preferências / Definições

Página de configurações do utilizador (conteúdo a especificar).

### BACK-01 — Reestruturar Backend Flask

`Flask.py` está atualmente monolítico. Estrutura alvo:

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

### INFRA-01 — Monitorização

Ferramentas candidatas: Sentry, BetterStack, UptimeRobot, Render monitoring.
Objetivos: detetar erros, uptime, debugging, auditoria.

### DB-02 — Estratégia de Backups

Garantir backup de: PostgreSQL Neon, env vars, configs de deployment.

---

## Pendente — Prioridade Baixa / Futuro

### UI-01 — Gráfico de Impacto de Intervenções

Tornado chart (bar chart horizontal) no módulo de Intervenções: impacto individual de cada intervenção selecionada.

- Backend: novo endpoint `POST /RI/interv/impact`
- Frontend: Recharts (já disponível)
- Custo: ~34 cálculos de RI por chamada (aceitável)

### UI-07 — Dark Mode

Tema escuro na aplicação.

### UI-08 — Chatbot AI

Assistente de IA para ajudar os utilizadores a compreender o CHICHORRO e a usar a aplicação (Claude API ou similar).

### TEST-02 — Testes Automatizados

Unit tests, integration tests, e2e tests. Objetivos: estabilidade, prevenção de regressões, validação auth e modelo CHICHORRO.

### INFRA-02 — Pipeline CI/CD

GitHub Actions + Render Deploy Hooks. Objetivos: deploy automático, testes automáticos, linting, validação de build.

### BACK-03 — Avaliar Migração Flask → FastAPI

Não prioritário. Flask continua válido. Considerar apenas quando o backend crescer significativamente ou surgir necessidade real de async.

---

## Backlog — Versão Futura (pós-3.1)

Propostas de Rui Sobral (dissertação, secção 7.2) — fora do âmbito do modelo 3.1:

| ID | Descrição |
| --- | --- |
| MODEL-01 | Método simplificado baseado no CHICHORRO 2.0 |
| MODEL-02 | Alterar ordem do Cenário 4 (CI → VVE → VHE alternativo) |
| MODEL-03 | Afinação de custos €/m² via PRONIC |
| MODEL-04 | Intervenções adicionais: Gerador, Grupo de bombagem, Cablagem, Evacuação alternativa |
| MODEL-05 | Georreferenciação e base de dados de edifícios |
| MODEL-06 | Tratamento de edifícios devolutos |
| MODEL-07 | Integração com Firecheck 2.0 |
