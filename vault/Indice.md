---
tipo: indice
tags: [chichorro, moc]
---

# Indice CHICHORRO

Modelo de risco: `RI = POI x CTI x ((DPI + ESCI) / 2)`

## Fatores

- [[POI]] -- Probabilidade de Ocorrência de Incêndio
- [[CTI]] -- Consequências Totais do Incêndio
- [[DPI]] -- Desenvolvimento e Propagação do Incêndio
- [[ESCI]] -- Eficácia do Socorro e Combate ao Incêndio
- [[RI]] -- Risco de Incêndio

## Subfatores

### POI

  - [[POI_CC]] -- Carga Combustível
  - [[POI_IEE]] -- Instalações de Energia Elétrica
  - [[POI_IA]] -- Instalação de Aquecimento
  - [[POI_ICONFA]] -- Instalação de Confeção com Chama
  - [[POI_ICONSA]] -- Instalação de Confeção sem Chama
  - [[POI_IVCA]] -- Instalação de Ventilação e Climatização
  - [[POI_ILGC]] -- Instalação de Líquidos e Gases Combustíveis
  - [[POI_EF]] -- Exposição ao Fogo
  - [[POI_EA]] -- Empena e Adjacência
  - [[POI_FA]] -- Fachada
  - [[POI_PPP]] -- Plano de Prevenção e Proteção
  - [[POI_ATIV]] -- Atividade / Uso

### CTI

  - [[CTI_CI]] -- Cenário de Incêndio
  - [[CTI_VHE]] -- Vias Horizontais de Evacuação
  - [[CTI_VVE]] -- Vias Verticais de Evacuação

### DPI

  - [[DPI_REIC]] -- Resistência Estrutural e Isolamento de Construção
  - [[DPI_EI]] -- Estanquidade e Isolamento
  - [[DPI_VDGF]] -- Vãos, Diedros e Guarda-fogo
  - [[DPI_PE]] -- Parede Exterior
  - [[DPI_OGS]] -- Organização e Gestão de Segurança

### ESCI

  - [[ESCI_GP]] -- Guarnição e Prontidão
  - [[ESCI_SID]] -- Sinalização, Iluminação e Deteção
  - [[ESCI_AE]] -- Acessibilidade Exterior
  - [[ESCI_HE]] -- Hidrantes Exteriores
  - [[ESCI_EXT]] -- Extintores
  - [[ESCI_RIA]] -- Rede Interior de Incêndio Armada
  - [[ESCI_CPB]] -- Corpo Privado de Bombeiros

## Fontes

- [[Tese 3.0 (JPT)]] (tese30)
- [[Tese 3.1 (RS)]] (tese31)
- [[Tese 4.0 (IC)]] (tese40)
- [[RT-SCIE 1532-2008]] (rtscie)
- [[RT-SCIE 135-2020]] (rtscie2020) -- TODO
- [[Backend (FastAPI)]] (backend)
- [[Frontend (React)]] (frontend)

## Conceitos

- [[Utilizacao-Tipo]]
- [[Categoria de Risco]]
- [[Classificacao RI]]
- [[Compartimentacao]]
- [[Evacuacao]]
- [[Reacao ao Fogo]]
- [[Resistencia ao Fogo]]
- [[Carga de Incendio]]
- [[Efetivo]]
- [[Plano de Prevencao e Emergencia]]

## Como usar

- Abre `docs/` no Obsidian para ver o Graph View completo.
- Corre `python scripts/map_sources.py` para preencher as tabelas de mencoes.
- Tags: `#subfator`, `#fator`, `#fonte`, `#conceito`

