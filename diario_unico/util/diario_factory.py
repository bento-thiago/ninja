class DiarioUnicoFactory:
    @staticmethod
    def getCobrancasRepository():
        from diario_unico.repository.cobrancas_repository import CobrancasRepository
        return CobrancasRepository()

    @staticmethod
    def getFaturaPrestacaoServicosService():
        from diario_unico.services.fatura_prestacao_servicos_service import FaturaPrestacaoServicosService
        return FaturaPrestacaoServicosService(DiarioUnicoFactory.getDocumentoService(),
                                              DiarioUnicoFactory.getPessoaService())

    @staticmethod
    def getCobrancasService():
        from diario_unico.services.cobrancas_service import CobrancasService
        return CobrancasService(DiarioUnicoFactory.getCobrancasRepository())

    @staticmethod
    def getContratosService():
        from diario_unico.services.contrato_service import ContratoService
        return ContratoService(DiarioUnicoFactory.getContratoRepository(), DiarioUnicoFactory.getUtilitarioService(),
                               DiarioUnicoFactory.getEstabelecimentoRepository(), DiarioUnicoFactory.getPessoaService())

    @staticmethod
    def getContratoRepository():
        from diario_unico.repository.contrato_repository import ContratoRepository
        return ContratoRepository()

    @staticmethod
    def getUtilitarioService():
        from diario_unico.services.utilitario_service import UtilitarioService
        return UtilitarioService(DiarioUnicoFactory.getUtilitarioRepository())

    @staticmethod
    def getPessoaService():
        from diario_unico.services.pessoa_service import PessoaService
        return PessoaService(DiarioUnicoFactory.getPessoasRepository(), DiarioUnicoFactory.getUtilitarioService(),
                             DiarioUnicoFactory.getContatoService(), DiarioUnicoFactory.getEnderecoService())

    @staticmethod
    def getUtilitarioRepository():
        from diario_unico.repository.utilitario_repository import UtilitarioRepository
        return UtilitarioRepository()

    @staticmethod
    def getContatoService():
        from diario_unico.services.contato_service import ContatoService
        return ContatoService(DiarioUnicoFactory.getContatoRepository())

    @staticmethod
    def getEnderecoService():
        from diario_unico.services.endereco_service import EnderecoService
        return EnderecoService(DiarioUnicoFactory.getEnderecoRepository())

    @staticmethod
    def getContatoRepository():
        from diario_unico.repository.contato_repository import ContatoRepository
        return ContatoRepository()

    @staticmethod
    def getEnderecoRepository():
        from diario_unico.repository.endereco_repository import EnderecoRepository
        return EnderecoRepository()

    @staticmethod
    def getPagamentosRepository():
        from diario_unico.repository.pagamentos_repository import PagamentosRepository
        return PagamentosRepository()

    @staticmethod
    def getPagamentosService():
        from diario_unico.services.pagamentos_service import PagamentosService
        return PagamentosService(DiarioUnicoFactory.getPagamentosRepository())

    @staticmethod
    def getDiarioUnicoRepository():
        from diario_unico.repository.diario_unico_repository import DiarioUnicoRepository
        return DiarioUnicoRepository()

    @staticmethod
    def getDiarioUnicoService():
        from diario_unico.services.diario_unico_service import DiarioUnicoService
        return DiarioUnicoService(DiarioUnicoFactory.getDiarioUnicoRepository())

    @staticmethod
    def getUtilRepository():
        from diario_unico.repository.util_repository import UtilRepository
        return UtilRepository()

    @staticmethod
    def getDocumentoRepository():
        from diario_unico.repository.documento_repository import DocumentoRepository
        return DocumentoRepository()

    @staticmethod
    def getEstabelecimentoRepository():
        from diario_unico.repository.estabelecimento_repository import EstabelecimentoRepository
        return EstabelecimentoRepository()

    @staticmethod
    def getPessoasRepository():
        from diario_unico.repository.pessoas_repository import PessoasRepository
        return PessoasRepository()

    @staticmethod
    def getDocumentoService():
        from diario_unico.services.documento_service import DocumentoService
        return DocumentoService(DiarioUnicoFactory.getDocumentoRepository(),
                                DiarioUnicoFactory.getDiarioUnicoService(),
                                DiarioUnicoFactory.getUtilitarioService(),
                                DiarioUnicoFactory.getInfoCobrancaService())

    @staticmethod
    def getEstabelecimentoService():
        from diario_unico.services.estabelecimento_service import EstabelecimentoService
        return EstabelecimentoService(DiarioUnicoFactory.getEstabelecimentoRepository())

    @staticmethod
    def getPlanoContasRepository():
        from diario_unico.repository.plano_contas_repository import PlanoContasRepository
        return PlanoContasRepository()

    @staticmethod
    def getPlanoContasService():
        from diario_unico.services.plano_contas_service import PlanoContasService
        return PlanoContasService(DiarioUnicoFactory.getPlanoContasRepository())

    @staticmethod
    def getInfoCobrancaService():
        from diario_unico.services.info_cobranca_service import InfoCobrancaService
        return InfoCobrancaService(DiarioUnicoFactory.getInfoCobrancaRepository())

    @staticmethod
    def getInfoCobrancaRepository():
        from diario_unico.repository.info_cobranca_repository import InfoCobrancaRepository
        return InfoCobrancaRepository()
