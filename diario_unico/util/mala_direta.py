import requests
import os
import json
import base64


class MalaDireta:
    def __init__(self):
        # Recuperando as variáveis de ambiente:
        self.url_maladireta = os.getenv(
            "url_maladireta", "http://localhost:82")
        self.api_key = os.getenv(
            "api_key", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaXN0ZW1hIjoiMjc4IiwidGlwbyI6InNpc3RlbWEifQ.M2bk-j65jiMO5iDpZAuSj9zgTpla3JHIST2yUILwVWs")

    """
     * Envia email pelo mala direta
     * 
     * Parâmetros (! = obrigatórios):
     * 
     * -! de (remetente)
     * -! para (array de destinatários)
     * -! template (código do template)
     * - dados (dados adicionais para o layout) 
     * - tenant (tenant solicitante) 
     * - split (se deve enviar um email para cada destinatário separadamente)
     """

    def enviarEmail(self, de: str, para: list, template: str, dados: dict = {}, tenant: str = '', split: bool = False):
        dados_email = {'from': de, 'codigo': template, 'tenant': tenant}

        for i in range(len(para)):
            dados_email['to[{}]'.format(i)] = para[i]

        dados_email = self.ajustarDados(dados_email, dados, 'tags')

        if split:
            dados_email['split'] = 'true'

        response = requests.post(
            self.url_maladireta + '/api/mail/send', data=dados_email, headers={'apikey': self.api_key})

        response.raise_for_status()

        return dados_email

    def ajustarDados(self, dados_email, dados, nome):
        if type(dados) is dict:
            for chave, valor in dados.items():
                dados_email = self.ajustarDados(
                    dados_email, valor, nome + '[{}]'.format(chave))
        elif type(dados) is list:
            for i in range(len(dados)):
                dados_email = self.ajustarDados(
                    dados_email, dados[i], nome + '[{}]'.format(i))
        else:
            dados_email[nome] = dados

        return dados_email
