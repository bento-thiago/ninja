from nasajon.util.projecao_util import ProjecaoUtil

from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo

import datetime
import os
import unittest
from nasajon.pastas_contabeis.pastas_router import get_pasta_obj
from nasajon.pastas_contabeis.pasta_conta_energia_eletrica import PastaContaEnergiaEletrica
from nasajon.pastas_contabeis.pasta_conta_agua import PastaContaAgua


class TestPastasRouter(unittest.TestCase):
    def test_get_pasta_obj(self):
        pasta = get_pasta_obj('conta_energia_eletrica')
        self.assertEqual(pasta.__class__, PastaContaEnergiaEletrica)
        self.assertEqual(pasta.documento_tipo, DocumentoTipo.CONTA_ENERGIA)

    def test_get_pasta_obj_agua(self):
        pasta = get_pasta_obj('conta_agua')
        self.assertEqual(pasta.__class__, PastaContaAgua)
        self.assertEqual(pasta.documento_tipo,
                         DocumentoTipo.CONTA_AGUA_E_ESGOTO)


if __name__ == '__main__':
    unittest.main()
