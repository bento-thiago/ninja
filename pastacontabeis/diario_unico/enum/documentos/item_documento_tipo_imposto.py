import enum
from diario_unico.entity.confins_retido_acumulado import CONFINSRetidoAcumulado
from diario_unico.entity.csll_retido_acumulado import CSLLRetidoAcumulado
from diario_unico.entity.icms_retido_acumulado import ICMSRetidoAcumulado
from diario_unico.entity.irrf_retido_acumulado import IRRFRetidoAcumulado
from diario_unico.entity.iss_retido_acumulado import ISSRetidoAcumulado
from diario_unico.entity.pis_retido_acumulado import PISRetidoAcumulado

class ItemDocumentoTipoImposto(enum.Enum):
    COFINS = {"codigo": "COFINS", "campos": ["cofins_retido_original", "cofins_retido",
                                             "base_cofins_retido_original", "base_cofins_retido", "aliquota_cofins_retido"], "type_acumulado": CONFINSRetidoAcumulado}
    CSLL = {"codigo": "CSLL", "campos": ["csll_retido_original", "csll_retido",
                                         "base_csll_retido_original", "base_csll_retido", "aliquota_csll_retido"], "type_acumulado": CSLLRetidoAcumulado}
    ICMS = {"codigo": "ICMS", "campos": ["icms_retido_original", "icms_retido",
                                         "base_icms_retido_original", "base_icms_retido", "aliquota_icms_retido"], "type_acumulado": ICMSRetidoAcumulado}
    IRRF = {"codigo": "IRRF", "campos": ["irrf_retido_original", "irrf_retido",
                                         "base_irrf_retido_original", "base_irrf_retido", "aliquota_irrf_retido"], "type_acumulado": IRRFRetidoAcumulado}
    ISS = {"codigo": "ISS", "campos": ["iss_retido_original", "iss_retido",
                                       "base_iss_retido_original", "base_iss_retido", "aliquota_iss_retido"], "type_acumulado": ISSRetidoAcumulado}
    PIS = {"codigo": "PIS", "campos": ["pis_retido_original", "pis_retido",
                                       "base_pis_retido_original", "base_pis_retido", "aliquota_pis_retido"], "type_acumulado": PISRetidoAcumulado}
