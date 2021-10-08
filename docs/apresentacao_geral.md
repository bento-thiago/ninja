
# Como o diário unico atenderá aos vários requisitos do ERP.

## Abordagem por Snapshot

* O Diário unico terá linhas específicas (Definidas por um valor específico no campo diario_unico_tipo) que representarão o saldo (Soma de movimentações) de algum valor contábil naquela data.<br/><br/>
* Por exemplo, linhas com o saldo de uma conta contábil em determinada data, rateado por todas as dimensões aplicáveis, como estabelecimento, participante, centro de custo, projeto, etc.<br/><br/>
* Para obter o saldo de uma conta na data X, podemos fazer nossos cálculos a partir da linha de snapshot mais recente anterior a data X, e então somar os lançamentos até alcançar a exata data desejada.<br/><br/>
* Haverá um (ou mais) Jobs responsáveis por criar essas linhas de Snapshot quando um mês for contabilmente encerrado. Um critério possível para considerar um mês contabilmente encerrado é o envio do SPED fiscal,  que pode ser entregue até o 25o dia do mês subsequente<br/><br/>
* Caso haja uma alteração em um documento de uma data contabilmente encerrada (eg. Base de homologação ou com alguém que esteja retificando seu SPED) o sistema irá imediatamete excluir as linhas de Snapshots posteriores a essa data (Filtrando pelas dimensões). Eventualmente o Job supracitado irá gerar novamente essas linhdas de Snapshot<br/><br/><br/>
Como veremos abaixo, essa abordagem será usada para vários tipos de cálculos.


## Como obter saldo de estoque?
<br/>

* Para obter o Saldo de Estoque de um ítem, deverá usar a última linha de Saldo de Estoque como Saldo de Estoque inicial,
e então calcular a movimentação do saldo de estoque das notas seguintes, até a data desejada

## Como tratar inventários?

* O Inventário também será calculad considerando o último Snapshot. Sempre que houver um ajuste de inventário, serão inseridos novos snapshots para CMP e Saldo de Estoque. Esse Snapshot gravado pelo ajuste de inventário será permanente e não será excluído ainda que haja movimento em data anterior a sua criação.

## Como calcular Custo Medio Ponderado?

* O valor de custo de um produto, dentro de determinada nota, será obtido a partir da soma das linhas do Diário Unico
que forem referentes a campos que façam parte do custo (eg. valor, frete, etc). Claro que isso será aplicável apenas a
certos tipos de nota (eg. compra). Como esse valor pode ser inferido a partir de agregações de linhas da nota, não será criada 
uma linha específica com o valor de custo para cada nota

* Caso haja conhecimento de novos documentos que impactem no custo de um produto (eg. Nota de Conhecimento de Transporte), serão inseridas
linhas no Diário Unico. Uma linha para cada produto afetado. Essas linhas serão vinculadas ao novo documento,
e não ao documento original de entrada do produto. Isso é para que possamos rastrear adequadamente a origem dessas linhas. E caso o novo
documento de custo-extra seja alterado/excluído, essas linhas precisarão ser alteradas/excluídas

* Para um relatório encontrar o CMP em uma data arbitrária, será feito pela fórmula:
CMP[data] = ((<CMP do mês anterior> * <Quantidade do mês anterior>) + <Soma dos custos de todas as notas entre o mês anterior e a data interessada>)/
            (<Quantidade do mês anterior> + <Soma das quantidades de notas>)


* Sabendo o Saldo de Estoque, anterior e corrente, é possível obter a qualquer momento o CMV. 
Formula: CMV = (Saldo de estoque inicial) + (Compras) + (Devolucoes de vendas) – (Devolucoes de Compras) – (Saldo de estoque atual).


## Como tratar cenários orçamentários?


* Haverá um cadastro de Cenários Orçamentários (C.O.). Cada C.O. terá um exercício de competência,
código, e Status (Aprovação, em elaboração, etc).

* Cada Linha do C.O. será uma Conta Contábil, pois a Conta Contábil indica a operação realizada
(eg. Venda de produtos, Impostos pagos, etc). Esse orçamento poderá ser rateado pelas dimensões
do D.U. (eg. projeto, centro de custo, etc). A estrutura do DU permitirá agregações personalizadas,
como por exemplo, orçamento consolidado de diversos projetos.

* O acompanhamento de um cenário orçamentario se fará por meio da visualização das colunas
Valor Planejado, Valor Realizado, Valor Histórico, e a Diferença entre os valores Planejados 
e Realizados. A coluna Histórico terá um valor estimado automaticamente pelo sistema, 
baseado no histórico realizado pelo cliente. As heurísticas de estimativa podem usar 
uma média simples ou considerar sazonalidades.

* O valor histórico será baseado apenas em meses contabilmente encerrados. O módulo de 
encerramento contábil será configurável, e não será detalhado aqui.

* As informações previstas pelo sistema irão compor um cenário orçamentário adicional, 
que não pode ser alterado pelo usuário. Chamarei esse C.O. de C.O. Automático

* Diversos relatórios dos sistemas terão a funcionalidade de Fecho Anual. Essa funcionalidade
consiste do cliente poder, a qualquer dia, tirar um relatório com dados até o final do ano.
Dados de meses ainda vindouros serão estimados baseados em um Cenário Orçamentário.
Por Default, o Cenário orçamentário sugerido para o Fecho Anual será o C.O. Automático

* Sempre que for cadastrado um novo C.O., será inserida uma linha em uma tabela específica
para Cenários Orçamentários

* Os valores Planejados que compõem o Cenário orçamentário estarão persistidos no Diário
Unico. Contendo a Conta Contábil, valor, e data com o último dia do mês competente 
ao valor orçado

## Como tratar custos e receitas previstos?

* Periodicamente, um (ou mais) Job usará um conjunto de heurísticas para prever
receitas e despesas para os próximos 12 meses

* Serão então gerados um conjunto de documentos de previsão. Um documento para cada tipo
de receita/despesa (eg. conta de luz, conta de água, etc...), para cada mês, nos próximos 12 meses

* Esses documentos serão gravados nas tabelas de documentos. Será criado um campo na tabela
de documentos para indicar se é um documento de previsao.

* Seus lançamentos serão gerados e armazenados no diário unico. Também será criado
um campo na tabela de diario unico para indicar que é um lançamento de previsao.
Esse campo será redundante, pois o documento já tem esse indicador.


* Documentos de previsao serão totalmente invisiveis para o usuário, inclusive em todos
os relatórios e apurações fiscais. Sua razão de existir é apenas para rastrear
agrupamentos de lançamentos de previsão.

* Os Jobs também serão responsáveis por atualizar documentos (e lançamentos) de previsao
de meses futuros conforme novos dados forem armazenados no sistema.



## Como tratar Extratos Bancários?

* Lancamentos em Contas Bancárias (hoje financas.lancamentoscontas) serão armazenados no Diário Unico

* Para obter o extrato bancário pelo ERP, será apenas exibida uma listagem desses lançamentos com o filtro
selecionado (Conta bancaria, período, etc)

* Durante o processo de conciliação bancária, quando o cliente importar o arquivo OFX contendo seu extrato bancário,
o ERP armazenará as linhas de extrato bancário importadas no Diário Unico
(com um indicador específico em diario_unico_tipo).

* No processo de conciliação bancária, quando um lançamento em conta for conciliado por um lançamento
de extrato bancário, a linha do lançamento em conta do diário unico terá o GUID do lançamento
de extrato preenchido no campo [Conciliado_por: UUID (Auto FK)] Para auditoria da conciliação, 
também haverá o campo [Conciliado_em: Date]

### Questões em aberto:

1. É interessante tornar evidente os lançamentos vindos de um extrato bancário, porém ainda não conciliados com nenhuma
lançamento do diário unico?  


## Como obter saldo de uma conta contábil?

* A cada mês contabilmente encerrado, serão inseridas linhas no diário unico com o saldo 
das contas contábeis (snapshots).

* Para que seja possível exibir relatórios com diferentes dimensões, essas linhas serão rateadas
pelas principais dimensões dos lançamentos [conta ; centro de custo; projeto; participante, etc].

## Como obter a movimentação Contábil/Financeira de uma dimensão qualquer?
* Para uma dimensão qualquer (eg: conta contabil, conta financeira, centro de custo, projeto, etc),
é possível obter sua movimentação/saldo monetário a partir da soma dos lançamentos contábeis do diário unico,
agrupando/filtrando por essa dimensão.

* Isso parte da premissa de que todo movimento financeiro é um lançamento
contábil.

## Como calcular um balancete?

* Um balancete de verificação por período (data inicial e final), deverá ser feito calculando o saldo duas vezes,
uma vez para a data inicial, e outra para a data final.

* Um balancete de verificação mensal, poderá ser feito calculando o saldo 12 vezes. Contudo, para todos os meses
já encerrados bastará recuperar a linha de snapshot.

## Como calcular os dados de um fluxo de caixa?

* O Fluxo de Caixa é uma amostragem de movimentação de uma dimensão qualquer. Hoje, o ERP permite Classificação Financeira, 
Centro de Custo, Projeto e Conta. Com a abordagem do diário Unico, as agregações (group by) usando essas mesmas
dimensões resolveria o problema.

* Além disso, a estrutura permite utilizar, de modo equivalente, qualquer das dimensões de BI presentes no diário unico.

* O Fluxo de Caixa oferece dados separados visualmente por OPERAÇÃO (entradas, saidas, transferencias, saldo final). Isso
poderá ser realizado utilizando-se os campos [Tipo] e [Sinal] do diário unico.

