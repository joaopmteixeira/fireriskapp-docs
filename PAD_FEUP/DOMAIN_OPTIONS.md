# Opções de registo de domínio — `chichorro.pt`

> **Estado:** documento de referência para decisão do registador do domínio `chichorro.pt`.
> Requisito fixo: TLD **.pt** (não avaliadas alternativas .com/.app). Complementar a
> [`VPS_CONSOLIDATION.md`](../deploy/VPS_CONSOLIDATION.md) e
> [`HOSTING_OPTIONS.md`](../deploy/HOSTING_OPTIONS.md).
> Preços consultados em 2026-07-10, sujeitos a alteração pelos fornecedores.

## 1. Contexto

O CHICHORRO precisa de um domínio próprio (`chichorro.pt`) para servir a app fora da rede
local, associado à VPS pública escolhida (ver [`VPS_CONSOLIDATION.md`](../deploy/VPS_CONSOLIDATION.md)).
A entidade gestora oficial do TLD `.pt` é a **Associação DNS.PT**, que cobra **€9,60+IVA/ano
por domínio aos registadores acreditados** — este valor não é o preço final ao público; cada
registador acrescenta a sua margem de gestão, suporte e DNS.

## 2. Comparação de registadores

| Registador | Registo 1.º ano | Renovação/ano | Vantagens | Desvantagens |
| --- | --- | --- | --- | --- |
| **DNS.PT** (registo direto) | N/D — a `.pt` não vende a retalho ao público em geral, apenas fatura registadores acreditados | N/D | Entidade oficial, sem intermediário | Na prática não é acessível a um registo individual direto sem passar por um agente de registo acreditado |
| **PTisp** | ~€16,50 | ~€16,50 | Um dos 3 maiores agentes de registo da DNS.PT; suporte em português; sem burocracia extra; preço mais competitivo dos 3 comparados com custo real | Empresa mais pequena; sem consolidação com a VPS (VPS final é OVHcloud, não PTisp) |
| **Dominios.pt** | €32,90 (+IVA) | €32,90 (+IVA) | Registador nacional dedicado, gestão DNS própria, transferência .pt gratuita | O mais caro dos quatro comparados |
| **OVHcloud** | €11,19 + IVA (€13,76 c/IVA) | €13,39 + IVA (€16,47 c/IVA) | **Consolidação com a VPS** — mesma conta, painel e fatura da OVHcloud VPS-1 já escolhida; inclui Email Starter e proteção DNSSEC; preço de registo inicial mais baixo dos quatro | Renovação sobe para valor próximo do PTisp; gestão de domínio e VPS ficam dependentes do mesmo fornecedor único |

## 3. Recomendação

**OVHcloud**, pelo mesmo motivo que motivou a escolha da VPS: consolidação num único
fornecedor, painel e fatura (mesma lógica de simplificação administrativa documentada em
[`VPS_CONSOLIDATION.md`](../deploy/VPS_CONSOLIDATION.md)). Custo total ano 1: **€13,76 IVA incl.**;
renovação a partir do ano 2: **€16,47/ano IVA incl.** — comparável ao PTisp e claramente
abaixo do Dominios.pt.

Alternativa a considerar caso se prefira separar a gestão do domínio da infraestrutura de
VPS (ex. por segurança — não perder o domínio se a conta VPS tiver problemas): **PTisp**,
com custo muito semelhante (~€16,50/ano) mas sem consolidação de fatura.

## 4. Fontes consultadas

- DNS.PT — [Preços de domínio .PT](https://www.pt.pt/en/domain/domain-prices/) (taxa
  €9,60+IVA/ano cobrada a registadores)
- Dominios.pt — [Preços dos domínios](https://www.dominios.pt/precos/dominio/tld/)
- PTisp — [Registe o .PT perfeito para o seu site](https://blog.ptisp.pt/registo-pt-6euros/) /
  [Como registar um domínio .pt](https://kb.ptisp.com/como-registar-um-dominio-pt/)
- OVHcloud Portugal — [Domínio .pt](https://www.ovhcloud.com/pt/domains/tld/pt/)
