
# Pastas Contábeis de Operações com Mercadorias

Toda NFE ou NFCE poderá ser inserida no diário utilizando a API de Pastas Contábeis invocando uma Pasta Contábil chamada PastaDeOperacoesComMercadorias.
Essa Pasta ficará responsável por avaliar o documento recebido e direcionar para a Pasta Contábil adequada de acordo com o CFOP ou qualquer outro critério de avaliação adequado.


## Escrituração Antecipada

Uma vez por dia será executado um JOB que irá escriturar antecipadamente NFEs para os próximos 12 meses de cada estabelecimento.
Cadastradas no último dia de cada mês, esses documentos terão seus valores baseados na média mensal de NFEs dos últimos três meses.
Será um documento para cada tupla (Estabelecimento;Sinal;Participante;CFOP)
Esses documentos terão seus lançamentos agrupados por  Ítem de estoque.


A previsão será realizada apenas para meses posteriores ao mês atual. O mês atual não terá valores previstos, apenas realizados.

Ao iniciar um novo mês, o documento escriturado antecipadamente desse mês será apagado

### Entrada
```json
{
    "Estabelecimento": "<Codigo do estabelecimento>"
}
```


## Apropriação

Uma nova NFE deverá ser cadastrada no Diário Unico usando a rota da pasta PastaDeOperacoesComMercadorias. Pois caberá ao Diário Unico decidir qual a pasta contábil adequada para aquela NFE

O json a ser passado para a rota tem a seguinte assinatura:

### Entrada

A definição de entrada será expandida no futuro, conforme as pastas forem sendo implementadas e precisarem de mais informações

```json
{
  "numero": "<Número do documento>",
  "participante": "<Participante do documento>",
  "cfop": "<CFOP do documento>",
  "data_de_lancamento": "<Data de emissão do documento>",
  "valor": "<Valor>",
  "modelo": "<Modelo do documento>",
  "sinal": "<Entrada ou Saída>",
  "itens":[
      {
        "codigo": "<Código do ítem de estoque>",
        "descricao": "<Descrição do ítem de estoque>",
        "quantidade": "<Quantidade>",
        "valor": "<Valor>"
      }
    ]
}
```

## Roteamento para a Pasta Contábil adequada

O criério para definir a Pasta Contábil adequada para lidar com uma NFE será o seguinte:

|CFOP	|Modelo	    |Sinal	|Pasta Contábil                                         |
| ------------ | ------------ | ------------ | ------------ |
|-	    |NCE/NFCE	|Saída	|PastaVendaConsumidorFinal|
|-	    |SAT	    |Saída	|PastaVendaConsumidorFinal|
|1101	|NFE	    |-	    |PastaCompraMercadorias|
|1102	|NFE	    |-	    |PastaCompraMercadorias|
|1111	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|1113	|NFE	    |-	    |PastaCompraMercadorias|
|1116	|NFE	    |-	    |PastaCompraMercadorias|
|1117	|NFE	    |-	    |PastaCompraMercadorias|
|1118	|NFE	    |-	    |PastaCompraMercadorias|
|1120	|NFE	    |-	    |PastaCompraMercadorias|
|1121	|NFE	    |-	    |PastaCompraMercadorias|
|1122	|NFE	    |-	    |PastaCompraMercadorias|
|1124	|NFE	    |-	    |PastaCompraMercadorias|
|1125	|NFE	    |-	    |PastaCompraMercadorias|
|1126	|NFE	    |-	    |PastaCompraMercadorias|
|1128	|NFE	    |-	    |PastaCompraMercadorias|
|1151	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1152	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1153	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1154	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1201	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1202	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1203	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1204	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1206	|NFE	    |-	    |PastaAnulaçãoValorRelativoPrestaçãoServiçoTransporte|
|1207	|NFE	    |-	    |PastaAnulaçãoVendaEnergiaElétrica|
|1208	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1209	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1251	|NFE	    |-	    |PastaCompraMercadorias|
|1252	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1253	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1254	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1255	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1256	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1257	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|1401	|NFE	    |-	    |PastaCompraMercadorias|
|1403	|NFE	    |-	    |PastaCompraMercadorias|
|1406	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|1407	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|1408	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1409	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1410	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1411	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1415	|NFE	    |-	    |PastaOutrasEntradas|
|1501	|NFE	    |-	    |PastaCompraMercadorias|
|1503	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1504	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1551	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|1552	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1554	|NFE	    |-	    |PastaRetornoImobilizadoRemetidoParaUsoForaEstabelecimen|to
|1555	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|1556	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|1557	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1602	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1605	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1650	|NFE	    |-	    |PastaCompraMercadorias|
|1651	|NFE	    |-	    |PastaCompraMercadorias|
|1652	|NFE	    |-	    |PastaCompraMercadorias|
|1653	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|1658	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1659	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|1660	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1661	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1662	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|1901	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|1902	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|1903	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|1904	|NFE	    |-	    |PastaOutrasEntradas|
|1905	|NFE	    |-	    |PastaOutrasEntradas|
|1906	|NFE	    |-	    |PastaOutrasEntradas|
|1907	|NFE	    |-	    |PastaOutrasEntradas|
|1908	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|1909	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|1910	|NFE	    |-	    |PastaEntradaDeBrinde|
|1911	|NFE	    |-	    |PastaEntradaDeBrinde|
|1912	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|1913	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|1914	|NFE	    |-	    |PastaOutrasEntradas|
|1915	|NFE	    |-	    |PastaEntradaDeBensOuMercadoriasRecebidosParaConserto|
|1916	|NFE	    |-	    |PastaRetornoDeBensOuMercadoriasParaReparoOuConserto|
|1917	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|1918	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|1919	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|1920	|NFE	    |-	    |PastaOutrasEntradas|
|1921	|NFE	    |-	    |PastaOutrasEntradas|
|1922	|NFE	    |-	    |PastaOutrasEntradas|
|1923	|NFE	    |-	    |PastaOutrasEntradas|
|1924	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|1925	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|1926	|NFE	    |-	    |PastaOutrasEntradas|
|1949	|NFE	    |-	    |PastaOutrasEntradas|
|2101	|NFE	    |-	    |PastaCompraMercadorias|
|2102	|NFE	    |-	    |PastaCompraMercadorias|
|2111	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|2113	|NFE	    |-	    |PastaCompraMercadorias|
|2116	|NFE	    |-	    |PastaCompraMercadorias|
|2117	|NFE	    |-	    |PastaCompraMercadorias|
|2118	|NFE	    |-	    |PastaCompraMercadorias|
|2120	|NFE	    |-	    |PastaCompraMercadorias|
|2121	|NFE	    |-	    |PastaCompraMercadorias|
|2122	|NFE	    |-	    |PastaCompraMercadorias|
|2124	|NFE	    |-	    |PastaCompraMercadorias|
|2125	|NFE	    |-	    |PastaCompraMercadorias|
|2126	|NFE	    |-	    |PastaCompraMercadorias|
|2128	|NFE	    |-	    |PastaCompraMercadorias|
|2151	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2152	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2153	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2154	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2201	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2202	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2203	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2204	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2206	|NFE	    |-	    |PastaAnulaçãoValorRelativoPrestaçãoServiçoTransporte|
|2207	|NFE	    |-	    |PastaAnulaçãoVendaEnergiaElétrica|
|2208	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2209	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2251	|NFE	    |-	    |PastaCompraMercadorias|
|2252	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2253	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2254	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2255	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2256	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2257	|NFE	    |-	    |PastaAquisiçãoServiçosPúblicos|
|2401	|NFE	    |-	    |PastaCompraMercadorias|
|2403	|NFE	    |-	    |PastaCompraMercadorias|
|2406	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|2407	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|2408	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2409	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2410	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2411	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2415	|NFE	    |-	    |PastaOutrasEntradas|
|2501	|NFE	    |-	    |PastaCompraMercadorias|
|2551	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|2552	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2554	|NFE	    |-	    |PastaRetornoImobilizadoRemetidoParaUsoForaEstabelecimen|to
|2555	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|2556	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|2651	|NFE	    |-	    |PastaCompraMercadorias|
|2652	|NFE	    |-	    |PastaCompraMercadorias|
|2653	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|2658	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2659	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosEntradas|
|2660	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2661	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2662	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|2901	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|2902	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|2903	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|2904	|NFE	    |-	    |PastaOutrasEntradas|
|2905	|NFE	    |-	    |PastaOutrasEntradas|
|2906	|NFE	    |-	    |PastaOutrasEntradas|
|2907	|NFE	    |-	    |PastaOutrasEntradas|
|2908	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|2909	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|2910	|NFE	    |-	    |PastaEntradaDeBrinde|
|2911	|NFE	    |-	    |PastaEntradaDeBrinde|
|2912	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|2913	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|2914	|NFE	    |-	    |PastaOutrasEntradas|
|2915	|NFE	    |-	    |PastaEntradaDeBensOuMercadoriasRecebidosParaConserto|
|2916	|NFE	    |-	    |PastaRetornoDeBensOuMercadoriasParaReparoOuConserto|
|2917	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|2918	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|2919	|NFE	    |-	    |PastaEntradaDevoluçãoDeConsignação|
|2920	|NFE	    |-	    |PastaOutrasEntradas|
|2921	|NFE	    |-	    |PastaOutrasEntradas|
|2922	|NFE	    |-	    |PastaOutrasEntradas|
|2923	|NFE	    |-	    |PastaOutrasEntradas|
|2924	|NFE	    |-	    |PastaEntradasParaIndustrialização|
|2925	|NFE	    |-	    |PastaRetornoMercadoriaRemetidaIndústriaPorEncomenda|
|2949	|NFE	    |-	    |PastaOutrasEntradas|
|3101	|NFE	    |-	    |PastaCompraMercadorias|
|3102	|NFE	    |-	    |PastaCompraMercadorias|
|3126	|NFE	    |-	    |PastaCompraMercadorias|
|3127	|NFE	    |-	    |PastaCompraMercadorias|
|3128	|NFE	    |-	    |PastaCompraMercadorias|
|3201	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|3202	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|3503	|NFE	    |-	    |PastaDevoluçãoVendaMercadoria|
|3551	|NFE	    |-	    |PastaCompraAtivoImobilizado|
|3556	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|3653	|NFE	    |-	    |PastaCompraMaterialUsoConsumo|
|3949	|NFE	    |-	    |PastaCompraMercadorias|
|5101	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5101	|NFE	    |-	    |PastaVendaMercadorias|
|5102	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5102	|NFE	    |-	    |PastaVendaMercadorias|
|5103	|NFE	    |-	    |PastaVendaMercadorias|
|5103	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5104	|NFE	    |-	    |PastaVendaMercadorias|
|5104	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5105	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5105	|NFE	    |-	    |PastaVendaMercadorias|
|5106	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5106	|NFE	    |-	    |PastaVendaMercadorias|
|5109	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5109	|NFE	    |-	    |PastaVendaMercadorias|
|5110	|NFE	    |-	    |PastaVendaMercadorias|
|5110	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5111	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5111	|NFE	    |-	    |PastaVendaMercadorias|
|5112	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5112	|NFE	    |-	    |PastaVendaMercadorias|
|5113	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5113	|NFE	    |-	    |PastaVendaMercadorias|
|5114	|NFE	    |-	    |PastaVendaMercadorias|
|5114	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5115	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5115	|NFE	    |-	    |PastaVendaMercadorias|
|5116	|NFE	    |-	    |PastaOutrasSaidas|
|5117	|NFE	    |-	    |PastaVendaMercadorias|
|5118	|NFE	    |-	    |PastaVendaMercadorias|
|5119	|NFE	    |-	    |PastaVendaMercadorias|
|5119	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5120	|NFE	    |-	    |PastaVendaMercadorias|
|5120	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5122	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5122	|NFE	    |-	    |PastaVendaMercadorias|
|5123	|NFE	    |-	    |PastaVendaMercadorias|
|5123	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5124	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5124	|NFE	    |-	    |PastaVendaMercadorias|
|5125	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5125	|NFE	    |-	    |PastaVendaMercadorias|
|5132	|NFE	    |-	    |PastaVendaMercadorias|
|5151	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5152	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5153	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5155	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5156	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5201	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5202	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5206	|NFE	    |-	    |PastaAnulaçãoValorRelativoAquisiçãoDeServiçoDeTransport|e
|5207	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5208	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5209	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5210	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5251	|NFE	    |-	    |PastaVendaMercadorias|
|5252	|NFE	    |-	    |PastaVendaMercadorias|
|5253	|NFE	    |-	    |PastaVendaMercadorias|
|5301	|NFE	    |-	    |PastaVendaMercadorias|
|5301	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5303	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5303	|NFE	    |-	    |PastaVendaMercadorias|
|5307	|NFE	    |-	    |PastaVendaMercadorias|
|5307	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5401	|NFE	    |-	    |PastaVendaMercadorias|
|5401	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5402	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5402	|NFE	    |-	    |PastaVendaMercadorias|
|5403	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5403	|NFE	    |-	    |PastaVendaMercadorias|
|5405	|NFE	    |-	    |PastaVendaMercadorias|
|5405	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5408	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5409	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5410	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5411	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5412	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|5413	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|5415	|NFE	    |-	    |PastaOutrasSaidas|
|5501	|NFE	    |-	    |PastaVendaMercadorias|
|5502	|NFE	    |-	    |PastaVendaMercadorias|
|5503	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5551	|NFE	    |-	    |PastaVendaDeBemDoAtivoImobilizado|
|5552	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5553	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|5554	|NFE	    |-	    |PastaRemessaDeImobilizadoParaUsoForaDoEstabelecimento|
|5556	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|5557	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5602	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5650	|NFE	    |-	    |PastaVendaMercadorias|
|5650	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5651	|NFE	    |-	    |PastaVendaMercadorias|
|5651	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5652	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5652	|NFE	    |-	    |PastaVendaMercadorias|
|5653	|NFE	    |-	    |PastaVendaMercadorias|
|5653	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5654	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5654	|NFE	    |-	    |PastaVendaMercadorias|
|5655	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5655	|NFE	    |-	    |PastaVendaMercadorias|
|5656	|NFE	    |-	    |PastaVendaMercadorias|
|5656	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5658	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5659	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|5660	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5661	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5662	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|5667	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5667	|NFE	    |-	    |PastaVendaMercadorias|
|5901	|NFE	    |-	    |PastaRemessaParaIndustrializaçãoPorEncomenda|
|5902	|NFE	    |-	    |PastaRetornoDeMercadoriaUtilizadaNaIndustrialização|
|5904	|NFE	    |-	    |PastaOutrasSaidas|
|5905	|NFE	    |-	    |PastaOutrasSaidas|
|5906	|NFE	    |-	    |PastaOutrasSaidas|
|5907	|NFE	    |-	    |PastaOutrasSaidas|
|5908	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|5909	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|5910	|NFE	    |-	    |PastaSaídaDeBrindes|
|5911	|NFE	    |-	    |PastaSaídaDeBrindes|
|5912	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|5913	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|5914	|NFE	    |-	    |PastaOutrasSaidas|
|5915	|NFE	    |-	    |PastaRemessaDeBensOuMercadoriasParaReparoOuConserto|
|5916	|NFE	    |-	    |PastaRetornoDeBensOuMercadoriasRecebidosParaConserto|
|5917	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|5918	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|5919	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|5920	|NFE	    |-	    |PastaOutrasSaidas|
|5921	|NFE	    |-	    |PastaOutrasSaidas|
|5922	|NFE	    |-	    |PastaVendaConsumidorFinal|
|5922	|NFE	    |-	    |PastaVendaMercadorias|
|5923	|NFE	    |-	    |PastaOutrasSaidas|
|5924	|NFE	    |-	    |PastaOutrasSaidas|
|5925	|NFE	    |-	    |PastaRetornoDeMercadoriaUtilizadaNaIndustrialização|
|5926	|NFE	    |-	    |PastaOutrasSaidas|
|5927	|NFE	    |-	    |PastaBaixaDeEstoque|
|5928	|NFE	    |-	    |PastaBaixaDeEstoque|
|5934	|NFE	    |-	    |PastaOutrasSaidas|
|5949	|NFE	    |-	    |PastaOutrasSaidas|
|6101	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6101	|NFE	    |-	    |PastaVendaMercadorias|
|6102	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6102	|NFE	    |-	    |PastaVendaMercadorias|
|6103	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6103	|NFE	    |-	    |PastaVendaMercadorias|
|6104	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6104	|NFE	    |-	    |PastaVendaMercadorias|
|6105	|NFE	    |-	    |PastaVendaMercadorias|
|6105	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6106	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6106	|NFE	    |-	    |PastaVendaMercadorias|
|6107	|NFE	    |-	    |PastaVendaMercadorias|
|6107	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6108	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6108	|NFE	    |-	    |PastaVendaMercadorias|
|6109	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6109	|NFE	    |-	    |PastaVendaMercadorias|
|6110	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6110	|NFE	    |-	    |PastaVendaMercadorias|
|6111	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6111	|NFE	    |-	    |PastaVendaMercadorias|
|6112	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6112	|NFE	    |-	    |PastaVendaMercadorias|
|6113	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6113	|NFE	    |-	    |PastaVendaMercadorias|
|6114	|NFE	    |-	    |PastaVendaMercadorias|
|6114	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6115	|NFE	    |-	    |PastaVendaMercadorias|
|6115	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6116	|NFE	    |-	    |PastaOutrasSaidas|
|6117	|NFE	    |-	    |PastaVendaMercadorias|
|6118	|NFE	    |-	    |PastaVendaMercadorias|
|6119	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6119	|NFE	    |-	    |PastaVendaMercadorias|
|6120	|NFE	    |-	    |PastaVendaMercadorias|
|6120	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6122	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6122	|NFE	    |-	    |PastaVendaMercadorias|
|6123	|NFE	    |-	    |PastaVendaMercadorias|
|6123	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6124	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6124	|NFE	    |-	    |PastaVendaMercadorias|
|6125	|NFE	    |-	    |PastaVendaMercadorias|
|6125	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6132	|NFE	    |-	    |PastaVendaMercadorias|
|6151	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6152	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6153	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6155	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6156	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6201	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6202	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6206	|NFE	    |-	    |PastaAnulaçãoValorRelativoAquisiçãoDeServiçoDeTransport|e
|6207	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6208	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6209	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6251	|NFE	    |-	    |PastaVendaMercadorias|
|6252	|NFE	    |-	    |PastaVendaMercadorias|
|6253	|NFE	    |-	    |PastaVendaMercadorias|
|6301	|NFE	    |-	    |PastaVendaMercadorias|
|6301	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6303	|NFE	    |-	    |PastaVendaMercadorias|
|6303	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6307	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6307	|NFE	    |-	    |PastaVendaMercadorias|
|6401	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6401	|NFE	    |-	    |PastaVendaMercadorias|
|6402	|NFE	    |-	    |PastaVendaMercadorias|
|6402	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6403	|NFE	    |-	    |PastaVendaMercadorias|
|6403	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6404	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6404	|NFE	    |-	    |PastaVendaMercadorias|
|6408	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6409	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6410	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6411	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6413	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|6415	|NFE	    |-	    |PastaOutrasSaidas|
|6501	|NFE	    |-	    |PastaVendaMercadorias|
|6502	|NFE	    |-	    |PastaVendaMercadorias|
|6503	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6551	|NFE	    |-	    |PastaVendaDeBemDoAtivoImobilizado|
|6552	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6553	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|6554	|NFE	    |-	    |PastaRemessaDeImobilizadoParaUsoForaDoEstabelecimento|
|6555	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|6556	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|6557	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6651	|NFE	    |-	    |PastaVendaMercadorias|
|6651	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6652	|NFE	    |-	    |PastaVendaMercadorias|
|6652	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6653	|NFE	    |-	    |PastaVendaMercadorias|
|6653	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6654	|NFE	    |-	    |PastaVendaMercadorias|
|6654	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6655	|NFE	    |-	    |PastaVendaMercadorias|
|6655	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6656	|NFE	    |-	    |PastaVendaMercadorias|
|6656	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6658	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6659	|NFE	    |-	    |PastaTransferênciaEntreEstabelecimentosSaídas|
|6660	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6661	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6662	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|6667	|NFE	    |-	    |PastaVendaMercadorias|
|6667	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6901	|NFE	    |-	    |PastaRemessaParaIndustrializaçãoPorEncomenda|
|6902	|NFE	    |-	    |PastaRetornoDeMercadoriaUtilizadaNaIndustrialização|
|6904	|NFE	    |-	    |PastaOutrasSaidas|
|6905	|NFE	    |-	    |PastaOutrasSaidas|
|6906	|NFE	    |-	    |PastaOutrasSaidas|
|6907	|NFE	    |-	    |PastaOutrasSaidas|
|6908	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|6909	|NFE	    |-	    |PastaBensPorContaContratoComodato|
|6910	|NFE	    |-	    |PastaSaídaDeBrindes|
|6911	|NFE	    |-	    |PastaSaídaDeBrindes|
|6912	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|6913	|NFE	    |-	    |PastaMercadoriaOuBemParaDemonstração|
|6914	|NFE	    |-	    |PastaOutrasSaidas|
|6915	|NFE	    |-	    |PastaRemessaDeBensOuMercadoriasParaReparoOuConserto|
|6916	|NFE	    |-	    |PastaRetornoDeBensOuMercadoriasRecebidosParaConserto|
|6917	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|6918	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|6919	|NFE	    |-	    |PastaRemessaOuDevoluçãoDeConsignação|
|6920	|NFE	    |-	    |PastaOutrasSaidas|
|6921	|NFE	    |-	    |PastaOutrasSaidas|
|6922	|NFE	    |-	    |PastaVendaMercadorias|
|6922	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6923	|NFE	    |-	    |PastaOutrasSaidas|
|6924	|NFE	    |-	    |PastaOutrasSaidas|
|6925	|NFE	    |-	    |PastaRetornoDeMercadoriaUtilizadaNaIndustrialização|
|6933	|NFE	    |-	    |PastaVendaMercadorias|
|6933	|NFE	    |-	    |PastaVendaConsumidorFinal|
|6934	|NFE	    |-	    |PastaOutrasSaidas|
|6949	|NFE	    |-	    |PastaOutrasSaidas|
|7101	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7101	|NFE	    |-	    |PastaVendaMercadorias|
|7102	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7102	|NFE	    |-	    |PastaVendaMercadorias|
|7105	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7105	|NFE	    |-	    |PastaVendaMercadorias|
|7106	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7106	|NFE	    |-	    |PastaVendaMercadorias|
|7127	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7127	|NFE	    |-	    |PastaVendaMercadorias|
|7202	|NFE	    |-	    |PastaDevoluçãoCompraMercadoria|
|7301	|NFE	    |-	    |PastaVendaMercadorias|
|7301	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7501	|NFE	    |-	    |PastaVendaMercadorias|
|7551	|NFE	    |-	    |PastaVendaDeBemDoAtivoImobilizado|
|7553	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|7556	|NFE	    |-	    |PastaDevoluçãoDeCompraBensDeConsumoOuImobilizado|
|7651	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7651	|NFE	    |-	    |PastaVendaMercadorias|
|7654	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7654	|NFE	    |-	    |PastaVendaMercadorias|
|7657	|NFE	    |-	    |PastaVendaConsumidorFinal|
|7657	|NFE	    |-	    |PastaVendaMercadorias|
|7667	|NFE	    |-	    |PastaVendaMercadorias|
|7667	|NFE	    |-	    |PastaVendaConsumidorFinal|


## [Lançamentos Contábeis ](https://docs.google.com/spreadsheets/d/1E4JPjJuzailjlwZSgXjYthDGvw4aci0MeBszVYdcl3o/edit?usp=sharing "## Lançamentos Contábeis ")


