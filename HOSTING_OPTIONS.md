# Opções de Alojamento — CHICHORRO Fire Risk App

Documento de comparação para decisão de infraestrutura de produção. Cobre backend (Python/Flask/gunicorn), frontend (React estático) e base de dados.

---

## 1. Backend (Python / Flask / gunicorn)

| Plataforma | Free tier | Plano pago (mínimo) | Limitações free | Spin-down | Adequado para produção? |
|---|---|---|---|---|---|
| **Render** *(atual)* | Sim | Starter $7/mês | Ephemeral disk, 512 MB RAM | Sim (15 min) | Sim (Starter+) |
| **Railway** | $5 crédito/mês | Usage-based (~$5–10/mês) | Crédito esgota-se | Não | Sim |
| **Fly.io** | 3 VMs 256 MB | ~$1.94/mês/VM | RAM muito baixa para Flask | Não | Sim (2+ VMs) |
| **Heroku** | Não | Eco $5/mês (1 000 h) | — | Sim (Eco) | Sim (Basic+) |
| **PythonAnywhere** | Sim (limitado) | Hacker $5/mês | CPU quota, sem websockets | Não | Para apps simples |
| **Google Cloud Run** | 2 M req/mês grátis | Pay-per-use | Cold start ~1–2 s | Sim | Sim |
| **DigitalOcean App Platform** | Não | Basic $5/mês | — | Não | Sim |
| **VPS Hetzner CX22** | Não | €3,79/mês (2 vCPU, 4 GB) | Gestão manual (nginx + systemd) | Não | Sim (mais controlo) |
| **VPS DigitalOcean Droplet** | Não | $4/mês (1 vCPU, 512 MB) | Gestão manual | Não | Sim |

### Notas relevantes

- **Render free**: instância hiberna após 15 min sem pedidos; o primeiro pedido depois demora ~50 s (cold start). Inaceitável para produção real.
- **Railway**: faturação por uso real (CPU + RAM). Muito competitivo para cargas baixas. Deploy por Git igual ao Render.
- **Fly.io**: requer `fly.toml` + Dockerfile; curva de aprendizagem maior. Mais flexível para multi-região.
- **Google Cloud Run**: excelente para cargas imprevisíveis. Requer containerização (Docker). Free tier generoso.
- **VPS Hetzner**: melhor relação preço/desempenho na Europa. Requer configuração manual mas dá controlo total (SSL, cron, backups).

---

## 2. Frontend (React estático)

| Plataforma | Free tier | Plano pago | Limitações free | CDN global | Deploy por Git |
|---|---|---|---|---|---|
| **Cloudflare Pages** *(atual)* | Ilimitado | Pro $20/mês | 500 builds/mês | Sim (200+ PoPs) | Sim |
| **Vercel** | Sim | Pro $20/mês | 100 GB bandwidth/mês | Sim | Sim |
| **Netlify** | Sim | Pro $19/mês | 100 GB bandwidth, 300 min build/mês | Sim | Sim |
| **GitHub Pages** | Sim | — | 1 GB storage, 100 GB bandwidth | Parcial | Sim (Actions) |
| **Surge.sh** | Sim | $30/mês | Sem CI/CD nativo | Não | Manual |

### Notas relevantes

- **Cloudflare Pages**: melhor opção free para esta app. CDN mais amplo do mercado. Integração com domínios Cloudflare é imediata.
- **Vercel**: ótima DX (developer experience), especialmente para Next.js. Para Vite/React puro é equivalente ao Cloudflare.
- **Netlify**: funcionalidades extra (forms, edge functions) mas limites free mais apertados.
- **GitHub Pages**: gratuito e sem limite de builds, mas CDN menos otimizado e não suporta SPA routing sem hack (`404.html`).

---

## 3. Base de dados

| Opção | Free tier | Plano pago | Migração de código | Notas |
|---|---|---|---|---|
| **SQLite + ephemeral** *(atual)* | Sim | — | Nenhuma | Dados perdidos em redeploy |
| **SQLite + Render Disk** | Não | $7/mês (add-on) | Só `DB_DIR` env var | Simples, ficheiro local |
| **Turso (SQLite distribuído)** | Sim (9 GB, 500 DB) | $29/mês | Mínima (libsql driver) | Mantém SQLite sem migração |
| **Neon (PostgreSQL serverless)** | Sim (0,5 GB) | $19/mês | Média (psycopg2/3) | Boa DX, branching de DB |
| **Supabase (PostgreSQL)** | Sim (500 MB) | $25/mês | Média | Inclui auth, storage, APIs REST |
| **Railway PostgreSQL** | Incluído no crédito | Usage-based | Média | Conveniente se backend no Railway |
| **PlanetScale (MySQL)** | Fechou free tier | $39/mês | Média (mysqlclient) | — |

### Notas relevantes

- **Turso**: permite manter o código SQLite quase inalterado (usa `libsql` em vez de `sqlite3`). Ideal para migração gradual.
- **Neon**: PostgreSQL serverless com branching (útil para CI/CD). Free tier permanente (não expira).
- **Supabase**: se no futuro se quiser substituir a autenticação custom por uma solução gerida, o Supabase Auth é uma opção natural.
- **Render Disk**: a forma mais simples de persistir o SQLite atual — basta montar o disco em `/data` e definir `DB_DIR=/data`.

---

## 4. Recomendações por cenário

| Cenário | Backend | Frontend | Base de dados | Custo/mês |
|---|---|---|---|---|
| **Demo / tese (gratuito)** | Render free | Cloudflare Pages | SQLite ephemeral | €0 |
| **Produção baixo custo** | Render Starter | Cloudflare Pages | Render Disk | ~$14 |
| **Produção + persistência grátis** | Railway | Cloudflare Pages | Neon free | ~$0–5 |
| **Produção escalável** | Fly.io ou Cloud Run | Cloudflare Pages | Neon ou Supabase | $5–25 |
| **Controlo total (Europa)** | VPS Hetzner CX22 | Cloudflare Pages | SQLite no VPS | ~€4 |

### Recomendação para produção definitiva

Para uma aplicação académica/institucional de baixo tráfego com utilizadores convidados:

> **Railway (backend) + Cloudflare Pages (frontend) + Neon (PostgreSQL)** — custo zero ou quase zero, sem spin-down, dados persistentes, deploy por Git.

Alternativa de menor custo total e gestão mais simples:

> **Hetzner VPS CX22 (nginx + gunicorn + SQLite) + Cloudflare Pages** — €3,79/mês, controlo total, sem dependência de plataformas PaaS.
