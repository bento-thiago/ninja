# Escrituração de impostos no Diário Unico

### Objetivos

- Usar o Diário Unico como principal insumo para o cálculo fiscal.

- Obter resultado fiscal parcial do período a qualquer momento.

- Obter resultado fiscal projetado para o período, baseado em compromissos que já foram assumidos (orçamento de continuidade).

- Obter resultado fiscal projetado para o período considerando projetos e planos da empresa que ainda não foram concretizados (cenários orçamentários).

- A apuração de cada imposto deverá ser feita pela pasta contábil específica desse imposto.

### Caso Bap/Estasa:

#### Integração com o Persona

A Bap e a Estasa já estão com o Persona funcionando em produção. Sendo assim, já possuem uma solução para seus impostos sobre Folha.

Haverá um módulo de integração para sincronizar o diário unico com os dados gerados pelo Persona. Todos os movimentos financeiros gerados pelo persona serão sincronizados, e não apenas a parte tributária.

#### Demais impostos

Impostos __retidos__ sobre notas de serviço serão atendidos pelas pastas contábeis. São eles:
* PIS
* Cofins
* CSLL
* ISS

Impostos retidos em RPA (Recibo de Pagamento a Autônomo), apesar de serem sobre serviços, são atendidos pelo Persona e também serão recebidos por meio da integração.

### A natureza periódica das regras fiscais

Nosso módulo fiscal deverá refletir nossa legislação fiscal.

Como todas as legislações, nossa legislação fiscal é um "estatuto vivo", em constantes mudanças. Assim, as configurações da empresa, estabelecimento, produtos, itens, participante e etc, deverão ser salvos com referência de data inicial e data final de vigência.

Além disso, as próprias pastas contábeis devem ser capazes de apurar os impostos de acordo com a legislação da data da operação.

### Lançamentos de guias de impostos
Haverá guias de impostos escrituradas no Diário Unico.

Uma guia de imposto é um documento (Header) que agrega os lançamentos no Diário Unico.

Esses lançamentos poderão estar em 4 estados.
- Orçado: Lançamentos feitos baseados em cenários orçamentários.
- Previsto: Lançamentos feitos baseados em documentos previstos pelo orçamento continuidade.
- Realizados: Lançamentos feitos baseados em movimentações financeiras já concretizada, contudo de guias ainda não pagas.
- Quitado: Lançamentos feitos baseados no momento de pagamento das guias.

Cada lançamento da Guia estará vinculado também ao documento original, indo ao detalhe de estar vinculado ao ítem de documento.Isso será feito por uma nova coluna do Diário Unico, em auto-referencia, apontando para uma linha do Diário Unico do documento original (Eg. Uma partida da nota tributada). Esses lançamentos serão criados pelo Segundo Movimento, a ser explicado abaixo.

### Abordagem de dois movimentos.
Sempre que que houver a apropiação de um documento tributável (ex. NFE) haverá dois movimentos no Diário Unico. 

O **Primeiro Movimento** será a apropriação do documento e será realizado pela própria pasta contábil do documento. Depois de realizado o Primeiro Movimento as pastas contáveis referentes aos impostos cabíveis nessa operação serão acionadas para realizarem o Segundo Movimento.

O **Segundo Movimento** será lançamentos nas guias de impostos. Normalmente serão 4 partidas. Sendo 2 partidas em situação Realizado referentes a provisão de pagamento do imposto, e 2 partidas em situação Previsto referentes ao pagamento em sí.

### Guardando fielmente os termos do compromisso (Nova coluna no Diário)
Há casos em que o imposto apurado é diferente dos impostos declarados no momento compromisso (Eg. xml da nota).

Contudo é importante que tenhamos no Diário Unico os impostos destacados na nota. Porque caso haja alguma mudança tributária na empresa será necessário recalcular os lançamentos do segundo movimento. Por isso, o Diário Unico terá novas colunas para armazenar o imposto descrito no xml. Por exemplo: para cada linha que compõe a guia de ICMS, além dos campos tradicionais de um lançamento contábil, terá uma coluna contendo o valor de ICMS a recolher destacado no XML. Essa coluna será usada de insumo para cálculos quando necessários.  

### Impostos que incidem sobre Compras/Vendas
Para cada operação de compra ou venda há uma nota fiscal. A nota fiscal possui informações sobre os impostos agregados. (Exemplo: ICMS). 

Essas informações fiscais são imutáveis pois estão escrituradas na nota fiscal e são portanto conhecidas pelos orgãos públicos competentes (Exemplo: SEFAZ).

Seguindo a abordagem de dois movimentos:
- No Primeiro Movimento seriam feitos lançamentos para a nota fiscal ignorando a tributação
  

- No Segundo Movimento seriam feitos lançamentos vinculados a guia de imposto (Exemplo: Guia de ICMS). 
    - Esses lançamentos teriam também, em outra coluna, a informação de cada imposto disposta no XML original.  
    - Esses lançamentos teriam referencia tanto ao Header da guia, quanto à nota de venda/compra.

Alguns dos impostos sobre compra/venda são: ICMS, IPI, PIS, COFINS, CSLL, INSS e ISS.

### Diferenças entre os impostos destacados e o imposto real

Embora seja incomum, pode acontecer de uma nota fiscal ter informações tributárias destacadas diferentes do que será de fato pago na apuração de impostos.

Por exemplo, no Rio de Janeiro há inúmeros incentivos fiscais criados pelo governo estadual para beneficiar certas áreas de atividade. Uma empresa beneficiada, e que portanto esteja sob regime especial, continuará realizando vendas e destacando 18% de alíquota de ICMS, contudo pagará apenas 3% de ICMS.

Se essa diferença for causada pela legislação sobre a área de atividade da empresa, ou por algum incentivo discal que não dependa de processos judiciais, então ela será tratada normalmente pelo Segundo Movimento. A única consequência será que os lançamentos do Segundo Movimento terão valores diferentes em seu campo VALOR do que está destacado no campo que guarda a informação original do XML

Porém, caso seja uma mudança fiscal adquirida por alguma ação ativa da empresa (como por exemplo, um processo no judiciário) será realizado um **Terceiro Movimento**.

Por exemplo, no caso de uma venda no RJ com regime diferenciado de 3% de ICMS. Haverá um lançamento de 18% de ICMS na apropriação da nota fiscal (Pois assim estará no XML), haverá um lançamento com aliquota de 18% para a guia de ICMS, e haverá um lançamento de -15% para a guia de ICMS. Esse caso se enquadra no **Terceiro Movimento** porque a empresa precisa abrir um processo judicial para que esse direito seja concretizado. Hoje esse processo é armazenado em scritta.processos.

Há também documentos cuja finalidade é afetar (em valores absolutos) a base ou o valor a serem pagos em impostos. Um exemplo é o Lalur, cuja finalidade é usar prejuízos anterioes para diminuir a base de IR do período atual. Esse tipo de documento terá seus próprios lançamentos de Segundo Momento, e não serão rateados sobre as notas, porque seu valor não depende do resultado do período.

### Impostos sobre Folha de Pagamento

Os impostos sobre a Folha de Pagamento seguirão a abordagem de dois movimentos.

O contra-cheque do funcionário já traz destacado os valores dos impostos, rubrica a rubrica. Cada linha do contra-cheque estará no Diário Unico

As linhas referentes a impostos terão vínculo simultaneamente com o Header da ordem-de-pagamento e com o Header da guia de imposto.

Mesmo impostos que não são descontados em folha, e portanto são invisíveis para o trabalhador (Exemplo: PIS sobre folha) terão lançamentos no cálculo da folha do funcionário, ainda que seja invisivel.

Concluindo, um contra-cheque de um funcionário terá lançamentos com os dois movimentos contábeis descritos acima.

### Impostos sobre lucro/resultado

Há ainda impostos sobre lucro/resultado da empresa (IR e CSLL), que podem ser por regime de competência ou por regime de caixa (Empresas de lucro presumido de pequeno porte).

Para esses impostos, que incidem sobre todas as movimentação financeiras realizadas, não serão criados lançamentos no momento das operações.

Periodicamente um job deverá criar essas guias o resultado dos meses abertos com movimento

### Mudança de tributação e impostos que possuem alíquotas/faixas

Embora a seja raro que haja mudança de alíquotas de impostos para pessoas jurídicas, não é impossível. (Por exemplo, empresas de lucro real mudam de alíquota de IR quando sua receita ultrapassa os 360mil reais)

Inicialmente, o sistema deverá ser parametrizado com uma alíquota inicial. Caso haja uma mudança de alíquota (o que é raro) o sistema deverá aplicar a mudança retroativamente.

O mesmo ocorrerá se uma empresa mudar seu regime tributário


### Simulação de mudança de regime tributário

Uma empresa pode fazer, enquanto cenário orçamentário, a suposição de mudança de regime triburário. Isso deverá invocar todas as pastas contábeis referentes a tributação para cálcular o resultado tributário sob o novo regime.

Essa operação será computacionalmente pesada, e poderá inflar o banco de dados. A melhor abordagem é que esses lançamentos sejam persistidos apenas por um período limitado de tempo. Suficiente apenas para que decisões estratégicas possam ser tomadas. Depois de passado esse período de tempo, esses lançamentos serão excluídos, e o cenário orçamento estará marcado como obsoleto, podendo ser recalculado no futuro, se necessário.


### [Clique aqui para visualizar exemplos de lançamentos de um documento](https://docs.google.com/spreadsheets/d/1SdFLibZTWXH-0doxxyM1oDnckROpqe1Rco9ptgEUxf0/edit?usp=sharing) 

# Pastas Contábeis e seus relacionamentos

- #### ICMS
  - Acionado em: Compra de mercadorias, venda de mercadorias,  prestação de serviços e aquisição de serviços.
  - Não é necessário para BAP/ESTASA
- #### PIS
  - Acionado em: Compra de mercadorias, venda de mercadorias, prestação de serviços, aquisição de serviços e folha de pagamento.
  - Necessário implementar a retenção em aquisição de serviços para BAP/ESTASA. A parte referente a Folha de Pagamento já é atendida pelo Persona.
- #### COFINS
  - Acionado em: Compra de mercadorias, venda de mercadorias, prestação de serviços e aquisição de serviços.
  - Necessário implementar a retenção em aquisição de serviços para BAP/ESTASA.
- #### CSLL
  - Acionado em: Compra de mercadorias, venda de mercadorias, prestação de serviços e aquisição de serviços.
  - Necessário implementar a retenção em aquisição de serviços para BAP/ESTASA.
- #### ISS
  - Acionado em: Prestação de serviços e aquisição de serviços.
  - Necessário implementar a retenção em aquisição de serviços para BAP/ESTASA.
- #### INSS e FGTS
  - Acionado em: Operações com Folha de Pagamento
  - Não é necessário para BAP/ESTASA pois já é atendido pelo Persona.
- #### IR
  - Sobre Lucro.
  - Não é necessário para os condomínios. Contudo será necessário para as administradoras.
