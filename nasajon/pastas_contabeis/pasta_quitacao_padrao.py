from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from nasajon.entity.definicao_info_cobranca import DefinicaoInfoCobranca
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from diario_unico.entity.pagamento import Pagamento
from typing import List
from nasajon.util.lancamento_util import LancamentosUtil
from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from diario_unico.util.diario_factory import DiarioUnicoFactory


class PastaQuitacaoPadrao:
    def get_dados_quitacao_padrao(self, dados: dict):
        """
        Implementação padrão de tratamento de dados para a quitacao de um documento
        """
        return dados

    def quitar_padrao(self, dados: dict):
        """
        Implementação padrão de quitacao de um documento
        """

        if not hasattr(self, '_diario_util'):
            self._diario_util = DiarioUtil()

        dados["pagamento"] = ObjetosUtils().dictToObject(
            dados["pagamento"], Pagamento)
        dados["documento"] = ObjetosUtils().dictToObject(
            dados["documento"], Documento)

        definicoes_lancamentos = self.get_definicoes_lancamentos_quitacao()
        definicao_info_pagamento = self.get_definicao_info_pagamento_quitacao()
        definicao_info_cobranca = self.get_definicao_info_cobranca_quitacao()

        documento: Documento = dados["documento"]
        pagamento: Pagamento = dados["pagamento"]
        dados_cobranca = DiarioUnicoFactory.getCobrancasService().getDadosCobranca(
            dados["tenant"], documento.participante)
        for item in documento.itens:
            params = JsonUtil().toDict(item)
            params["data_pagamento"] = pagamento.data_pagamento
            params["participante"] = documento.participante
            params["texto_instrucao"] = ''
            params["dados_cobranca"] = dados_cobranca
            item.lancamentos = LancamentosUtil().criar_lancamentos(
                params, definicoes_lancamentos, definicao_info_pagamento, definicao_info_cobranca)

        documento.situacao = Situacao.QUITADO
        self._diario_util.quitar_documento(dados["tenant"], documento)
        return documento

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        # A ser implementado pela subclasse
        return list()

    def get_definicao_info_cobranca_quitacao(self) -> DefinicaoInfoCobranca:
        # A ser implementado pela subclasse
        return DefinicaoInfoCobranca()

    def get_definicao_info_pagamento_quitacao(self) -> DefinicaoInfoPagamento:
        # A ser implementado pela subclasse
        return DefinicaoInfoPagamento()
