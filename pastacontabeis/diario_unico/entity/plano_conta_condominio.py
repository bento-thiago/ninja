from diario_unico.entity.conta_contabil import ContaContabil, GrupoContaContabil
from diario_unico.enum.contas_contabeis.conta_contabil_natureza import ContaContabilNatureza

import enum


class PlanoContasCondominio(enum.Enum):
    CC_1 = ContaContabil("1", ContaContabilNatureza.D, "ATIVO",
                         GrupoContaContabil.ATIVO, None)
    CC_1_1 = ContaContabil("1.1", ContaContabilNatureza.D, "ATIVO CIRCULANTE",
                           GrupoContaContabil.ATIVO, "1")
    CC_1_1_1 = ContaContabil("1.1.1", ContaContabilNatureza.D,
                             "DISPONIBILIDADES", GrupoContaContabil.ATIVO, "1.1")
    CC_1_1_1_01 = ContaContabil("1.1.1.01", ContaContabilNatureza.D,
                                "CAIXA GERAL", GrupoContaContabil.ATIVO, "1.1.1")
    CC_1_1_1_02 = ContaContabil(
        "1.1.1.02", ContaContabilNatureza.D, "BANCOS C/ MOVIMENTO", GrupoContaContabil.ATIVO, "1.1.1")
    CC_1_1_1_03 = ContaContabil(
        "1.1.1.03", ContaContabilNatureza.D, "APLICAÇÕES DE LIQUIDEZ IMEDIATA", GrupoContaContabil.ATIVO, "1.1.1")
    CC_1_1_2 = ContaContabil(
        "1.1.2", ContaContabilNatureza.D, "CRÉDITOS E VALORES", GrupoContaContabil.ATIVO, "1.1")
    CC_1_1_2_01 = ContaContabil(
        "1.1.2.01", ContaContabilNatureza.D, "COTAS CONDOMINIAIS A RECEBER", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_1_2_02 = ContaContabil(
        "1.1.2.02", ContaContabilNatureza.D, "COTAS CONDOMINIAIS EM ATRASO", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_1_2_03 = ContaContabil(
        "1.1.2.03", ContaContabilNatureza.D, "COTAS EXTRAS CONDOMINIAIS A RECEBER", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_1_2_04 = ContaContabil(
        "1.1.2.04", ContaContabilNatureza.D, "COTAS EXTRAS CONDOMINIAIS EM ATRASO", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_1_2_08 = ContaContabil(
        "1.1.2.08", ContaContabilNatureza.C, "(-) PERDAS ESTIMADAS C/ CRÉDITOS", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_1_2_09 = ContaContabil(
        "1.1.2.09", ContaContabilNatureza.C, "(-) CRÉDITOS BAIXADOS", GrupoContaContabil.ATIVO, "1.1.2")
    CC_1_2 = ContaContabil(
        "1.2", ContaContabilNatureza.D, "ATIVO NÃO CIRCULANTE", GrupoContaContabil.ATIVO, "1")
    CC_1_2_1 = ContaContabil(
        "1.2.1", ContaContabilNatureza.D, "REALIZÁVEL A LONGO PRAZO", GrupoContaContabil.ATIVO, "1.2")
    CC_1_2_2 = ContaContabil("1.2.2", ContaContabilNatureza.D,
                             "INVESTIMENTOS", GrupoContaContabil.ATIVO, "1.2")
    CC_1_2_2_01 = ContaContabil(
        "1.2.2.01", ContaContabilNatureza.D, "SISTEMA FINANCEIRO NACIONAL", GrupoContaContabil.ATIVO, "1.2.2")
    CC_1_2_3 = ContaContabil("1.2.3", ContaContabilNatureza.D,
                             "IMOBILIZADO", GrupoContaContabil.ATIVO, "1.2")
    CC_1_2_3_03 = ContaContabil("1.2.3.03", ContaContabilNatureza.D,
                                "INSTALAÇÕES", GrupoContaContabil.ATIVO, "1.2.3")
    CC_1_2_3_09 = ContaContabil(
        "1.2.3.09", ContaContabilNatureza.C, "(-) DEPRECIAÇÕES ACUMULADAS", GrupoContaContabil.ATIVO, "1.2.3")
    CC_1_3 = ContaContabil("1.3", ContaContabilNatureza.D, "ATIVO COMPENSADO",
                           GrupoContaContabil.ATIVO, "1")
    CC_1_3_1 = ContaContabil(
        "1.3.1", ContaContabilNatureza.D, "CONTAS DE COMPENSAÇÃO DO ATIVO", GrupoContaContabil.ATIVO, "1.3")
    CC_2 = ContaContabil("2", ContaContabilNatureza.C, "PASSIVO",
                         GrupoContaContabil.PASSIVO, None)
    CC_2_1 = ContaContabil(
        "2.1", ContaContabilNatureza.C, "PASSIVO CIRCULANTE", GrupoContaContabil.PASSIVO, "2")
    CC_2_1_1 = ContaContabil(
        "2.1.1", ContaContabilNatureza.C, "EMPRÉSTIMOS E FINANCIAMENTOS", GrupoContaContabil.PASSIVO, "2.1")
    CC_2_1_1_01 = ContaContabil(
        "2.1.1.01", ContaContabilNatureza.C, "BANCOS C/ EMPRÉSTIMOS", GrupoContaContabil.PASSIVO, "2.1.1")
    CC_2_1_1_02 = ContaContabil(
        "2.1.1.02", ContaContabilNatureza.C, "BANCOS C/ FINANCIAMENTOS", GrupoContaContabil.PASSIVO, "2.1.1")
    CC_2_1_2 = ContaContabil(
        "2.1.2", ContaContabilNatureza.C, "OBRIGAÇÕES SOCIAIS", GrupoContaContabil.PASSIVO, "2.1")
    CC_2_1_2_01 = ContaContabil(
        "2.1.2.01", ContaContabilNatureza.C, "OBRIGAÇÕES PREVIDENCIÁRIAS", GrupoContaContabil.PASSIVO, "2.1.2")
    CC_2_1_2_01_0001 = ContaContabil(
        "2.1.2.01.0001", ContaContabilNatureza.C, "INSS A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.01")
    CC_2_1_2_01_0002 = ContaContabil(
        "2.1.2.01.0002", ContaContabilNatureza.C, "FGTS A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.01")
    CC_2_1_2_02 = ContaContabil(
        "2.1.2.02", ContaContabilNatureza.C, "OBRIGAÇÕES TRIBUTÁRIAS", GrupoContaContabil.PASSIVO, "2.1.2")
    CC_2_1_2_02_0001 = ContaContabil(
        "2.1.2.02.0001", ContaContabilNatureza.C, "CONTRIBUIÇÃO CONFEDERATIVA A PAGAR", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0002 = ContaContabil(
        "2.1.2.02.0002", ContaContabilNatureza.C, "CONTRIBUIÇÃO SINDICAL A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0003 = ContaContabil(
        "2.1.2.02.0003", ContaContabilNatureza.C, "IMPOSTO DE RENDA RETIDO NA FONTE A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0004 = ContaContabil(
        "2.1.2.02.0004", ContaContabilNatureza.C, "PIS S/ FOLHA A PAGAR", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0005 = ContaContabil(
        "2.1.2.02.0005", ContaContabilNatureza.C, "PIS RETIDO A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0006 = ContaContabil(
        "2.1.2.02.0006", ContaContabilNatureza.C, "COFINS RETIDO A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0007 = ContaContabil(
        "2.1.2.02.0007", ContaContabilNatureza.C, "CSLL RETIDO A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0008 = ContaContabil(
        "2.1.2.02.0008", ContaContabilNatureza.C, "ISS RETIDO A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_02_0009 = ContaContabil(
        "2.1.2.02.0009", ContaContabilNatureza.C, "ICMS RETIDO A RECOLHER", GrupoContaContabil.PASSIVO, "2.1.2.02")
    CC_2_1_2_03 = ContaContabil(
        "2.1.2.03", ContaContabilNatureza.C, "OBRIGAÇÕES TRABALHISTAS", GrupoContaContabil.PASSIVO, "2.1.2")
    CC_2_1_2_03_0001 = ContaContabil(
        "2.1.2.03.0001", ContaContabilNatureza.C, "13.º SALÁRIOS A PAGAR", GrupoContaContabil.PASSIVO, "2.1.2.03")
    CC_2_1_2_03_0002 = ContaContabil(
        "2.1.2.03.0002", ContaContabilNatureza.C, "FÉRIAS A PAGAR", GrupoContaContabil.PASSIVO, "2.1.2.03")
    CC_2_1_2_03_0003 = ContaContabil(
        "2.1.2.03.0003", ContaContabilNatureza.C, "SALÁRIOS E ORDENADOS A PAGAR", GrupoContaContabil.PASSIVO, "2.1.2.03")
    CC_2_1_2_04 = ContaContabil(
        "2.1.2.04", ContaContabilNatureza.C, "FORNECEDORES", GrupoContaContabil.PASSIVO, "2.1.2")
    CC_2_1_3 = ContaContabil(
        "2.1.3", ContaContabilNatureza.C, "PROVISÕES P/ CONTINGÊNCIAS", GrupoContaContabil.PASSIVO, "2.1")
    CC_2_1_3_01 = ContaContabil(
        "2.1.3.01", ContaContabilNatureza.C, "PROVISÕES DE 13.º SALÁRIOS", GrupoContaContabil.PASSIVO, "2.1.3")
    CC_2_1_3_01_0001 = ContaContabil(
        "2.1.3.01.0001", ContaContabilNatureza.C, "PROVISÃO DE 13.º SALÁRIOS A PAGAR", GrupoContaContabil.PASSIVO, "2.1.3.01")
    CC_2_1_3_01_0002 = ContaContabil(
        "2.1.3.01.0002", ContaContabilNatureza.C, "PROVISÃO DO FGTS A PAGAR S/ 13.º SALÁRIOS", GrupoContaContabil.PASSIVO, "2.1.3.01")
    CC_2_1_3_01_0003 = ContaContabil(
        "2.1.3.01.0003", ContaContabilNatureza.C, "PROVISÃO DO INSS A PAGAR S/ 13.º SALÁRIOS", GrupoContaContabil.PASSIVO, "2.1.3.01")
    CC_2_1_3_02 = ContaContabil(
        "2.1.3.02", ContaContabilNatureza.C, "PROVISÕES DE FÉRIAS", GrupoContaContabil.PASSIVO, "2.1.3")
    CC_2_1_3_02_0001 = ContaContabil(
        "2.1.3.02.0001", ContaContabilNatureza.C, "PROVISÃO DE FÉRIAS A PAGAR", GrupoContaContabil.PASSIVO, "2.1.3.02")
    CC_2_1_3_02_0002 = ContaContabil(
        "2.1.3.02.0002", ContaContabilNatureza.C, "PROVISÃO DO FGTS A PAGAR S/ FÉRIAS", GrupoContaContabil.PASSIVO, "2.1.3.02")
    CC_2_1_3_02_0003 = ContaContabil(
        "2.1.3.02.0003", ContaContabilNatureza.C, "PROVISÃO DO INSS A PAGAR S/ FÉRIAS", GrupoContaContabil.PASSIVO, "2.1.3.02")
    CC_2_2 = ContaContabil(
        "2.2", ContaContabilNatureza.C, "PASSIVO NÃO CIRCULANTE", GrupoContaContabil.PASSIVO, "2")
    CC_2_2_1 = ContaContabil(
        "2.2.1", ContaContabilNatureza.C, "EXIGÍVEL A LONGO PRAZO", GrupoContaContabil.PASSIVO, "2.2")
    CC_2_3 = ContaContabil(
        "2.3", ContaContabilNatureza.C, "PATRIMÔNIO LÍQUIDO", GrupoContaContabil.PASSIVO, "2")
    CC_2_3_1 = ContaContabil(
        "2.3.1", ContaContabilNatureza.C, "PATRIMÔNO SOCIAL", GrupoContaContabil.PASSIVO, "2.3")
    CC_2_3_1_01 = ContaContabil(
        "2.3.1.01", ContaContabilNatureza.C, "BENS PATRIMONIAIS", GrupoContaContabil.PASSIVO, "2.3.1")
    CC_2_3_1_02 = ContaContabil(
        "2.3.1.02", ContaContabilNatureza.C, "SUPERÁVIT PATRIMONIAL", GrupoContaContabil.PASSIVO, "2.3.1")
    CC_2_3_1_03 = ContaContabil(
        "2.3.1.03", ContaContabilNatureza.D, "(-) DÉFICIT PATRIMONIAL", GrupoContaContabil.PASSIVO, "2.3.1")
    CC_2_3_2 = ContaContabil(
        "2.3.2", ContaContabilNatureza.C, "FUNDOS DE RESERVA", GrupoContaContabil.PASSIVO, "2.3")
    CC_2_3_2_01 = ContaContabil(
        "2.3.2.01", ContaContabilNatureza.C, "FUNDO DE RESERVA P/ CONTINGÊNCIAS", GrupoContaContabil.PASSIVO, "2.3.2")
    CC_2_3_2_02 = ContaContabil(
        "2.3.2.02", ContaContabilNatureza.C, "FUNDO DE RESERVA P/ INDENIZAÇÕES TRABALHISTAS", GrupoContaContabil.PASSIVO, "2.3.2")
    CC_2_4 = ContaContabil(
        "2.4", ContaContabilNatureza.C, "PASSIVO COMPENSADO", GrupoContaContabil.PASSIVO, "2")
    CC_2_4_1 = ContaContabil(
        "2.4.1", ContaContabilNatureza.C, "CONTAS DE COMPENSAÇÃO DO PASSIVO", GrupoContaContabil.PASSIVO, "2.4")
    CC_3 = ContaContabil(
        "3", ContaContabilNatureza.D, "CONTAS DE RESULTADOS CREDORAS", GrupoContaContabil.RECEITAS, None)
    CC_3_1 = ContaContabil("3.1", ContaContabilNatureza.D, "RECEITAS",
                           GrupoContaContabil.RECEITAS, "3")
    CC_3_1_1 = ContaContabil(
        "3.1.1", ContaContabilNatureza.C, "RECEITAS CONDOMINIAIS", GrupoContaContabil.RECEITAS, "3.1")
    CC_3_1_1_01 = ContaContabil(
        "3.1.1.01", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_02 = ContaContabil(
        "3.1.1.02", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - ENERGIA ELÉTRICA", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_03 = ContaContabil(
        "3.1.1.03", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - ÁGUA E ESGOTO", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_04 = ContaContabil(
        "3.1.1.04", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - GÁS", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_05 = ContaContabil(
        "3.1.1.05", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - MULTAS", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_06 = ContaContabil(
        "3.1.1.06", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - FUNDO DE OBRA", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_07 = ContaContabil(
        "3.1.1.07", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - FUNDO DE RESERVA", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_08 = ContaContabil(
        "3.1.1.08", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - GARAGEM", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_1_09 = ContaContabil(
        "3.1.1.09", ContaContabilNatureza.C, "RECEITA DE COTAS CONDOMINIAIS - OUTRAS RECEITAS", GrupoContaContabil.RECEITAS, "3.1.1")
    CC_3_1_2 = ContaContabil(
        "3.1.2", ContaContabilNatureza.D, "RECEITAS FINANCEIRAS", GrupoContaContabil.RECEITAS, "3.1")
    CC_3_1_2_01 = ContaContabil(
        "3.1.2.01", ContaContabilNatureza.D, "RECEITAS DE MULTA E ACRÉSCIMOS MORATÓRIOS", GrupoContaContabil.RECEITAS, "3.1.2")
    CC_3_1_2_02 = ContaContabil(
        "3.1.2.02", ContaContabilNatureza.D, "RENDAS DE INVESTIMENTOS TEMPORÁRIOS NO SFN (sistema financeiro de habitação)", GrupoContaContabil.RECEITAS, "3.1.2")
    CC_3_1_2_03 = ContaContabil(
        "3.1.2.03", ContaContabilNatureza.D, "LUCRO NA VENDA DE INVESTIMENTOS TEMPORÁRIOS", GrupoContaContabil.RECEITAS, "3.1.2")
    CC_4 = ContaContabil(
        "4", ContaContabilNatureza.D, "CONTAS DE RESULTADO DEVEDORAS", GrupoContaContabil.DESPESAS, None)
    CC_4_1 = ContaContabil("4.1", ContaContabilNatureza.D, "DESPESAS",
                           GrupoContaContabil.DESPESAS, "4")
    CC_4_1_1 = ContaContabil(
        "4.1.1", ContaContabilNatureza.D, "DESPESAS CONDOMINIAIS", GrupoContaContabil.DESPESAS, "4.1")
    CC_4_1_1_01 = ContaContabil(
        "4.1.1.01", ContaContabilNatureza.D, "DESPESAS C/ SALÁRIOS E ENCARGOS SOCIAIS DOS EMPREGADOS", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_01_0001 = ContaContabil(
        "4.1.1.01.0001", ContaContabilNatureza.D, "ADICIONAL NOTURNO", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0002 = ContaContabil(
        "4.1.1.01.0002", ContaContabilNatureza.D, "ANUÊNIO", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0003 = ContaContabil(
        "4.1.1.01.0003", ContaContabilNatureza.D, "ASSISTÊNCIA MÉDICA E SOCIAL", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0004 = ContaContabil(
        "4.1.1.01.0004", ContaContabilNatureza.D, "ASSISTÊNCIA ODONTOLÓGICA", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0005 = ContaContabil(
        "4.1.1.01.0005", ContaContabilNatureza.D, "AVISO PRÉVIO E OUTRAS INDENIZAÇÕES TRABALHISTAS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0006 = ContaContabil(
        "4.1.1.01.0006", ContaContabilNatureza.D, "DESCANSO SEMANAL REMUNERADO (DSR)", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0007 = ContaContabil(
        "4.1.1.01.0007", ContaContabilNatureza.D, "EQUIPAMENTOS DE PROTEÇÃO INDIVIDUAL - EPI", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0008 = ContaContabil(
        "4.1.1.01.0008", ContaContabilNatureza.D, "FARMÁCIA E MEDICAMENTOS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0009 = ContaContabil(
        "4.1.1.01.0009", ContaContabilNatureza.D, "FÉRIAS C/ ABONO", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0010 = ContaContabil(
        "4.1.1.01.0010", ContaContabilNatureza.D, "FUNDO DE GARANTIA DO TEMPO DE SERVIÇO - FGTS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0011 = ContaContabil(
        "4.1.1.01.0011", ContaContabilNatureza.D, "GRATIFICAÇÃO NATALINA (13.º SALÁRIOS)", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0012 = ContaContabil(
        "4.1.1.01.0012", ContaContabilNatureza.D, "HORAS EXTRAS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0013 = ContaContabil(
        "4.1.1.01.0013", ContaContabilNatureza.D, "INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0014 = ContaContabil(
        "4.1.1.01.0014", ContaContabilNatureza.D, "PROGRAMA DE ALIMENTAÇÃO DO TRABALHADOR - PAT", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0015 = ContaContabil(
        "4.1.1.01.0015", ContaContabilNatureza.D, "SALÁRIOS E ORDENADOS", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0016 = ContaContabil(
        "4.1.1.01.0016", ContaContabilNatureza.D, "UNIFORMES", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_01_0017 = ContaContabil(
        "4.1.1.01.0017", ContaContabilNatureza.D, "VALE TRANSPORTE - VT", GrupoContaContabil.DESPESAS, "4.1.1.01")
    CC_4_1_1_02 = ContaContabil(
        "4.1.1.02", ContaContabilNatureza.D, "DESPESAS DE ADMINISTRAÇÃO DO CONDOMÍNIO", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_03 = ContaContabil(
        "4.1.1.03", ContaContabilNatureza.D, "DESPESAS C/ PRESTAÇÃO DE SERVIÇOS", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_04 = ContaContabil(
        "4.1.1.04", ContaContabilNatureza.D, "DESPESAS C/ SEGUROS", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_04_0001 = ContaContabil(
        "4.1.1.04.0001", ContaContabilNatureza.D, "SEGURO DE ACIDENTE DE TRABALHO", GrupoContaContabil.DESPESAS, "4.1.1.04")
    CC_4_1_1_04_0002 = ContaContabil(
        "4.1.1.04.0002", ContaContabilNatureza.D, "SEGURO DE VIDA EM GRUPO", GrupoContaContabil.DESPESAS, "4.1.1.04")
    CC_4_1_1_05 = ContaContabil(
        "4.1.1.05", ContaContabilNatureza.D, "DESPESAS C/ LIMPEZA E CONSERVAÇÃO", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_05_0001 = ContaContabil(
        "4.1.1.05.0001", ContaContabilNatureza.D, "HIGIÊNE E LIMPEZA", GrupoContaContabil.DESPESAS, "4.1.1.05")
    CC_4_1_1_06 = ContaContabil(
        "4.1.1.06", ContaContabilNatureza.D, "DESPESAS C/ MANUTENÇÃO E CONSERVAÇÃO DE EQUIPAMENTOS", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_07 = ContaContabil(
        "4.1.1.07", ContaContabilNatureza.D, "DESPESAS DE ÁGUA E ESGOTO", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_07_0001 = ContaContabil(
        "4.1.1.07.0001", ContaContabilNatureza.D, "CONSUMO DE ÁGUA", GrupoContaContabil.DESPESAS, "4.1.1.07")
    CC_4_1_1_08 = ContaContabil(
        "4.1.1.08", ContaContabilNatureza.D, "DESPESAS DE LUZ, GÁS, TELEFONE, ANTENA COLETIVA", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_08_0001 = ContaContabil(
        "4.1.1.08.0001", ContaContabilNatureza.D, "COMUNICAÇÕES TELEFÔNICAS", GrupoContaContabil.DESPESAS, "4.1.1.08")
    CC_4_1_1_08_0002 = ContaContabil(
        "4.1.1.08.0002", ContaContabilNatureza.D, "CONSUMO DE ENERGIA ELÉTRICA", GrupoContaContabil.DESPESAS, "4.1.1.08")
    CC_4_1_1_08_0003 = ContaContabil(
        "4.1.1.08.0003", ContaContabilNatureza.D, "CONSUMO DE GÁS", GrupoContaContabil.DESPESAS, "4.1.1.08")
    CC_4_1_1_08_0004 = ContaContabil(
        "4.1.1.08.0004", ContaContabilNatureza.D, "USO DA ANTENA COLETIVA", GrupoContaContabil.DESPESAS, "4.1.1.08")
    CC_4_1_1_09 = ContaContabil(
        "4.1.1.09", ContaContabilNatureza.D, "DESPESAS C/ IMPOSTOS E TAXAS", GrupoContaContabil.DESPESAS, "4.1.1")
    CC_4_1_1_09_0001 = ContaContabil(
        "4.1.1.09.0001", ContaContabilNatureza.D, "IMPOSTO S/ PROPRIEDADE TERRITORIAL URBANA - IPTU", GrupoContaContabil.DESPESAS, "4.1.1.09")
    CC_4_1_1_09_0002 = ContaContabil(
        "4.1.1.09.0002", ContaContabilNatureza.D, "TAXA DA COLETA DE LIXO", GrupoContaContabil.DESPESAS, "4.1.1.09")
    CC_4_1_1_09_0003 = ContaContabil(
        "4.1.1.09.0003", ContaContabilNatureza.D, "TAXA DE VISTORIA DOS BOMBEIROS", GrupoContaContabil.DESPESAS, "4.1.1.09")
    CC_4_1_2 = ContaContabil(
        "4.1.2", ContaContabilNatureza.D, "DESPESAS FINANCEIRAS E FISCAIS", GrupoContaContabil.DESPESAS, "4.1")
    CC_4_1_2_01 = ContaContabil(
        "4.1.2.01", ContaContabilNatureza.D, "PREJUÍZO NA VENDA DE INVESTIMENTOS TEMPORÁRIOS NO S.F.N.", GrupoContaContabil.DESPESAS, "4.1.2")
    CC_4_1_2_02 = ContaContabil(
        "4.1.2.02", ContaContabilNatureza.D, "JUROS E DESPESAS BANCÁRIAS", GrupoContaContabil.DESPESAS, "4.1.2")
    CC_4_1_2_02_0001 = ContaContabil(
        "4.1.2.02.0001", ContaContabilNatureza.D, "IOF - DÉBITO AUTOMÁTICO", GrupoContaContabil.DESPESAS, "4.1.2.02")
    CC_4_1_2_02_0002 = ContaContabil(
        "4.1.2.02.0002", ContaContabilNatureza.D, "JUROS E COMISSÕES BANCÁRIAS", GrupoContaContabil.DESPESAS, "4.1.2.02")
    CC_4_1_2_03 = ContaContabil(
        "4.1.2.03", ContaContabilNatureza.D, "DESPESAS C/ MULTAS E INFRAÇÕES FISCAIS", GrupoContaContabil.DESPESAS, "4.1.2")
