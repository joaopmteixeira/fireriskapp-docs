# Serviços e Plataformas — CHICHORRO Fire Risk App

Referência operacional de todos os serviços externos usados no projeto. Para comparação de alternativas e decisões históricas, ver [HOSTING_OPTIONS.md](HOSTING_OPTIONS.md).

---

## Serviços ativos

| Serviço | Função | Endpoint / URL | Notificações | Plano |
| --- | --- | --- | --- | --- |
| **GitHub** | Repositório de código-fonte | [github.com/joaopmteixeira/chichorro-fire-risk-app](https://github.com/joaopmteixeira/chichorro-fire-risk-app) | email pessoal | Free |
| **Render** | Backend hosting (FastAPI/Python) | [chichorro-fire-risk-app.onrender.com](https://chichorro-fire-risk-app.onrender.com) | `chichorrofireriskapp@gmail.com` | Free |
| **Cloudflare Pages** | Frontend hosting (React/Vite) | [fireriskapp-demo.joaopmteixeira.net](https://fireriskapp-demo.joaopmteixeira.net) | `chichorrofireriskapp@gmail.com` | Free |
| **Supabase** | Base de dados PostgreSQL (produção) | — | `chichorrofireriskapp@gmail.com` (Owner) | Free |
| **Sentry** | Error monitoring — frontend + backend | — | `chichorrofireriskapp@gmail.com` | Free |
| **UptimeRobot** | Uptime monitoring e alertas de downtime | — | `chichorrofireriskapp@gmail.com` | Free |
| **Upstash Redis** | Rate limiting do backend (slowapi storage) | — | `chichorrofireriskapp@gmail.com` | Free |
| **Resend** | Email transacional (SMTP para auth flows) | — | — | Free |
| **Linear** | Gestão de tarefas e issues (FIR-XX) | [linear.app](https://linear.app) | email pessoal | Free |

**Email de projeto:** `chichorrofireriskapp@gmail.com` — conta Google dedicada para alertas e notificações de todos os serviços acima (exceto GitHub e Linear que ficam no email pessoal).

---

## Deploy e branches

| Ambiente | Branch | Serviço | URL |
| --- | --- | --- | --- |
| Produção (backend) | `3.1-dev` | Render | [chichorro-fire-risk-app.onrender.com](https://chichorro-fire-risk-app.onrender.com) |
| Produção (frontend) | `3.1-dev` | Cloudflare Pages | [fireriskapp-demo.joaopmteixeira.net](https://fireriskapp-demo.joaopmteixeira.net) |

Deploy automático por push para a branch `3.1-dev`.

---

## Credenciais e variáveis de ambiente

Guardadas em:

- **Render**: Environment Variables no dashboard do serviço
- **Cloudflare Pages**: Settings → Environment Variables
- **Local**: ficheiro `.env` na raiz (não versionado)

Variáveis críticas: `DATABASE_URL`, `SECRET_KEY`, `SENTRY_DSN`, `RESEND_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`.

---

## Limitações dos planos free

| Serviço | Limitação relevante |
| --- | --- |
| **Render** | Spin-down após 15 min de inatividade (~30s cold start); 750h/mês |
| **Supabase** | 500 MB storage; sem connection pooler (PgBouncer) no free tier |
| **Cloudflare Pages** | 500 deploys/mês; sem limite de tráfego |
| **Sentry** | 5 000 erros/mês; retenção de 30 dias |
| **UptimeRobot** | 50 monitores; intervalo mínimo de 5 min |
| **Upstash Redis** | 10 000 comandos/dia; 256 MB storage; fallback para `memory://` se URL em falta |
| **Resend** | 3 000 emails/mês; 100/dia |

---

## Serviços descontinuados / substituídos

| Serviço | Substituído por | Motivo |
| --- | --- | --- |
| Flask (backend) | FastAPI | Performance, tipagem, docs automáticas |
| Neon PostgreSQL | Supabase | Supabase inclui auth, storage e dashboard integrado |
