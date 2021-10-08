## Despesa com Pessoal:

**Pasta sintética (Abstrata)**

- Contém interface para lidar com os movimentos como documentos de departamento pessoal genéricos. Para o caso da folha, seria a Ordem de Pagamento, que tem a data de reconhecimento da despesa (Apropriação), e a data de Pagamento (Que hoje está no título). Para casos de obrigações com o governo, representa as GUIAS (GPS, GRRF, ETC)

- Todo lançamento contábil de Departamento Pessoal tem um campo com o ID da Despesa com Pessoal

## Folha de Pagamento (Pai: Despesa com Pessoal)

- Responsável por gerar os lançamentos contábeis da folha de pagamento. Essa pasta sabe qual conta contábil usar para cada rubrica do e-Social. Também registra no diário o Estabelecimento, Tomador e Departamento e Lotação naquele momento.

- Sub-pastas para os tipos de trabalhadores. Estagiários, Contribuintes Individuais e etc.

- Tipos de cálculos contemplados: Folha, Folha Corretiva, Adiantamento de Salário

- **Previsão Folha de Pagamento**

	Quando: Depois do evento 'Apropriação Folha de Pagamento'
	
	Heurística: Média de salários anteriores

- **Previsão Folha de Pagamento (Ajustes)**

	Quando: Depois de Cálculo da Folha (Integração Persona)
	
	Entrada:
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "tipo_de_calculo": "Tipo de Cálculo",
  "trabalhadores" : [{
    "id": "<GUID do Trabalhador>",
    "codigo" : "<Códito do Trabalhador>",
    "nome": "<Nome do Trabalhador>",
    "cpf": "<CPF do Trabalhador>"
    
  }],
  "departamentos" : [{
    "id": "<GUID do departamento>",
    "codigo": "<Código do departamento>",
    "nome": "<Nome do departamento>"
  }],
  "lotacoes" : [{
    "id": "<GUID da lotação>",
    "codigo": "<Código da lotação>",
    "nome": "<Nome da lotação>"
  }],
  "rubricas" : [{
    "id": "<GUID da rubrica>",
    "codigo": "<Código da rubrica>",
    "nome": "<Nome da rubrica>",
    "tipovalor": "<tipovalor da rubrica, ENUM, campo persona.eventos.tipovalor>",
    "categoria": "<Categoria da rubrica, ENUM, campo persona.eventos.categoria>",
    "unidade": "<Unidade da rubrica, ENUM, campo persona.eventos.unidade>"
  }],
  "calculos" : [{
    "id": "<GUID do calculotrabalhador>",
    "data_de_pagamento": "<Data de pagamento preenchida na tela. Campo persona.calculostrabalhadores.datapagamento",
    "valor": "<Valor>",
    "rubrica": "<ID da rubrica. Campo persona.calculostrabalhadores.evento>",
    "lotacao": "<ID da lotacao. Campo persona.calculostrabalhadores.lotacao>",
    "ano": "<Ano do calculo, Campo persona.calculostrabalhadores.ano>",
    "mes": "<Mês do calculo. Campo persona.calculostrabalhadores.mes>",
    "trabalhador": "<ID do Trabalhador>",
    "ano_gerador": "<Ano gerador, essencial em folha corretiva>",
    "mes_gerador": "<Mês gerador, essencial em folha corretiva>",
    "invisivel": "<indicador de calculo invisivel>",
    "tipo_recebimento_trabalhador": "campo persona.calculostrabalhadores.tiporecebimentotrabalhador"
  }],
  "mudancas_trabalhadores":[{
    "data_iinicial": "<Data Inicial da alocacao do trabalhador",
    "data_final": "<Data Final da alocacao do trabalhador>",
    "tipo": "<Tipo de mudanca, ENUM>",
    "estabelecimento": "<Codigo do estabelecimento>",
    "departamento": "<ID do departamento>",
    "lotacao": "<ID da lotacao>",
    "trabalhador": "<ID do trabalhador>"
  }],
  "estabelecimentos":[{
    "id": "<ID do estabelecimento>",
    "codigo": "<Código do estabelecimento>"
  }]
}
```

- **Apropriação Folha de Pagamento**

	Quando: Depois do Fechamento do Período (Integração Persona)
	
	Entrada:
```json
{
"mes" : "<Mês de competência>",
"ano": "<Ano de competência>",
"estabelecimento": "<ID do estabelecimento>"
}
```


## Décimo Terceiro (Pai: Despesa com Pessoal)

- Responsável pelos movimentos de décimo terceiro salário

- Sub-pastas para os tipos de trabalhadores. Estagiários, Contribuintes Individuais e etc.

- Tipos de Cálculo Contemplados: 13º Salário, Complemento de 13º Salário, Adiantamento de 13º Salário

- Responsável pelos lançamentos de Provisão de Décimo terceiro

- **Previsão Provisão de Décimo Terceiro**

	Quando: Depois do Evento 'Previsão Folha de Pagamento'
	
	Heurística: Cálculo de 13º segundo regras de negócio

- **Apropriação Provisão de Décimo Terceiro**

	Quando: Depois do Evento 'Apropriação Folha de Pagamento'

- **Previsão Décimo Terceiro (ajustes)**

	Quando: Depois do cálculo de 13º (Integração Persona)
	
	Entrada: Mesma entrada que o evento 'Previsão Folha de Pagamento (Ajustes)'

- **Previsão de 13º (Lançamento Caixa, referente ao pagamento ao trabalhador)**

	Quando: Depois do evento 'Previsão/Apripriação Provisão de Décimo terceiro'
	
	Heurística: Soma das provisões


## Férias (Pai: Despesa com Pessoal)

- Responsável pelo cálculo de férias do funcionário

- Sub-pastas para os tipos de trabalhadores. Contribuinte Individual, Funcionários e etc.

- Tipos de Cálculo Contemplados: Férias, Complemento de Férias

- Responsável pelos lançamentos de Provisão de 1/3 de Férias

- **Previsão Férias (1/3)**

	Quando: Depois do evento 'Previsão Folha de Pagamento'
	
	Heurística: Cálculo do valor de 1/3 de férias de acordo com regras de negócio

- **Previsão Férias (1/3) (ajustes)**

	Quando: Depois do cálculo de férias (Integração Persona)
	
	Entrada: Mesma entrada que o evento 'Previsão Folha de Pagamento (Ajustes)'

- **Apropriação Férias**

	Quando: Depois do Fechamento do Período (Integração Persona)
	
	Entrada: 
```json
{
"mes" : "<Mês de competência>",
"ano": "<Ano de competência>",
"estabelecimento": "<Codigo do estabelecimento>"
}
```

## Rescisão (Pai: Despesa com Pessoal)

- Responsável pelos lançamentos da rescisão do funcionário

- Responsável pelos lançamentos de apropriação e pagamento da GRRF

- **Previsão Rescisão**

	Quando: Depois de Cálculo de Rescisão (Integração Persona)
	
	Entrada: Mesma entrada que o evento 'Previsão Folha de Pagamento (Ajustes)'

- **Apropriação Rescisão**

	Quando: Depois do fechamento do período
	
	Entrada: 
```json
{
"mes" : "<Mês de competência>",
"ano": "<Ano de competência>",
"estabelecimento": "<Codigo do estabelecimento>"
}
```

- **Apropriação GRRF**

	Quando: Depois de geração da GRRF (Integração Persona)
	
	Entrada:
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "trabalhadores" : [{
    "id": "<GUID do Trabalhador>",
    "codigo" : "<Códito do Trabalhador>",
    "nome": "<Nome do Trabalhador>"
    
  }],
  "departamentos" : [{
    "id": "<GUID do departamento>",
    "codigo": "<Código do departamento>",
    "nome": "<Nome do departamento>"
  }],
  "lotacoes" : [{
    "id": "<GUID da lotação>",
    "codigo": "<Código da lotação>",
    "nome": "<Nome da lotação>"
  }],
  "mudancas_trabalhadores":[{
    "data_iinicial": "<Data Inicial da alocacao do trabalhador",
    "data_final": "<Data Final da alocacao do trabalhador>",
    "tipo": "<Tipo de mudanca, ENUM>",
    "estabelecimento": "<Codigo do estabelecimento>",
    "departamento": "<ID do departamento>",
    "lotacao": "<ID da lotacao>",
    "trabalhador": "<ID do trabalhador>"
  }],
  "sefip": [{
    "id": "<GUID da Sefip>",
    "tipo_sefip": "tipo de sefip"
  }],
  "guias_sefip_trabalhadores":[{
    "id": "<GUID da tabela persona.guiasefiptrabalhadores>",
    "sefip": "<GUID da sefip>",
    "trabalhador": "<GUID do trabalhador>",
    "valor": "<Valor numérico do campo persona.guiasefiptrabalhadores.valor>"
  }],
  "grrf_trabalhadores":[{
    "id": "<GUID da tabela persona.grrftrabalhadores>",
    "valor_fgts": "<Valor numérico do campo persona.grrftrabalhadores.valorfgts>",
    "multa_fgts": "<Valor numérico do campo persona.grrftrabalhadores.multafgts>",
    "multa_fgts_csoc": "<Valor numérico do campo persona.grrftrabalhadores.multafgtscsoc>"
  }],
  "estabelecimentos":[{
    "id": "<ID do estabelecimento>",
    "codigo": "<Código do estabelecimento>"
  }]
}
```

## Cálculo Sindical (Pai: Despesa com Pessoal)

- Responsável por fazer os lançamentos do dissídio sindical

-  Responsável por fazer os lançamentos da GRCS

- **Apropriação Dissídio**

	Quando: Fechamento do período (Integração Persona)
	
	Entrada: Mesma que o evento 'Previsão Folha de pagamento (Ajustes)'

- **Apropriação GRCS**

	Quando: Geração da GRCS (Integração Persona)
	
	Entrada: 
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "valor": "<Valor do documento>",
  "vencimento": "<Vencimento do documento>",
  "data_criacao": "<Data de criação do documento>",
  "estabelecimento": "<Código do estabelecimento>"
}
```

## Eventos Trabalhistas

**Pasta Sintética e abstrata**

- Contém uma coleção de eventos (Alguns hoje são apenas rubricas) que fazem parte de mais de um momento do departamento pessoal, e portanto merecem um destaque maior do que eventos mais simples

## INSS (Pai: Impostos, Pai: Evento Trabalhista)

- Contém a inteligência de lançamentos para INSS Funcionário e INSS Patronal (Declarada na GPS. Não se chama GPS porque a GPS é apenas a GUIA, enquanto a movimentação contábil real é o pagamento de INSS).

- Invocado pelas pastas de Despesa com Pessoal para ajudar a fazer os lançamentos contábeis.

- **Previsão GPS:**

	Quando: Depois de Apropriação GPS
	
	Heurística: Previsão baseada no histórico dos últimos meses

- **Apropriação GPS**

	Quando: Depois do fechamento do período (Integração Persona)
	
	Entrada:
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "trabalhadores" : [{
    "id": "<GUID do Trabalhador>",
    "codigo" : "<Códito do Trabalhador>",
    "nome": "<Nome do Trabalhador>"
    
  }],
  "departamentos" : [{
    "id": "<GUID do departamento>",
    "codigo": "<Código do departamento>",
    "nome": "<Nome do departamento>"
  }],
  "lotacoes" : [{
    "id": "<GUID da lotação>",
    "codigo": "<Código da lotação>",
    "nome": "<Nome da lotação>"
  }],
  "mudancas_trabalhadores":[{
    "data_iinicial": "<Data Inicial da alocacao do trabalhador",
    "data_final": "<Data Final da alocacao do trabalhador>",
    "tipo": "<Tipo de mudanca, ENUM>",
    "estabelecimento": "<Codigo do estabelecimento>",
    "departamento": "<ID do departamento>",
    "lotacao": "<ID da lotacao>",
    "trabalhador": "<ID do trabalhador>"
  }],
  "gps_empresa": [{
    "id": "<GUID da tabela persona.guiaprevidenciasocialempresa>",
    "ano": "<Ano de competência da GPS>",
    "mes": "<Mês de competência da GPS>",
    "estabelecimento": "<Estabelecimento>",
    "cooperativas": "<Valor referente a cooperativas>",
    "compensacao_limitada": "<Valor referente a compensação limitada>",
    "compensacao_ilimitada": "<Valor referente a compensação ilimitada>",
    "valor_deducao_inss_retido": "<Valor referente ao valor de redução de INSS Retido>",
    "reembolso_no_mes": "<Valor refenre ao reembolso>"
  }],
  "gps_empresa_trabalhador":[{
    "id": "<GUID da tabela persona.guiaprevidenciasocialempresatrabalhadores>",
    "gps_empresa": "<GUID da gps_empresa relacionada>",
    "trabalhador": "<GUID do trabalhador>",
    "valor_total": "<valor numérico de compõe a GPS. campo valortotal da tabela>",
    "valor_inss": "<valor numérico de compõe a GPS. campo valorinss da tabela>",
    "valor_deducao_salario_maternidade_folha": "<valor numérico de compõe a GPS. campo valordeducaosalariomaternidadefolha da tabela>",
    "sat_empresa": "<valor numérico de compõe a GPS. campo satempresa da tabela>",
    "sat_agente_nocivo2": "<valor numérico de compõe a GPS. campo satagentenocivo2 da tabela>",
    "sat_agente_nocivo3": "<valor numérico de compõe a GPS. campo satagentenocivo3 da tabela>",
    "sat_agente_nocivo4": "<valor numérico de compõe a GPS. campo satagentenocivo4 da tabela>",
    "contribuicao_terceiros": "<valor numérico de compõe a GPS. campo contribuicaoterceiros da tabela>",
    "contribuicao_sobre_trabalhador": "<valor numérico de compõe a GPS. campo contribuicaosobretrabalhador da tabela>",
    "valor_deducao_salario_familia": "<valor numérico de compõe a GPS. campo valordeducaosalariofamilia da tabela>",
    "valor_deducao_salario_maternidade_13": "<valor numérico de compõe a GPS. campo valordeducaosalariomaternidade13 da tabela>"    
  }],
  "estabelecimentos":[{
    "id": "<ID do estabelecimento>",
    "codigo": "<Código do estabelecimento>"
  }]
}
```


## FGTS (Pai: Evento Trabalhista)

- Contém a inteligência de lançamentos de FGTS.

- **Previsão SEFIP (Lançamento Caixa):**

	Quando: Depois de Apropriação SEFIP
	
	Heurística: Previsão baseada no histórico dos últimos meses

- **Previsão SEFIP  (Lançamento Caixa) (Ajustes)**

	Quando: Depois de geração da guia (Integração Persona)
	
	Entrada:
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "trabalhadores" : [{
    "id": "<GUID do Trabalhador>",
    "codigo" : "<Códito do Trabalhador>",
    "nome": "<Nome do Trabalhador>"
    
  }],
  "departamentos" : [{
    "id": "<GUID do departamento>",
    "codigo": "<Código do departamento>",
    "nome": "<Nome do departamento>"
  }],
  "lotacoes" : [{
    "id": "<GUID da lotação>",
    "codigo": "<Código da lotação>",
    "nome": "<Nome da lotação>"
  }],
  "mudancas_trabalhadores":[{
    "data_iinicial": "<Data Inicial da alocacao do trabalhador",
    "data_final": "<Data Final da alocacao do trabalhador>",
    "tipo": "<Tipo de mudanca, ENUM>",
    "estabelecimento": "<Codigo do estabelecimento>",
    "departamento": "<ID do departamento>",
    "lotacao": "<ID da lotacao>",
    "trabalhador": "<ID do trabalhador>"
  }],
  "sefip": [{
    "id": "<GUID da Sefip>",
    "tipo_sefip": "tipo de sefip"
  }],
  "guias_sefip_trabalhadores":[{
    "id": "<GUID da tabela persona.guiasefiptrabalhadores>",
    "sefip": "<GUID da sefip>",
    "trabalhador": "<GUID do trabalhador>",
    "valor": "<Valor numérico do campo persona.guiasefiptrabalhadores.valor>"
  }],
  "estabelecimentos":[{
    "id": "<ID do estabelecimento>",
    "codigo": "<Código do estabelecimento>"
  }]
  
}
```

Obs: A Apropriação do lançamento caixa é feita no pagamento da SEFIP

## Imposto de Renda (Pai: Impostos, Pai: Evento Trabalhista)

- Contém a inteligência de lançamentos do IRPF retido pela empresa

- Invocado pelas pastas de Despesa com Pessoal para ajudar a fazer os lançamentos contábeis.

- Invocado pela geração e pagamento das DARFs de Imposto de Renda (Integração Persona)


- **Previsão DARF IRPF (Lançamento Caixa):**

	Quando: Depois de Apropriação DARF IRPF
	
	Heurística: Previsão baseada no histórico dos últimos meses

- **Previsão DARF IRPF  (Lançamento Caixa) (Ajustes)**

	Quando: Depois de geração da guia (Integração Persona)
	
	Entrada:
```json
{
  "ano": "<Ano de competência>",
  "mes": "<Mês de competência>",
  "valor": "<Valor do documento>",
  "vencimento": "<Vencimento do documento>",
  "data_criacao": "<Data de criação do documento>",
  "trabalhador" : {
    "id": "<GUID do Trabalhador>",
    "codigo" : "<Códito do Trabalhador>",
    "nome": "<Nome do Trabalhador>"
  },
  "departamentos" : [{
    "id": "<GUID do departamento>",
    "codigo": "<Código do departamento>",
    "nome": "<Nome do departamento>"
  }],
  "lotacoes" : [{
    "id": "<GUID da lotação>",
    "codigo": "<Código da lotação>",
    "nome": "<Nome da lotação>"
  }],
  "mudancas_trabalhadores":[{
    "data_iinicial": "<Data Inicial da alocacao do trabalhador",
    "data_final": "<Data Final da alocacao do trabalhador>",
    "tipo": "<Tipo de mudanca, ENUM>",
    "estabelecimento": "<Codigo do estabelecimento>",
    "departamento": "<ID do departamento>",
    "lotacao": "<ID da lotacao>",
    "trabalhador": "<ID do trabalhador>"
  }],
  "estabelecimentos":[{
    "id": "<ID do estabelecimento>",
    "codigo": "<Código do estabelecimento>"
  }]
}
```

## Orientações gerais.

- Quando um valor cheio (Eg. Valor de uma GPS) for rateado por uma dimensão (Eg. Funcionário) e houver arredondamento a ser realizado, será escriturado em um lançamento a mais, com um funcionário fictício de Arredondamento. Para o caso de Cenários Orçamentários, não serão realizados ajustes de arredondamento.

- Os movimentos de Departamento Pessoal estão entre os poucos movimentos contábeis onde realmente há conta contábil para provisão. Sendo assim, as pastas contábeis de 13º e de Férias serão responsáveis por manter a provisão em estado Realizado de meses passados, a provisão em estado Previsto de meses futuro, assim como o lançamento de Pagamento da obrigação na data estimada para o pagamento, em estado Previsto

# Rubricas E-Social

Segue abaixo a listagem de naturezas de rubricas do e-social, e sua respectiva conta contábil

| Rubrica  | Conta Contábil (Despesa) | Conta Contábil (Passivo) |
| ------------ | ------------ | ------------ |
| 1000 - Salário, vencimento, soldo ou subsídio.  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1002 - Descanso semanal remunerado - DSR   |4.1.1.01.0006 DESCANSO SEMANAL REMUNERADO (DSR)  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1003 - Horas extraordinárias   | 4.1.1.01.0012 HORAS EXTRAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1004 - Horas extraordinárias – Indenização de banco de horas | 4.1.1.01.0012 HORAS EXTRAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1005 - Direito de arena  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1007 - Luvas e premiações  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1009 -  Salário-família – complemento  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1010 - Salário in natura - pagos em bens ou serviços  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1011 - Sobreaviso  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1020 - Férias – gozadas  | 4.1.1.01.0009 FÉRIAS C/ ABONO  |2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 1021 - Férias - abono ou gratificação de férias superior a 20 dias   | 4.1.1.01.0009 FÉRIAS C/ ABONO  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 1022 - Férias - abono ou gratificação de férias não excedente a 20 dias   | 4.1.1.01.0009 FÉRIAS C/ ABONO  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 1023 - Férias - abono pecuniário   |  4.1.1.01.0009 FÉRIAS C/ ABONO | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
|  1024 - Férias - o dobro na vigência do contrato | 4.1.1.01.0009 FÉRIAS C/ ABONO  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 1040 - Licença-prêmio   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1041 - Licença-prêmio indenizada  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1099 - Outras verbas salariais   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1201 - Adicional de função / cargo confiança  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1202 - Adicional de insalubridade  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1203 - Adicional de periculosidade  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1204 - Adicional de transferência   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1205 - Adicional noturno  |  4.1.1.01.0001 ADICIONAL NOTURNO  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1206 - Adicional por tempo de serviço  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1207 - Comissões, porcentagens, produção   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1208 - Gueltas  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1209 - Gorjetas  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1210 - Gratificação por acordo ou convenção coletiva | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1211 - Gratificações  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1213 - Quebra de caixa  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1215 - Adicional de Unidocência  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1230 - Remuneração do dirigente sindical  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1299 - Outros Adicionais  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1300 - PLR – Participação em Lucros ou Resultados   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1350 - Bolsa de estudo - estagiário  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1351 - Bolsa de estudo – médico residente |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1352 - Bolsa de estudo ou pesquisa  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1401 - Abono | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1402 - Abono PIS / PASEP  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1403 - Abono legal | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1404 - Auxílio babá  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1405 - Assistência médica  |  4.1.1.01.0003 ASSISTÊNCIA MÉDICA E SOCIAL | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1406 - Auxílio-creche  |  4.1.1.01.0003 ASSISTÊNCIA MÉDICA E SOCIAL | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1407 - Auxílio-educação | 4.1.1.01.0003 ASSISTÊNCIA MÉDICA E SOCIAL  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1409 - Salário-família  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1410 - Auxílio – Locais de difícil acesso  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1601 - Ajuda de custo - aeronauta  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1602 - Ajuda de custo de transferência  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1620 - Ressarcimento de despesas pelo uso de veículo do empregado  | 4.1.1.02 DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1621 - Ressarcimento de despesas de viagem, exceto despesas com veículos |  4.1.1.02 DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1629 - Ressarcimento de outras despesas |  4.1.1.02 DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1651 - Diárias de viagem – até 50% do salário  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1652 - Diárias de viagem – acima de 50% do salário  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1801 - Alimentação  | 4.1.1.01.0014 PROGRAMA DE ALIMENTAÇÃO DO TRABALHADOR - PAT  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 1802 - Etapas (marítimos)  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1805 - Moradia |  4.1.1.02 DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  1810 - Transporte | 4.1.1.01.0017 VALE TRANSPORTE - VT  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  2501 - Prêmios |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  2510 - Direitos autorais e intelectuais |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 2901 - Empréstimos  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  2902 - Vestuário e equipamentos  | 4.1.1.01.0016 UNIFORMES  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 2920 - Reembolsos diversos  | 4.1.1.02 DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 2930 - Insuficiência de saldo   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  3501 - Prestação de serviços | 4.1.1.03 DESPESAS C/ PRESTAÇÃO DE SERVIÇOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  3505 - Retiradas (prólabore) de diretores empregados |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  3506 - Retiradas (pró-labore) de diretores não empregados  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 3508 - Retiradas (prólabore) de proprietários ou sócios  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  3509 - Honorários a conselheiros  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 3520  - Remuneração de cooperado | 4.1.1.01.0015 SALÁRIOS E ORDENADOS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  4010 - Complementação salarial de auxíliodoença  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  4050 - Salário maternidade | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  4051 - Salário maternidade – 13° salário  |  4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS) | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 5001 - 13º salário   |  4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
|  5005 - 13° salário complementar  |  4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 5501 -  Adiantamento de salário  |   4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 5504 - 13º salário - 1ª parcela  | 4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
|  5510 - Adiantamento de benefícios previdenciários  |  4.1.1.01.0013 INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS  | 2.1.2.01.0001 INSS À RECOLHER |
| 6000 - Saldo de salários na rescisão contratual |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 RESCISÕES À PAGAR |
|  6001 - 13º salário relativo ao aviso-prévio indenizado  | 4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
| 6002 - 13° salário proporcional na  rescisão |  4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS) | 2.1.2.03.0003 RESCISÕES À PAGARR |
| 6003 - Indenização compensatória do aviso-prévio   |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  6004 - Férias - o dobro na rescisão  |   4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS   | 2.1.2.03.0003 RESCISÕES À PAGAR |
|  6006 - Férias proporcionais | 4.1.1.01.0009 FÉRIAS C/ ABONO   |  2.1.2.03.0002 FÉRIAS À PAGAR |
|   6007 - Férias vencidas na rescisão | 4.1.1.01.0009 FÉRIAS C/ ABONO  | 2.1.2.03.0003 RESCISÕES À PAGAR |
|6101 - Indenização compensatória - multa rescisória 20 ou 40% (CF/88)    |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 RESCISÕES À PAGAR |
|  6102 - Indenização do art. 9º lei nº 7.238/84  |4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  6103 - Indenização do art. 14 da lei nº 5.889, de 8 de junho de 1973  | 4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  6104 - Indenização do art. 479 da CLT |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 6105 - Indenização recebida a título de incentivo a demissão.  |   4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  6106 - Multa do art. 477 da CLT. |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 6107 - Indenização por quebra de estabilidade  |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 6129 - Outras Indenizações  |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  6901 - Desconto do avisoprévio  |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 RESCISÕES À PAGAR |
|  6904 Multa prevista no art. 480 da CLT |  4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 7001 - Proventos   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9200 - Desconto de Adiantamentos |   4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9201 - Contribuição Previdenciária  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.01.0001 INSS À RECOLHER |
|  9203 Imposto de renda retido na fonte  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.02.0003 IMPOSTO DE RENDA RETIDO NA FONTE À RECOLHER |
| 9208 - Atrasos   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9209 - Faltas  |   4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9210 - DSR s/faltas e atrasos   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9211 - Faltas e atrasos - estagiários   |   4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9213 - Pensão alimentícia  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|   9214 - 13° salário – desconto da primeira parcela| 4.1.1.01.0011 GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)  | 2.1.2.03.0001 13.º SALÁRIOS À PAGAR |
|  9216 - Desconto de valetransporte  | 4.1.1.01.0017 VALE TRANSPORTE - VT   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|   9217 - Contribuição a Outras Entidades e Fundos  |   4.1.1.01.0015 SALÁRIOS E ORDENADOS    | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|   9218 - Retenções judiciais |   4.1.1.01.0015 SALÁRIOS E ORDENADOS    | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|   9219 - Desconto de assistência médica ou odontológica  | 4.1.1.01.0003 ASSISTÊNCIA MÉDICA E SOCIAL  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9220 - Alimentação – desconto   | 4.1.1.01.0014 PROGRAMA DE ALIMENTAÇÃO DO TRABALHADOR - PAT  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9221 - Desconto de férias |  4.1.1.01.0009 FÉRIAS C/ ABONO  | 2.1.2.03.0002 FÉRIAS À PAGAR |
| 9222 - Desconto de outros impostos e contribuições   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9226 - Desconto de férias - abono   |  4.1.1.01.0009 FÉRIAS C/ ABONO | 2.1.2.03.0002 FÉRIAS À PAGAR |
|  9230 - Contribuição Sindical - Compulsória  |   4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.02.0002 CONTRIBUIÇÃO SINDICAL À RECOLHER |
| 9231 - Contribuição Sindical - Associativa   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.02.0002 CONTRIBUIÇÃO SINDICAL À RECOLHER |
| 9232 - Contribuição Sindical - Assistencial   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS   | 2.1.2.02.0002 CONTRIBUIÇÃO SINDICAL À RECOLHER |
| 9233 - Contribuição sindical - Confederativa   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.02.0002 CONTRIBUIÇÃO SINDICAL À RECOLHER |
|  9250 - Seguro de vida - desconto  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9254 - Empréstimos consignados - desconto   |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9255 - Empréstimos do empregador - desconto  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9258 - Convênios  |   4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9260 - Fies – desconto  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9270 - Danos e prejuízos causados pelo trabalhador   | 4.1.1.01.0005 AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9290 - Desconto de pagamento indevido em meses anteriores  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9299 - Outros descontos  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9901 - Base de cálculo da contribuição previdenciária   |   |
|  9902 - Total da base de cálculo do FGTS  |   |
| 9903 - Total da base de cálculo do IRRF   |   |
| 9904 - Total da base de cálculo do FGTS rescisório   |   |
| 9905 - Serviço militar  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9906 - Remuneração no exterior   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9908 - FGTS - depósito  |  4.1.1.01.0010 FUNDO DE GARANTIA DO TEMPO DE SERVIÇO - FGTS  | 2.1.2.01.0002 FGTS À RECOLHER |
|  9910 - Seguros  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|9911 - Assistência Médica   | 4.1.1.01.0003 ASSISTÊNCIA MÉDICA E SOCIAL  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9930 - Salário maternidade pago pela Previdência Social  | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9931 - 13° salário maternidade pago pela Previdência Social   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  |2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9932 - Auxílio-doença acidentário   |   4.1.1.01.0015 SALÁRIOS E ORDENADOS|2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9933 - Auxílio-doença   | 4.1.1.01.0015 SALÁRIOS E ORDENADOS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|9938 - Isenção IRRF - 65 anos    | 4.1.1.01.0015 SALÁRIOS E ORDENADOS  | 2.1.2.02.0003 IMPOSTO DE RENDA RETIDO NA FONTE À RECOLHER |
|  9939 - Outros valores tributáveis  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
| 9950 - Horas extraordinárias - Banco de horas   |4.1.1.01.0012 HORAS EXTRAS   | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9951 - Horas compensadas - Banco de horas  |  4.1.1.01.0012 HORAS EXTRAS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |
|  9989 - Outros valores informativos  |  4.1.1.01.0015 SALÁRIOS E ORDENADOS | 2.1.2.03.0003 SALÁRIOS E ORDENADOS À PAGAR |


