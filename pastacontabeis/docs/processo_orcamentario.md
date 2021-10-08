# Gestão Orçamentária

## Objetivo

Cumprimento do Planejamento Estratégico da empresa, no que se refere a dinâmica dos recursos financeiros.

## Metas

* Planejamento Orçamentário
* Acompanhamento de Resultados
* Revisão Orçamentária

## Requisitos Funcionais

Seguem os requisitos funcionais por ator:

### Equipe de Planejamento

1. Definir um conjunto de premissas orçamentárias internas e externas, tal que se possa determinar variáveis balizadoras das estimativas do cálculo orçamentário. Exemplos:
   1. Premissas internas:
      1. Meta de vendas (qtd/ano)
      2. Capacidade de produção
      3. Número de funcionários (mínimo e máximo)
      4. etc
   2. Premissas externas:
      1. Preço matéria prima (mínimo e máximo)
      2. Inflação anual
      3. Taxa de juros para aplicações financeiras (mínimo e máximo)
      4. etc
2. Escolher bases orçamentárias, isto é, um conjunto de artefatos a serem orçados, por centro de resultados, de modo que se possa tornar o mais objetivo possível o processo orçamentário, para cada responsável dos centros de resultado. Exemplo:
   1. Conjunto de produtos a vender (sendo a estimativa restrita ao preenchimento das quantidades).
   2. Relação de funcionários
   3. etc
3. Consolidar automaticamente os orçamentos de cada centro de resultados, tal que seja possível visualizar o resultado global da empresa por meio de um processo de orçamentário colaborativo.
4. Gerar automaticamente cenários alternativos (otimista, pessimista e médio), cujos resultados seja de acordo com os valores máximos e mínimos determinados para as premissas orçamentárias. De modo que seja possível avaliar, com facilidade, as variações consideradas plausíveis segundo as estimativas.
5. Conduzir análise **Planejado X Histórico**, tal que se possa avaliar a qualidade do planejamento orçamentário, frente ao histórico financeiro da empresa.
   * A análise deve ser realizada comparativamente aos dados do exercício anterior (comparando o mes X do ano Y, ao mês X do ano Y-1).
   * A análise deve permitir evidenciar os desvios absolutos e/ou em percentual.
6. Conduzir análise **Realizado X Histórico**, tal que se possa obter métricas de crescimento e decrescimento do último ano, úteis enquanto insumo para o novo planejamento.
   * A análise deve ser realizada comparativamente aos dados do exercício anterior (comparando o mes X do ano Y, ao mês X do ano Y-1).
   * A análise deve permitir evidenciar os desvios absolutos e/ou em percentual.

### Gestor de Centro de Resultados

1. Preencher e revisar as estimativas orçamentárias, de acordo com as bases orçamentárias anteriormente definidas, de modo que cada responsável possa se concentrar nos parâmetros que lhe cabem.
   * Esta etapa deve contar com a possibilidade de preechimento automático das estimativas, de acordo com as informações de histórico.
2. Cadastrar simulações orçamentárias livremente, tal que se possa gerar situações hipotéticas que se utilizem de qualquer das bases orçamentárias cabíveis (ao gestor em questão), sem compromimsso com qualquer tipo de parâmetro histórico.
3. Adicionar simulações orçamentárias, nos cenários orçamentários disponíveis, de modo que seja possível avaliar o impacto local e global das simulações desejadas.

### Controladoria

1. Conduzir análise **Planejado X Realizado**, tal que se possa verificar regularmente se o planejamento está sendo cumprido.
   * A análise deve ser realizada mês a mês (comparando os valores orçados e realizados dentre de um mesmo mês).
   * A análise deve permitir evidenciar os desvios absolutos e/ou em percentual.
2. Conduzir análise **Realizado X Histórico**, tal que se possa verificar se a empresa vem de fato melhorando seus resultados e crescendo anualmente.
   * A análise deve ser realizada comparativamente aos dados do exercício anterior (comparando o mes X do ano Y, ao mês X do ano Y-1).
   * A análise deve permitir evidenciar os desvios absolutos e/ou em percentual.
3. Realizar ajustes pontuais em orçamentos aprovados, de modo que se possa alterar o orçamento de um mês, sem impactar os demais.
4. Realizar ajustes por redistribuição de valores, em orçamentos aprovados, de modo que se possa alterar o orçamento de um mês, rateando os desvios pelos meses subsequentes, ou mesmo movendo os ajustes para meses futuros escolhidos.

## Arquitetura da Solução

### Principais Entidades

#### Simulação Orçamentária

Conjunto de pastas contábeis estimadas para avaliar os impactos financeiros de uma ação gerencial.

#### Cenário Orçamentário

Conjunto de simulações orçamentárias, utilizado como agrupador final dos fatos contábeis a serem analisados.

Resumidamente, a emissão de relatórios (como DRE, etc) se fará para os dados realizados, ou para um cenário orçamentário. A ideia é que é necessário conhecer todos os valores cobertos por um cenário para o cálculo de impostos calculados por faixas.

#### Parâmetros Orçamentários

Cadastro das variáveis disponíveis para as estimativas de uma simulação orçamentária.

Estas variáveis devem permitir a definição de valor mínimo e máximo, de modo que seja possível gerar cenários otimistas, pessimistas e médios.

#### Bases Orçamentárias

Conjunto de pastas contábeis e respectivos parâmetros, escolhidos como relevantes para as simulações orçamentárias, e segmentados por centro de resultado. De modo que cada gestor de centro de resultado, possa se focar na estimativa dos dados relevantes para sua atividade em particular.

### Dinâmica Orçamentária

Uma vez expostos os requisitos básicos, bem como as principais entidades imaginadas para a solução, importa agora definir o modo pelo qual os fatos em si serão calculados e persisitdos no banco de dados:

#### Lançamentos no Diário

##### Pressupostos

* Possibilidade da comparação planejado X realizado, ou planejado X histórico, a qualquer tempo.
* Coexistência de diversos cenários orçamentários para um mesmo período.
* Independência entre fatos realizados e fatos simulados (isto é, a alteração dos valores, inclusão, ou até remoção de lançamentos, na realização de um fato, não pode alterar os valores orçados).
* Consolidação automática de um cenário orçamentário de tendência.
* Possibilidade de reajustes pontuais para um cenário qualquer (exemplo: reajuste de orçamento num mês do ano, sem comprometer os demais, ou "espalhando" ajustes pelos meses futuros).
* Equivalência entre os fatos orçados e os fatos realizados, isto é, a gravação dos orçamentos no diário deve ser equivalente ao que ocorre para os fatos reais, de modo que todos os relatórios capazes de sumarizar dados reais, sejam reaproveitados para as situações hipotéticas.

##### Modo de Persistência

Tendo em vista os pressupostos anteriores, sugere-se que a gravação dos dados orçados seja realizada de modo equivalente a gravação dos dados realizados, havendo apenas a distinção do preenchimento de informações para identificação da simulação correspondente (adição da coluna "simulacao" no diário unico).

#### Cálculo dos Valores

Conforme exposto, o calculo dos valores simulados será realizado por meio da estimativa de patrâmetros para cada pasta contábil que se deseje considerar.

Assim, idealmente, o processo orçamentário será similar a um cadastro simulado de diversas entidades reais de negócio (contratos de prestaçao de serviço, contratos CLT, etc).

Portanto, o calculo de um orçamento será exatamente igual a cálculo real, sendo que gerando dados marcados como orçados.

#### Aprovação de Cenário Orçamentário

Uma vez que a parametrização de um cenário orçamentário será muito similar ao cadastro dos fatos reais, pode-se considerar a aprovação de um cenário culmine num processo de complementação dos cadastro, gerando por fim cadastros de compromissos reais, os quais passarão a ser considerados no processo normal de previsão.

## Exemplos:

### [Exemplos de lançamentos no Diário Unico com gestão orçamentária](https://docs.google.com/spreadsheets/d/1O4uh3swpljgGUCsxX5iuy6zGMERPSVZKN6bWm0osKDQ/edit?usp=sharing)
