# BACK-02 — Melhorar Logging

**Estado:** ✅ Implementado  
**Ficheiro alterado:** `app/backend/Flask.py`

---

## O que foi feito

### 1. Coluna `user_agent` no `access_log`

Adicionada migração idempotente em `_init_db()`:

```sql
ALTER TABLE access_log ADD COLUMN IF NOT EXISTS user_agent TEXT
```

### 2. `_write_access_log()` actualizado

Passa a capturar o `User-Agent` do pedido e insere-o na nova coluna.

### 3. Tentativas de login falhadas

O handler `/auth/login` passa a registar dois novos eventos:

| Evento | Condição |
|--------|----------|
| `login_failed:unverified` | Conta existe mas e-mail não verificado |
| `login_failed` | Credenciais inválidas (utilizador não encontrado ou password errada) |

O `username` registado é o valor enviado no payload — pode ser arbitrário.

### 4. Request ID para erros 500

- `@app.before_request` gera `g.request_id = uuid.uuid4().hex[:8]` em cada pedido.
- `@app.errorhandler(500)` loga o erro com o `request_id` e devolve-o no JSON:
  ```json
  {"error": "INTERNAL_ERROR", "request_id": "a1b2c3d4"}
  ```

### 5. `/admin/log` actualizado

Passa a devolver a coluna `user_agent` em cada entrada do log.

---

## Eventos logados

| `event` | Quando |
|---------|--------|
| `login` | Login com sucesso |
| `logout` | Logout |
| `login_failed` | Credenciais inválidas |
| `login_failed:unverified` | E-mail não verificado |
