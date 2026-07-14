# Anexo — Prova de custo da VPS `chichorro.pt` (OVHcloud VPS-2, gama 2027)

> **Nota:** existe também uma captura de ecrã real desta página em
> [`anexos/anexo1_vps_precos.png`](anexos/anexo1_vps_precos.png), capturada em 2026-07-10. Este
> ficheiro mantém-se como transcrição textual complementar (pesquisável, sem depender de imagem).

**Fonte:** [www.ovhcloud.com/pt/vps/](https://www.ovhcloud.com/pt/vps/)
**Data de consulta:** 2026-07-10

> A gama de VPS da OVHcloud mudou de nomenclatura desde a última captura de ecrã existente no
> repositório (2026-05-06, gama "2026"). A gama atual chama-se "2027" e os planos e
> especificações associadas ao nome VPS-1/2/3 mudaram — ver comparação na secção seguinte.

## Preços publicados — gama VPS 2027

| Plano | vCores | RAM | Disco | Preço + IVA/mês | Preço IVA incl./mês |
| --- | --- | --- | --- | --- | --- |
| VPS-1 | 2 | 4 GB | 40 GB NVMe | 3,81 € | 4,69 € |
| **VPS-2 (escolhido)** | 4 | 8 GB | 75 GB NVMe | 7,21 € | 8,87 € |
| VPS-3 | 6 | 12 GB | 100 GB NVMe | 10,40 € | 12,79 € |
| VPS-4 | 8 | 24 GB | 200 GB NVMe | 19,96 € | 24,55 € |

Todos os planos incluem: backup automatizado diário, tráfego ilimitado, proteção anti-DDoS.
Preço "a partir de" pressupõe pré-pagamento anual (`pricing=upfront12` no configurador).

## Regimes de compromisso e desconto

O configurador de checkout da OVHcloud permite escolher entre três regimes de fidelização,
cada um com desconto diferente sobre o preço mensal base:

| Regime | Desconto | Faturação |
| --- | --- | --- |
| Sem compromisso | 0% | Mensal |
| 6 meses | -5% | Pago de uma vez no início do período |
| **12 meses (escolhido)** | -15% | Pago de uma vez no início do período |

Os valores de €7,21 (+IVA) / €8,87 (IVA incl.) por mês do VPS-2 na tabela acima já
correspondem ao regime de **12 meses**, confirmado no ecrã de checkout: total anual de
€86,52 + IVA (€7,21 × 12), faturado como um único pagamento de €106,44 (IVA incl.) no início
de cada período de 12 meses. Optou-se por este regime por ser o mais económico a médio prazo.

Adicionalmente, o checkout oferece a opção de **Backup Snapshot** (€0,50/mês, €6,00/ano),
usada para tirar uma imagem pontual do disco antes de operações de risco — incluída no pedido
de despesa (ver secção 3.1 e 4.1 de
[`FEUP_PEDIDO_DESPESA.md`](FEUP_PEDIDO_DESPESA.md)).

## Transcrição literal do bloco de preços (secção "VPS 2027")

```text
VPS-1
A partir de 3,81 € + IVA/mês ou seja 4,69 € IVA incl./mês
2 vCores | 4 GB RAM
Backup automatizado 1 dia | Tráfego ilimitado | 500 Mbps de largura de banda pública

VPS-2
A partir de 7,21 € + IVA/mês ou seja 8,87 € IVA incl./mês
4 vCores | 8 GB RAM | 75 GB SSD NVMe
Backup automatizado 1 dia | Tráfego ilimitado | 1 Gbps de largura de banda pública

VPS-3
A partir de 10,40 € + IVA/mês ou seja 12,79 € IVA incl./mês
6 vCores | 12 GB RAM | 100 GB SSD NVMe
Backup automatizado 1 dia | Tráfego ilimitado | 2 Gbps de largura de banda pública

VPS-4
A partir de 19,96 € + IVA/mês ou seja 24,55 € IVA incl./mês
8 vCores | 24 GB RAM | 200 GB SSD NVMe
Backup automatizado 1 dia | Tráfego ilimitado | 3 Gbps de largura de banda pública
```
