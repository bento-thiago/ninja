# FinanceiroAPI
MOPE 64 (Finanças) - Controle de contas a pagar e receber, conciliação bancária, etc.

## Rotas

### PJBank

Rotas destinadas a integração com o PJBank

#### Webhooks

Rotas destinadas ao retorno da comunicação com o PJBank, isto é, a escuta de chamadas realizadas pelo banco, com o fim de informar com respeito a atualização de estado para um ação registrada junto ao banco (isto é, cobranças ou pagamentos registrados).

__Assim, se tratando de uma comunicação passiva (que recebe o retorno de chamadas assincronas relizadas anteriormente), o PJBank envia no corpo de cada webhook o campo _chave_, o qual é único por conta (isto é, por credencial gerada no registro de uma conta). E portanto, este campo _chave_ deve ser armazenado na entidade _conta_financeira_ logo após a primeira recepção de webhook, pois se trata de um mecanismo de segurança na comunicação, pois permitirá identificar que um webhook futuro partiu realmente do PJBank (já que apenas este conhece a chave de cada conta, e a comunicação toda se faz via HTTPS).__

##### Webhook Boletos

Recebendo informações a respeito dos boletos de cobrança registrados ao banco.

* **Endpoint:** {base_url}/api/{tenant}/pjbank/boleto/{id_documento}
  * Exemplo: http://financeiro.nasajon.com.br/gednasajon/pjbank/boleto/6a00a613-f8f7-4d2f-91ad-13a3caf7d9a1
* **Método HTTP:** PUT
* **Parâmetros da URL:**
  * tenant: Identificador do tenant do cliente
  * id_documento: Identificador único, do documento que deu origem ao boleto, no diário unico.
* **Corpo da requisição:**

1. Boleto registrado com sucesso:
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "100",
    "nosso_numero": "24483712",
    "id_unico": "24483712",
    "pedido_numero": "10",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "confirmado"
}
```

2. Boleto com registro rejeitado:
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "100",
    "nosso_numero": "24483712",
    "id_unico": "24483712",
    "pedido_numero": "10",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "rejeitado",
    "registro_rejeicao_motivo": "Data de Vencimento Inválida"
}
```

3. Boleto baixado no banco (boleto cancelado):
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "100",
    "nosso_numero": "24483712",
    "id_unico": "24483712",
    "pedido_numero": "10",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "baixado"
}
```

4. Boleto alterado após registro (isto é, boletos alterados antes da efetivação do registro bancário nao disparam chamada ao webhook; porém boletos alterados após registro bancário incorrem na alteração no _nosso_numero_ e também na alteração do _id_unico_, ambos gerados pelo PJBank; notar no retorno o eco do _nosso_numero_ e do _id_unico_ anteriores a alteração do boleto, agora com o sufixo _original_):
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "300",
    "nosso_numero": "24483856",
    "nosso_numero_original": "24483855",
    "id_unico": "24483856",
    "id_unico_original": "24483855",
    "pedido_numero": "25",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "pendente"
}
```
**Obs.:** Neste caso, importa observar que após o novo registro bancário do boleto alterado, um novo webhook ainda será gerado, porém com a alteração de um dos campos: ```"registro_sistema_bancario": "confirmado"```, indicando que a alteração já foi registrada no sistema bancário.

5. Boleto pago pelo sacado:
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "100",
    "valor_pago": "100",
    "valor_liquido": "97.5",
    "valor_tarifa": "2.5",
    "nosso_numero": "24483860",
    "id_unico": "24483860",
    "pedido_numero": "90",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "data_pagamento": "07/24/2018",
    "data_credito": "07/26/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "confirmado"
}
```

6. Boleto pago mais de uma vez pelo sacado:
```json
{
    "operacao": "PUT",
    "tipo": "recebimento_boleto",
    "valor": "100",
    "valor_pago": "100",
    "valor_liquido": "97.5",
    "valor_tarifa": "2.5",
    "pagamento_duplicado": "1",
    "nosso_numero": "24483861",
    "nosso_numero_original": "24483860",
    "id_unico": "24483861",
    "id_unico_original": "24483860",
    "pedido_numero": "90",
    "banco_numero": "033",
    "token_facilitador": "a33235e33d0cec740e01cf6d8ab8325089061692",
    "data_vencimento": "07/24/2018",
    "data_pagamento": "07/24/2018",
    "data_credito": "07/26/2018",
    "credencial": "f9c697887f39e31f3f1411fb04516aea53eb0637",
    "chave": "bd3f0c8adef026744ac53fa19f31aadfb96c0861",
    "registro_sistema_bancario": "confirmado"
}
```
**Obs.:** Neste caso o _id_unico_ é alterado, no entanto, o valor anterior do mesmo é enviado no campo _id_unico_original_, além disto, é adicionado a seguinte informação para facilitar a identificação de que se trata de um pagamento em duplicidade: ```"pagamento_duplicado": "1"```.

* **Resposta da requisição:**
```json
{
    "status": "200"
}
```

**Obs. 1:** Em caso de sucesso no processamento do webhook, deve-se responder ao PJBank com o JSON acima, pois o PJBank não se utiliza do HTTP 200 como sinal suficiente de sucesso, visto que o em caso de chamada a uma URL válida, porém incorreta, o HTTP 200 poderia ser reproduzido por acidente.

**Obs. 2:** O PJBank espera uma resposta com timeout de 20 segundos, não podendo o processamento ultrapassar este tempo.

**Obs. 3:** Em caso de falha na chamada ao webhook, o PJBank tentará outras 9 vezes em horários diferentes (totalizando 10 tentativas).

###### Ações da rota

O objetivo desta rota está no conciliação automática junto ao banco com relação aos boletos de cobrança registrados, eliminando a necessidade de processamento dos tradicionais arquivos de remessa e retorno.

Assim, as seguintes ações devem ser realizadas de acordo com cada tipo de requisição citada acima:

1. Boleto registrado com sucesso:

* Alterar a situação do documento de cobrança de _previsto_ para _aberto_
  
2. Boleto com registro rejeitado:

* Alterar a situação do documento de cobrança de _previsto_ para _erro_
  
3. Boleto baixado no banco (boleto cancelado):

* Alterar a situação do documento de cobrança de _aberto_ para _cancelado_
  
4. Boleto alterado após registro

* Alterar a situação do documento de cobrança de _aberto_alterado_ para _aberto_

Obs.: Neste caso pode-se ignorar a requisição de webhook quando o campo _registro_sistema_bancario_ estiver false.

1. Boleto pago pelo sacado:

* Alterar a situação do documento de cobrança de _aberto_ para _quitado_

6. Boleto pago mais de uma vez pelo sacado:

* Gravar documento de reembolso ao sacado já em situação _aberto_

##### Webhook Conta Digital

Recebendo informações a respeito dos eventos referentes às movimentações sobre uma conta corrente digital.

Este tipo de webhook conta com uma grande diversidade de eventos, no entanto, a maior parte destes não é interessante para efetivar a conciliação bancária de modo automático. Assim, a seguir apenas os eventos de interesse imediato serão esclarecidos.

Por fim, a diferenciação entre os eventos se faz pelo verbo HTTP utilizado, e pelo valor do campo _tipo_, mesmo que todos sejam realizados sobre uma mesma rota. Portanto, este webhook será apresentado dividido de acordo com os métodos e tipos desejados com respeito as transações (pagamentos ou transferências) previamente enviadas ao banco.

* **Endpoint:** {base_url}/api/{tenant}/pjbank/conta_digital
  * Exemplo: http://financeiro.nasajon.com.br/gednasajon/pjbank/conta_digital
* **Parâmetros da URL:**
  * tenant: Identificador do tenant do cliente

1. Criação de uma transação (por meio do bankline direto, isto é, uma movimentação não originada do ERP):
   
* **Método HTTP:** POST
* **Corpo da requisição:**
```json
{
  "operacao" : "POST",
  "tipo" : "transacao",
  "id_operacao" : 1000000003238,
  "nome_favorecido" : "Favorecido Exemplo",
  "cnpj_favorecido" : "teste",
  "valor" : 10.50,
  "data_pagamento" : "09/1/2017", 
  "identificador" : 123123, 
  "historico" : "Teste",
  "status_pagamento" : "pendente_autorizacao",
  "credencial" : "eb2a********************************4164",
  "chave" : "a834********************************a32c",
   "documento" : [
        {
          "url" : "https://example.com.br/234234",
          "tipo" : [boleto, fatura, notafiscal, comprovante, outros],
          "nome": "NotaExemplo.pdf",
          "formato": [jpeg, png, pdf],
          "status": [excluido, ativo] //caso o documento tenha sido excluído, o status é alterado
        }
      ]
}
```
* __Ação do ERP__: Enfileirar a transação bancária como uma pendência para o ERP, pois a mesma precisa ser ligada a uma transação do ERP.

2. Atualização de uma transação (quanto ao situaçao da mesma, principalmente):

* **Método HTTP:** PUT
* **Corpo da requisição:**
```json
{
	"operacao": "PUT",
	"tipo": "transacao",
	"id_operacao": 1000000003238,
	"nome_favorecido": "Favorecido Exemplo",
	"cnpj_favorecido": "10467547000155",
	"banco_favorecido": "",
	"agencia_favorecido": "",
	"conta_favorecido": "",
	"codigo_barras": "03399699255873781001843279301014571980000001000",
	"valor": "1.00",
	"data_pagamento": "09/1/2017",
	"data_vencimento": "09/1/2017",
	"identificador": "",
	"mensagem": "Teste",
	"historico": "Teste",
	"status_pagamento": [realizada, com_erro, agendada, processando, nao_realizada, pendente_autorizacao, rejeitada],
	"credencial": "eb2a********************************4164",
	"chave": "a834********************************a32c",
	"documento" : [
        {
          "url" : "https://example.com.br/234234",
          "tipo" : [boleto, fatura, notafiscal, comprovante, outros],
          "nome": "NotaExemplo.pdf",
          "formato": "application/pdf",
          "status": [excluido, ativo]
        }
      ]
}
```
* __Ação do ERP__: Atualizar situação do documento no diário unico.
  
3. Cancelamento de uma transação:

* **Método HTTP:** DELETE
* **Corpo da requisição:**
```json
{
  "operacao" : "DELETE",
  "tipo" : "transacao",
  "id_operacao" : 1000000003238,
  "identificador" : 123123,
  "credencial" : "eb2a********************************4164",
  "chave" : "a834********************************a32c"
}
```
* __Ação do ERP__: Atualizar situação do documento no diário unico, e lançar uma transação de estorno da original cancelada.

4. Adicionado um documento a uma transação (por fora do ERP):

* **Método HTTP:** PUT
* **Corpo da requisição:**
```json
{
  "operacao" : "PUT",
  "tipo" : "transacao_documento",
  "id_operacao" : 1000000003238,
  "identificador" : 123123, 
  "credencial" : "eb2a********************************4164",
  "chave" : "a834********************************a32c",
  "documento" : [
    {
      "url" : "https://example.com.br/234234",
      "tipo" : [boleto, fatura, notafiscal, comprovante, outros],
      "nome": "NotaExemplo.pdf",
      "formato": [jpeg, png, pdf],
      "status": [excluido, ativo]
    }
  ]
}
```
* __Ação do ERP__: Vincular nova URL ao documento correspondente no diário unico.

5. Removendo um documento de uma transação (por fora do ERP):

* **Método HTTP:** DELETE
* **Corpo da requisição:**
```json
{
  "operacao" : "DELETE",
  "tipo" : "transacao_documento",
  "id_operacao" : 1000000003238,
  "identificador" : 123123, 
  "credencial" : "eb2a********************************4164",
  "chave" : "a834********************************a32c",
  "documento" : [
    {
      "url" : "https://example.com.br/234234",
      "tipo" : [boleto, fatura, notafiscal, comprovante, outros],
      "nome": "NotaExemplo.pdf",
      "formato": [jpeg, png, pdf],
      "status": [excluido, ativo]
    }
  ]
} 
```
* __Ação do ERP__: IGNORAR

6. Nova transferência entre contas (ou sub-contas):

* **Método HTTP:** POST
* **Corpo da requisição:**
```json
{
  "operacao" : "POST",
  "tipo" : "transferencia",
  "id_operacao" : 1000000003238,
  "valor" : 10.50,
  "data_pagamento" : "09/1/2017", 
  "identificador" : 123123, 
  "historico" : "Teste",
  "credencial" : "eb2a********************************4164",
  "chave" : "a834********************************a32c",
  "status_pagamento" : "pendente_autorizacao",
  "subconta_origem" : "f31cb9c07fbc3bf6f7f4291ac3f1793c6f7f798d", // "subconta_destino" : "f31cb9c07fbc3bf6f7f4291ac3f1793c6f7f798d"
}
```
* __Ação do ERP__: Enfileirar a tranferência como uma pendência para o ERP, pois a mesma precisa ser ligada a uma transação do ERP.

7. Edição dos dados cadastrais da conta digital:

* **Método HTTP:** PUT
* **Corpo da requisição:**
```json
{
  "operacao":"PUT",
  "tipo":"conta_digital",
  "codigo":"6540",
  "credencial":"eb2a********************************4164",
  "chave":"a834********************************a32c",
  "nome":"NOME EMPRESA",
  "cnpj":"41531421000126",
  "email":"email@teste.com",
  "telefone":"",
  "identificador":"18022",
  "status":"ativo",
  "endereco_logradouro":"Rua José dos Santos, 146",
  "endereco_numero":"146",
  "endereco_complemento":"",
  "endereco_bairro":"Jardim Aurélia",
  "endereco_cidade":"Campinas",
  "endereco_estado":"SP",
  "endereco_cep":"13033090",
  "data_criacao":"0000-00-00 00:00:00",
  "data_aprovacao":"04/10/2019 09:55:55",
  "data_bloqueio":"0000-00-00 00:00:00",
  "agencia" : "001", // exemplo
  "conta" : "001", // exemplo
  "banco" : "301"
}
```
* __Ação do ERP__: Atualizar cadastro da conta financeira no ERP.