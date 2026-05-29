# Método de Cálculo CHICHORRO v3.1 — Tabelas de referência por subfator

**Versão:** 3.1  
**Autores:** João Pedro Teixeira e Rui Sobral  
**Documento:** Referência técnica para entidades licenciadoras

---

## Introdução

O método CHICHORRO avalia o risco de incêndio em edifícios históricos através de quatro fatores principais:

$$RI = f(POI,\ CTI,\ DPI,\ ESCI)$$

| Fator | Designação | Subfatores |
|---|---|---|
| POI | Probabilidade de Ocorrência de Incêndio | 12 |
| CTI | Consequências Totais de Incêndio | Calculado por fórmula |
| DPI | Desenvolvimento e Propagação do Incêndio | 5 |
| ESCI | Eficácia de Socorro e Combate ao Incêndio | 7 |

### Regra de agregação por módulo

Cada módulo (POI, DPI, ESCI) é calculado como a **média aritmética** dos seus subfatores com valor **> 0**:

> O valor **0,00** indica **"Não se aplica"** — o subfator é inexistente no edifício e é excluído da média.

### Interpretação dos valores

| Intervalo | Significado |
|---|---|
| < 1,00 | Favorável — reduz o risco |
| = 1,00 | Neutro — condição base |
| > 1,00 | Penalizador — aumenta o risco |

---

## 1. POI — Probabilidade de Ocorrência de Incêndio

$$POI = \frac{\sum_{i}\ POI_i}{\text{n.º de subfatores com valor} > 0}$$

---

### 1.1 POI_CC — Características Construtivas

Avalia o risco associado à combustibilidade estrutural, presença de infiltrações e adequação do revestimento.

> **Nota:** O ano de construção é registado como dado complementar mas não entra no cálculo.

**Subcaso A — Estrutura Incombustível**

| Infiltrações | Revestimento Adequado | Revestimento Não Adequado |
|---|---|---|
| Sem infiltrações | 1,00 | 1,10 |
| Com infiltrações | 1,30 | 1,40 |

**Subcaso B — Estrutura Combustível**

| Infiltrações | Revestimento Adequado | Revestimento Não Adequado |
|---|---|---|
| Sem infiltrações | 1,20 | 1,30 |
| Com infiltrações | 1,60 | 1,70 |

---

### 1.2 POI_IEE — Instalações de Energia Elétrica

Avalia o risco da instalação elétrica quanto à conformidade regulamentar, existência de ligações indevidas e estado dos componentes.

**Caso 1 — Respeita regulamentação**

| | |
|---|---|
| Respeita regulamentação | **1,00** |

**Caso 2 — Não respeita regulamentação + Ligações piratas**

| | |
|---|---|
| Ligações piratas existentes | **1,80** |

**Caso 3 — Não respeita + Sem ligações piratas**

| Potência instalada vs. projeto (PIPC) | Proteção nos quadros | Condutores em Bom Estado (BCC) | Condutores em Mau Estado (MCC) |
|---|---|---|---|
| Igual ao projeto | Disjuntores | 1,00 | 1,10 |
| Igual ao projeto | Fusíveis | 1,30 | 1,40 |
| Superior ao projeto | Disjuntores | 1,20 | 1,30 |
| Superior ao projeto | Fusíveis | 1,50 | 1,60 |

---

### 1.3 POI_IA — Instalações de Aquecimento

Avalia o risco das instalações de aquecimento em função do tipo e conformidade com a regulamentação.

| Aplica? | Tipo de instalação | Subtipo / Conduta | Respeita regulamentação | Não respeita |
|---|---|---|---|---|
| Não se aplica | — | — | **0,00** | — |
| Inexistência de IA | — | — | **0,85** | — |
| Aplica | Centrais Térmicas | — | **1,00** | **1,20** |
| Aplica | Aparelhos Autónomos | Elétrico | **1,05** | **1,25** |
| Aplica | Aparelhos Autónomos | Catalítico | **1,10** | **1,35** |
| Aplica | Combustão Sólida | Sup. Incombustível + Conduta Simples | **1,20** | **1,40** |
| Aplica | Combustão Sólida | Sup. Incombustível + Conduta Dupla | **1,40** | **1,60** |
| Aplica | Combustão Sólida | Sup. Combustível + Conduta Simples | **1,40** | **1,60** |
| Aplica | Combustão Sólida | Sup. Combustível + Conduta Dupla | **1,60** | **1,80** |

---

### 1.4 POI_ICONFA — Instalações de Confeção de Alimentos (com fogão/forno a combustão)

Avalia o risco das instalações de cozinha com equipamentos de combustão.  
**Não se aplica → 0,00.**

**Subcaso A — Combustível Sólido**

| Conformidade instalação | Ventilação de exaustão | Corte elétrico automático |
|---|---|---|
| | **Com** | **Sem** |
| Respeita + Ventilação Respeita | 1,00 | 1,10 |
| Respeita + Ventilação Não Respeita | 1,30 | 1,40 |
| Respeita + Sem ventilação | 1,50 | 1,50 |
| Não Respeita + Ventilação Respeita | 1,10 | 1,15 |
| Não Respeita + Ventilação Não Respeita | 1,35 | 1,45 |
| Não Respeita + Sem ventilação | 1,60 | 1,60 |

**Subcaso B — Outros combustíveis (gás, etc.)**

| Conformidade instalação | Ventilação de exaustão | Corte elétrico automático |
|---|---|---|
| | **Com** | **Sem** |
| Respeita + Ventilação Respeita | 1,00 | 1,05 |
| Respeita + Ventilação Não Respeita | 1,20 | 1,30 |
| Respeita + Sem ventilação | 1,40 | 1,40 |
| Não Respeita + Ventilação Respeita | 1,05 | 1,10 |
| Não Respeita + Ventilação Não Respeita | 1,25 | 1,35 |
| Não Respeita + Sem ventilação | 1,50 | 1,50 |

---

### 1.5 POI_ICONSA — Instalações de Confeção de Alimentos (sem fogão/forno a combustão)

| Aplica? | Conformidade regulamentar | Valor |
|---|---|---|
| Não se aplica | — | **0,00** |
| Aplica | Respeita | **1,00** |
| Aplica | Não respeita | **1,10** |

---

### 1.6 POI_IVCA — Instalações de Ventilação e Condicionamento de Ar

| Aplica? | Conformidade instalação | Conformidade utilização | Valor |
|---|---|---|---|
| Não se aplica | — | — | **0,00** |
| Aplica | Respeita | Respeita | **1,00** |
| Aplica | Respeita | Não respeita | **1,20** |
| Aplica | Não respeita | Respeita | **1,10** |
| Aplica | Não respeita | Não respeita | **1,30** |

---

### 1.7 POI_ILGC — Instalações de Líquidos e Gases Combustíveis

| Aplica? | Conformidade armazenamento | Conformidade utilização | Valor |
|---|---|---|---|
| Não se aplica | — | — | **0,00** |
| Aplica | Respeita | Respeita | **1,00** |
| Aplica | Respeita | Não respeita | **1,20** |
| Aplica | Não respeita | Respeita | **1,10** |
| Aplica | Não respeita | Não respeita | **1,40** |

---

### 1.8 POI_EF — Exposição ao Fogo Exterior

Avalia o risco de propagação de incêndio a partir de edifícios vizinhos.  
**Não se aplica → 0,00.**  
**Elementos construtivos conformes (Respeita) → 1,00 em todos os casos.**

Os valores abaixo aplicam-se quando os **elementos construtivos não respeitam** a regulamentação:

**UT I a XI — Altura ≤ 9 m**

| Distância ao edifício vizinho | Elementos construtivos Não Conformes |
|---|---|
| > 8 m | 1,00 |
| > 4 m e ≤ 8 m | 1,05 |
| ≤ 4 m | 1,20 |

**UT I a XI — Altura > 9 m**

| Distância ao edifício vizinho | Elementos construtivos Não Conformes |
|---|---|
| > 16 m | 1,00 |
| > 8 m e ≤ 16 m | 1,05 |
| > 4 m e ≤ 8 m | 1,20 |
| ≤ 4 m | 1,40 |

**UT XII — Carga de Incêndio (CI) ≤ 500 MJ/m²**  
*(valores idênticos a UT I–XI)*

**UT XII — CI > 500 e ≤ 5 000 MJ/m² — Altura ≤ 9 m**

| Distância ao edifício vizinho | Elementos construtivos Não Conformes |
|---|---|
| > 16 m | 1,00 |
| > 8 m e ≤ 16 m | 1,05 |
| > 4 m e ≤ 8 m | 1,30 |
| ≤ 4 m | 1,50 |

**UT XII — CI > 500 e ≤ 5 000 MJ/m² — Altura > 9 m**

| Distância ao edifício vizinho | Elementos construtivos Não Conformes |
|---|---|
| > 12 m | 1,00 |
| > 8 m e ≤ 12 m | 1,30 |
| > 4 m e ≤ 8 m | 1,40 |
| ≤ 4 m | 1,60 |

**UT XII — CI > 5 000 MJ/m²** *(sem distinção de altura)*

| Distância ao edifício vizinho | Elementos construtivos Não Conformes |
|---|---|
| > 16 m | 1,00 |
| > 12 m e ≤ 16 m | 1,10 |
| > 8 m e ≤ 12 m | 1,40 |
| > 4 m e ≤ 8 m | 1,60 |
| ≤ 4 m | 1,80 |

---

### 1.9 POI_EA — Exposição ao Fogo pelo Átrio

Avalia o risco de propagação pelo átrio/empena entre edifícios adjacentes.

| Aplica? | Empena | Guarda-fogo | Valor |
|---|---|---|---|
| Não se aplica | — | — | **0,00** |
| Aplica | Respeita | Respeita | **1,00** |
| Aplica | Respeita | Não respeita | **1,20** |
| Aplica | Não respeita | Respeita | **1,10** |
| Aplica | Não respeita | Não respeita | **1,30** |

---

### 1.10 POI_FA — Propagação pelo Interior da Fração

Avalia o risco de propagação de incêndio entre frações contíguas.  
**Não se aplica → 0,00.**  
**Envolv. fração conforme (Respeita) → 1,00.**

Quando a envolvente da fração **não respeita**, o resultado é o **máximo** de quatro sub-valores independentes (Lajes, Paredes, Vãos, Condutas), cada um função do risco das frações vizinhas:

**Sub-tabela: Lajes**

| Conformidade Lajes | POI vizinhas menor | POI vizinhas igual / não sabe | POI vizinhas maior |
|---|---|---|---|
| Respeita | 1,00 | 1,00 | 1,00 |
| Não respeita | 1,20 | 1,30 | 1,40 |

**Sub-tabela: Paredes**

| Conformidade Paredes | POI vizinhas menor | POI vizinhas igual / não sabe | POI vizinhas maior |
|---|---|---|---|
| Respeita | 1,00 | 1,00 | 1,00 |
| Não respeita | 1,05 | 1,15 | 1,20 |

**Sub-tabela: Vãos**

| Conformidade Vãos | Caixa enclausurada | POI vizinhas menor | POI vizinhas igual / não sabe | POI vizinhas maior |
|---|---|---|---|---|
| Respeita | — | 1,00 | 1,00 | 1,00 |
| Não respeita | Com | 1,00 | 1,00 | 1,00 |
| Não respeita | Sem | 1,10 | 1,15 | 1,20 |

**Sub-tabela: Condutas**

| Conformidade Condutas | POI vizinhas menor | POI vizinhas igual / não sabe | POI vizinhas maior |
|---|---|---|---|
| Respeita | 1,00 | 1,00 | 1,00 |
| Não respeita | 1,05 | 1,15 | 1,20 |

> **POI_FA = max(Lajes, Paredes, Vãos, Condutas)**

---

### 1.11 POI_PPP — Plano de Prevenção e Procedimentos de Emergência

| Aplica? | Plano existe? | Implementado? | Valor |
|---|---|---|---|
| Não se aplica | — | — | **0,00** |
| Aplica | Sim e não necessário | — | **0,80** |
| Aplica | Sim | Sim | **1,00** |
| Aplica | Sim | Não | **1,20** |
| Aplica | Não | — | **1,40** |

---

### 1.12 POI_ATIV — Atividade / Tipo de Utilização

| Utilização-Tipo (UT) | Subtipo | Valor |
|---|---|---|
| I — Habitação | — | 1,00 |
| II — Estacionamento | — | 1,00 |
| III — Administrativos | — | 1,00 |
| IV — Escolas, Creches ou Jardins de Infância | — | 1,10 |
| V — Hospitais, Enfermarias, Lares, Consultórios ou Clínicas | — | 1,10 |
| VI — Salas de Espetáculo e Reuniões Públicas | — | 1,40 |
| VII — Hotéis, Hostéis, Pensões ou Albergarias | — | 1,10 |
| VII — Restauração | — | 1,20 |
| VIII — Comércio | Alimentação | 1,20 |
| VIII — Comércio | Calçado | 1,00 |
| VIII — Comércio | Eletrodomésticos | 1,00 |
| VIII — Comércio | Farmácia | 1,00 |
| VIII — Comércio | Mercearia c/ garrafas de gás | 1,20 |
| VIII — Comércio | Têxteis | 1,20 |
| VIII — Comércio | Encadernação | 1,40 |
| VIII — Comércio | Outros | 1,20 |
| IX — Desporto e de Lazer | Estádio / Pavilhão | 1,10 |
| IX — Desporto e de Lazer | Cinema / Teatro / Coliseu | 1,20 |
| IX — Desporto e de Lazer | Outros | 1,00 |
| X — Museus ou Galerias de Arte | — | 1,00 |
| XI — Bibliotecas | — | 1,40 |
| XI — Arquivos | — | 1,40 |
| XII — Indústria | Fogos de Artifício | 1,40 |
| XII — Indústria | Máquinas e Aparelhos | 1,20 |
| XII — Indústria | Vernizes e Pintura | 1,40 |
| XII — Indústria | Vestuário | 1,40 |
| XII — Indústria | Artigos de Papelaria | 1,20 |
| XII — Indústria | Resinas Naturais | 1,40 |
| XII — Indústria | Artigos de Cera | 1,40 |
| XII — Indústria | Produtos Farmacêuticos | 1,40 |
| XII — Indústria | Outros | 1,40 |
| XII — Oficinas | Reparação de Veículos | 1,20 |
| XII — Oficinas | Pintura | 1,00 |
| XII — Oficinas | Outros | 1,10 |
| XII — Laboratórios Químicos | — | 1,00 |
| XII — Armazém | — | 1,40 |

---

## 2. CTI — Consequências Totais de Incêndio

O CTI é calculado por **modelo analítico** (não por tabelas de lookup). Avalia as consequências potenciais de um incêndio na compartimentação principal (CI), nas vias horizontais de evacuação (VHE) e nas vias verticais de evacuação (VVE).

### 2.1 Parâmetros de entrada

| Parâmetro | Tipo | Descrição |
|---|---|---|
| Tipo de edifício (UT) | Categórico | Define o coeficiente de crescimento do fogo (t_alpha) |
| Área da compartimentação (m²) | Numérico | Área do CI em planta |
| Pé-direito do CI (m) | Numérico | Altura útil do espaço |
| Efetivo | Numérico | Número de ocupantes |
| N.º de saídas | Numérico | Calculado automaticamente se não fornecido |
| Dispositivos de evacuação | Categórico | Sinalização + Iluminação + Simulacros + Formação / Sinalização + Iluminação / Inexistência |
| Sistema de deteção | Categórico | Sem / Termovelocimétrico / Ótico / Aspiração |
| Sistema de extinção | Categórico | Sem / Com |
| Sistema de controlo de fumo | Categórico | Sem / Com |
| Reação ao fogo — teto/paredes do CI | Categórico | Melhor / Respeita / ≤ 1 Classe / > 1 Classe |
| Reação ao fogo — pavimento do CI | Categórico | Melhor / Respeita / ≤ 1 Classe / > 1 Classe |
| VHE — Comprimento (m) | Numérico | Se existir via horizontal de evacuação |
| VHE — Largura (m) | Numérico | — |
| VHE — Dispositivos | Categórico | Igual à CI |
| VHE — Reação ao fogo | Categórico | Igual à CI |
| VVE — Comprimento (m) | Numérico | Se existir via vertical de evacuação |
| VVE — N.º de pisos abaixo/acima | Numérico | — |
| VVE — Área de claraboia (m²) | Numérico | — |
| VVE — Dispositivos | Categórico | Igual à CI |
| VVE — Reação ao fogo | Categórico | Igual à CI |

### 2.2 Coeficiente de crescimento do fogo (t_alpha)

| Tipo de edifício | t_alpha (s) | Classe de crescimento |
|---|---|---|
| I — Habitação | 300 | Médio |
| II — Estacionamento | 75 | Ultra-rápido |
| III — Administrativos | 300 | Médio |
| IV — Escolas, Creches | 300 | Médio |
| V — Hospitais, Lares | 300 | Médio |
| VI — Salas de Espetáculo | 150 | Rápido |
| VII — Hotéis | 300 | Médio |
| VII — Restauração | 300 | Médio |
| VIII — Comércio | 150 | Rápido |
| IX — Desporto e Lazer | 300 | Médio |
| X — Museus, Galerias | 300 | Médio |
| XI — Bibliotecas / Arquivos | 150 | Rápido |
| XII — Indústria / Armazém | 75 | Ultra-rápido |
| XII — Oficinas | 150 | Rápido |
| XII — Laboratórios Químicos | 75 | Ultra-rápido |

### 2.3 Lógica de cálculo (síntese)

1. **Tempo de deteção (t_det):** calculado em função do sistema de deteção e do t_alpha do edifício.
2. **Volume de fumo disponível (Vf_lim):** `área × (pé-direito − 2)` — volume até à cota de 2 m, considerando extração se houver controlo de fumo.
3. **Tempo de enchimento de fumo (t_lim_f):** integração numérica do caudal de fumo até ao Vf_lim.
4. **Tempo de percurso de evacuação (t_per):** função da área, efetivo e dispositivos de evacuação.
5. **Tempo de atravessamento de vãos (t_av):** função do efetivo e largura das saídas.
6. **Tempo de evacuação total (t_ev):** `t_det + t_per + t_av`.
7. **Avaliação de segurança:** compara t_ev com t_lim_f. Se a evacuação demora mais do que o preenchimento de fumo, aplica penalização.
8. **CPI parcial:** combina os resultados da CI, VHE e VVE com ponderação pela reação ao fogo.
9. **CTI:** combinação dos CPI parciais.

> O CTI não produz uma tabela de valores fixos — o resultado depende das características físicas específicas do edifício.

---

## 3. DPI — Desenvolvimento e Propagação do Incêndio

$$DPI = \frac{\sum_{i}\ DPI_i}{\text{n.º de subfatores com valor} > 0}$$

---

### 3.1 DPI_REIC — Resistência dos Elementos da Compartimentação Corta-Fogo

Avalia a resistência ao fogo dos elementos de compartimentação em função da época de construção e condições de controlo de fumo.  
**Não se aplica → 0,00.**

**Edifícios posteriores a 1990 — VVE conforme:**

| | Valor |
|---|---|
| VVE respeita regulamentação | **1,00** |

**Edifícios posteriores a 1990 — VVE não conforme:**

| Controlo de fumo | Tipo | Resistência: Respeita | Resistência: < 30 min | Resistência: < 60 min |
|---|---|---|---|---|
| Com controlo | Mecânico | 1,05 | 1,15 | 1,25 |
| Com controlo | Natural | 1,10 | 1,20 | 1,30 |
| Sem controlo | — | 1,20 | 1,30 | 1,40 |

**Edifícios anteriores a 1990 — VVE conforme:**

| Controlo de fumo | Tipo | Resistência: Respeita | Resistência: < 30 min | Resistência: < 60 min |
|---|---|---|---|---|
| Com controlo | Mecânico | 1,10 | 1,20 | 1,30 |
| Com controlo | Natural | 1,15 | 1,25 | 1,35 |
| Sem controlo | — | 1,30 | 1,40 | 1,50 |

**Edifícios anteriores a 1990 — VVE não conforme:**

| Controlo de fumo | Tipo | Resistência: Respeita | Resistência: < 30 min | Resistência: < 60 min |
|---|---|---|---|---|
| Com controlo | Mecânico | 1,15 | 1,25 | 1,35 |
| Com controlo | Natural | 1,20 | 1,30 | 1,40 |
| Sem controlo | — | 1,35 | 1,45 | 1,55 |

---

### 3.2 DPI_EI — Estanquidade e Isolamento

Avalia a integridade corta-fogo dos elementos de separação entre compartimentações.  
**Não se aplica → 0,00.**

| Portas corta-fogo | Paredes | Resistência das paredes | Valor |
|---|---|---|---|
| Existem e não são necessárias | Respeita | — | **0,50** |
| Existem e não são necessárias | Não respeita | Metade da resistência | **0,80** |
| Existem e não são necessárias | Não respeita | Nenhuma resistência | **1,10** |
| Respeita regulamentação | Respeita | — | **1,00** |
| Respeita regulamentação | Não respeita | Metade da resistência | **1,10** |
| Respeita regulamentação | Não respeita | Nenhuma resistência | **1,20** |
| Não respeita regulamentação | Respeita | — | **1,20** |
| Não respeita regulamentação | Não respeita | Metade da resistência | **1,30** |
| Não respeita regulamentação | Não respeita | Nenhuma resistência | **1,40** |

---

### 3.3 DPI_VDGF — Vãos, Diedros e Guarda-fogo da Fachada

Avalia o risco de propagação pelo exterior do edifício.  
**Não se aplica → 0,00.**

O resultado é o **máximo** de três sub-valores independentes:

| Sub-valor | Conformidade | Valor |
|---|---|---|
| Afastamento dos vãos | Respeita | 1,00 |
| Afastamento dos vãos | Não respeita | 1,20 |
| Diedros da fachada | Respeita | 1,00 |
| Diedros da fachada | Não respeita | 1,20 |
| Empena / Guarda-fogo | Respeita | 1,00 |
| Empena / Guarda-fogo | Não respeita + materiais Classe A1 | 1,10 |
| Empena / Guarda-fogo | Não respeita + materiais pior que Classe A1 | 1,30 |

> **DPI_VDGF = max(AfastVaos, Diedros, EmpenaGuardaFogo)**

---

### 3.4 DPI_PE — Paredes Exteriores

Avalia o risco de propagação pelo exterior através das paredes da fachada.  
**Não se aplica → 0,00. Reação ao fogo conforme → 1,00.**

Quando a **reação ao fogo não respeita** a regulamentação:

| Classe de reação ao fogo | Tipo de parede exterior | Valor |
|---|---|---|
| Classe < 1 | Tradicional | 1,05 |
| Classe < 1 | ETICS | 1,10 |
| Classe < 1 | Ventilada / Cortina | 1,15 |
| Classe < 2 | Tradicional | 1,10 |
| Classe < 2 | ETICS | 1,20 |
| Classe < 2 | Ventilada / Cortina | 1,30 |
| Classe < 3 | Tradicional | 1,20 |
| Classe < 3 | ETICS | 1,30 |
| Classe < 3 | Ventilada / Cortina | 1,40 |

---

### 3.5 DPI_OGS — Organização e Gestão da Segurança

Avalia a maturidade do sistema de gestão de segurança contra incêndio.  
**Não se aplica → 0,00.**

Os valores apresentados já incluem o **ajuste final** aplicado pelo motor de cálculo:  
− 0,10 se o regulamento interno existe (sem conformidade total); − 0,20 se respeita totalmente.

**Subcaso: Registos e Procedimento de Prevenção**

| Formação do pessoal | Regulamento interno | Valor final |
|---|---|---|
| Sem formação | Existe (não totalmente conforme) | 0,80 |
| Sem formação | Respeita totalmente | 1,10 |
| Sem formação | Não respeita | 1,40 |
| Com formação | Existe (não totalmente conforme) | 0,50 |
| Com formação | Respeita totalmente | 0,80 |
| Com formação | Não respeita | 1,30 |

**Subcaso: Registo e Plano de Prevenção**

| Formação do pessoal | Regulamento interno | Valor final |
|---|---|---|
| Sem formação | Existe (não totalmente conforme) | 0,80 |
| Sem formação | Respeita totalmente | 1,00 |
| Sem formação | Não respeita | 1,30 |
| Com formação | Existe (não totalmente conforme) | 0,60 |
| Com formação | Respeita totalmente | 0,80 |
| Com formação | Não respeita | 1,20 |

**Subcaso: Plano de Segurança e Simulacro**

| Formação do pessoal | Regulamento interno | Valor final |
|---|---|---|
| Sem formação | Existe (não totalmente conforme) | 0,70 |
| Sem formação | Respeita totalmente | 0,80 |
| Sem formação | Não respeita | 1,20 |
| Com formação | Existe (não totalmente conforme) | 0,50 |
| Com formação | Respeita totalmente | 0,60 |
| Com formação | Não respeita | 1,10 |

---

## 4. ESCI — Eficácia de Socorro e Combate ao Incêndio

$$ESCI = \frac{\sum_{i}\ ESCI_i}{\text{n.º de subfatores com valor} > 0}$$

---

### 4.1 ESCI_GP — Guarnição do Posto de Bombeiros

Avalia a eficácia da resposta dos bombeiros em função da distância, tempo de chegada e sistema de deteção e alerta.

**Subcaso A — Trajeto dos Bombeiros ≤ 10 km**

| Tempo de chegada | Não requer deteção | Automático — Aspiração | Automático — Ótico | Automático — Termovelocimétrico | Manual | Ausência de deteção |
|---|---|---|---|---|---|---|
| ≤ 10 min | 1,00 | **0,70** | **0,80** | **0,90** | 1,00 | 1,20 |
| > 10 min e ≤ 20 min | 1,10 | **0,80** | **0,90** | **1,00** | 1,10 | 1,30 |
| > 20 min | 1,20 | **0,90** | **1,00** | **1,10** | 1,20 | 1,40 |

**Subcaso B — Trajeto dos Bombeiros > 10 km**

| Tempo de chegada | Não requer deteção | Automático — Aspiração | Automático — Ótico | Automático — Termovelocimétrico | Manual | Ausência de deteção |
|---|---|---|---|---|---|---|
| ≤ 10 min | 1,10 | **0,80** | **0,90** | **1,00** | 1,10 | 1,30 |
| > 10 min e ≤ 20 min | 1,20 | **0,90** | **1,00** | **1,10** | 1,20 | 1,40 |
| > 20 min | 1,30 | **1,00** | **1,10** | **1,20** | 1,30 | 1,50 |

> Valores a **negrito** correspondem à deteção automática — quanto mais sensível o sistema, menor o valor (melhor).

---

### 4.2 ESCI_SID — Sinalização, Iluminação e Deteção (meios de evacuação)

Avalia os meios de sinalização e deteção nas vias de evacuação.

**Subcaso A — Altura do edifício < 9 m**

| Dispositivos de evacuação | OGS existe? | Caixa de escadas exterior | Caixa de escadas interior |
|---|---|---|---|
| Sinalização + Iluminação + Deteção | Sim | 0,40 | 0,50 |
| Sinalização + Iluminação + Deteção | Não | 0,60 | 0,70 |
| Sinalização + Iluminação | Sim | 0,50 | 0,60 |
| Sinalização + Iluminação | Não | 0,70 | 0,80 |
| Sinalização apenas | Sim | 0,70 | 1,05 |
| Sinalização apenas | Não | 0,85 | 1,20 |
| Inexistência | Sim | 0,80 | 1,10 |
| Inexistência | Não | 1,00 | 1,30 |

**Subcaso B — Altura do edifício > 9 m**

| Dispositivos de evacuação | OGS existe? | Caixa de escadas exterior | Caixa de escadas interior |
|---|---|---|---|
| Sinalização + Iluminação + Deteção | Sim | 0,50 | 0,60 |
| Sinalização + Iluminação + Deteção | Não | 0,70 | 0,80 |
| Sinalização + Iluminação | Sim | 0,60 | 0,70 |
| Sinalização + Iluminação | Não | 0,80 | 0,90 |
| Sinalização apenas | Sim | 0,80 | 1,10 |
| Sinalização apenas | Não | 0,95 | 1,30 |
| Inexistência | Sim | 0,90 | 1,20 |
| Inexistência | Não | 1,10 | 1,40 |

---

### 4.3 ESCI_AE — Acessibilidade ao Edifício

Avalia a facilidade de acesso dos meios de socorro ao edifício.

| Piso mais alto acima do solo | Acesso dos meios de socorro | Valor |
|---|---|---|
| < 3 pisos | Acesso possível | 1,00 |
| < 3 pisos | Apenas VLCI | 1,20 |
| < 3 pisos | Sem acesso | 1,40 |
| > 3 pisos | Acesso possível | 1,05 |
| > 3 pisos | Apenas VLCI | 1,30 |
| > 3 pisos | Sem acesso | 1,50 |
| > 3 pisos (acesso condicionado) | Acesso possível | 1,10 |
| > 3 pisos (acesso condicionado) | Apenas VLCI | 1,40 |
| > 3 pisos (acesso condicionado) | Sem acesso | 1,60 |

> VLCI = Veículo Ligeiro de Combate a Incêndios

---

### 4.4 ESCI_HE — Hidrantes Exteriores

Avalia a disponibilidade de hidrantes exteriores para abastecimento de água.

| Situação | Distância ao hidrante | Valor |
|---|---|---|
| Não se aplica | — | **0,00** |
| Aplica | ≤ 30 m | 1,00 |
| Aplica | > 30 m e ≤ 60 m | 1,10 |
| Aplica | > 60 m | 1,20 |
| Não existe | — | 1,60 |

---

### 4.5 ESCI_EXT — Extintores

Avalia a adequação dos meios de primeira intervenção com extintores portáteis.  
**Não se aplica → 0,00.**

**Subcaso: Com OGS — Plano de Emergência + Simulacro (PE+S)**

| Formação do pessoal | Extintores | Valor |
|---|---|---|
| Sem formação | Existem (sem verificação de conformidade) | 0,80 |
| Sem formação | Respeita totalmente | 1,10 |
| Sem formação | Respeita parcialmente | 1,20 |
| Sem formação | Não respeita | 1,35 |
| Com formação | Existem (sem verificação de conformidade) | 0,70 |
| Com formação | Respeita totalmente | 1,00 |
| Com formação | Respeita parcialmente | 1,15 |
| Com formação | Não respeita | 1,25 |

**Subcaso: Com OGS — Registos + Plano de Prevenção (R+PP)**

| Formação do pessoal | Extintores | Valor |
|---|---|---|
| Sem formação | Existem (sem verificação de conformidade) | 0,90 |
| Sem formação | Respeita totalmente | 1,10 |
| Sem formação | Respeita parcialmente | 1,15 |
| Sem formação | Não respeita | 1,25 |
| Com formação | Existem (sem verificação de conformidade) | 0,80 |
| Com formação | Respeita totalmente | 1,00 |
| Com formação | Respeita parcialmente | 1,05 |
| Com formação | Não respeita | 1,15 |

**Subcaso: Sem OGS — Registos + Plano de Prevenção (R+PP)**

| Formação do pessoal | Extintores | Valor |
|---|---|---|
| Sem formação | Existem (sem verificação de conformidade) | 1,00 |
| Sem formação | Respeita totalmente | 1,10 |
| Sem formação | Respeita parcialmente | 1,20 |
| Sem formação | Não respeita | 1,30 |
| Com formação | Existem (sem verificação de conformidade) | 0,90 |
| Com formação | Respeita totalmente | 1,05 |
| Com formação | Respeita parcialmente | 1,10 |
| Com formação | Não respeita | 1,20 |

---

### 4.6 ESCI_RIA — Rede de Incêndio Armada

Avalia a adequação da rede de incêndio armada (bocas de incêndio).  
**Não se aplica → 0,00.**

**Subcaso: Com OGS — PE+S**

| Formação | Tipo de coluna | Conformidade RIA | Valor |
|---|---|---|---|
| Sem formação | RIA | Existe (sem verificação) | 0,80 |
| Sem formação | RIA | Respeita totalmente | 1,10 |
| Sem formação | RIA | Respeita parcialmente | 1,20 |
| Sem formação | RIA | Não respeita | 1,35 |
| Sem formação | RIA + CS | Existe (sem verificação) | 0,75 |
| Sem formação | RIA + CS | Respeita totalmente | 1,05 |
| Sem formação | RIA + CS | Respeita parcialmente | 1,15 |
| Sem formação | RIA + CS | Não respeita | 1,35 |
| Com formação | RIA | Existe (sem verificação) | 0,70 |
| Com formação | RIA | Respeita totalmente | 1,00 |
| Com formação | RIA | Respeita parcialmente | 1,10 |
| Com formação | RIA | Não respeita | 1,25 |
| Com formação | RIA + CS | Existe (sem verificação) | 0,65 |
| Com formação | RIA + CS | Respeita totalmente | 0,95 |
| Com formação | RIA + CS | Respeita parcialmente | 1,05 |
| Com formação | RIA + CS | Não respeita | 1,25 |

**Subcaso: Com OGS — R+PP**

| Formação | Tipo de coluna | Conformidade RIA | Valor |
|---|---|---|---|
| Sem formação | RIA | Existe (sem verificação) | 0,90 |
| Sem formação | RIA | Respeita totalmente | 1,10 |
| Sem formação | RIA | Respeita parcialmente | 1,15 |
| Sem formação | RIA | Não respeita | 1,25 |
| Sem formação | RIA + CS | Existe (sem verificação) | 0,85 |
| Sem formação | RIA + CS | Respeita totalmente | 1,05 |
| Sem formação | RIA + CS | Respeita parcialmente | 1,10 |
| Sem formação | RIA + CS | Não respeita | 1,25 |
| Com formação | RIA | Existe (sem verificação) | 0,80 |
| Com formação | RIA | Respeita totalmente | 1,00 |
| Com formação | RIA | Respeita parcialmente | 1,05 |
| Com formação | RIA | Não respeita | 1,15 |
| Com formação | RIA + CS | Existe (sem verificação) | 0,75 |
| Com formação | RIA + CS | Respeita totalmente | 0,95 |
| Com formação | RIA + CS | Respeita parcialmente | 1,00 |
| Com formação | RIA + CS | Não respeita | 1,15 |

**Subcaso: Sem OGS — R+PP**

| Formação | Tipo de coluna | Conformidade RIA | Valor |
|---|---|---|---|
| Sem formação | RIA | Existe (sem verificação) | 1,00 |
| Sem formação | RIA | Respeita totalmente | 1,10 |
| Sem formação | RIA | Respeita parcialmente | 1,20 |
| Sem formação | RIA | Não respeita | 1,30 |
| Sem formação | RIA + CS | Existe (sem verificação) | 0,95 |
| Sem formação | RIA + CS | Respeita totalmente | 1,05 |
| Sem formação | RIA + CS | Respeita parcialmente | 1,15 |
| Sem formação | RIA + CS | Não respeita | 1,30 |
| Com formação | RIA | Existe (sem verificação) | 0,90 |
| Com formação | RIA | Respeita totalmente | 1,00 |
| Com formação | RIA | Respeita parcialmente | 1,10 |
| Com formação | RIA | Não respeita | 1,20 |
| Com formação | RIA + CS | Existe (sem verificação) | 0,85 |
| Com formação | RIA + CS | Respeita totalmente | 0,95 |
| Com formação | RIA + CS | Respeita parcialmente | 1,05 |
| Com formação | RIA + CS | Não respeita | 1,20 |

> CS = Coluna Seca; RIA = Rede de Incêndio Armada; OGS = Organização e Gestão da Segurança  
> PE+S = Plano de Emergência + Simulacro; R+PP = Registos + Plano de Prevenção

---

### 4.7 ESCI_CPB — Corpo Privado de Bombeiros

Avalia a existência de corpo privado de bombeiros no edifício ou complexo.

| Aplica? | Situação | Valor |
|---|---|---|
| Não se aplica | — | **0,00** |
| Aplica | Existe e não é exigido | **0,50** |
| Aplica | Existe (exigido por lei) | **1,00** |
| Aplica | Não existe | **1,50** |

---

## 5. Notas finais

- Todos os valores são extraídos do motor de cálculo Python `Chichorro v3.1` (`app/backend/`).
- O motor é a fonte canónica de verdade — em caso de discrepância com este documento, prevalece o código.
- O valor **0,00** de um subfator significa sempre que aquele subfator **não existe ou não é aplicável** ao edifício em análise, sendo excluído da média do módulo.
- Subfatores com valor **< 1,00** são **medidas benéficas** (ex.: sistema de deteção por aspiração, corpo privado de bombeiros existente e não exigido).
