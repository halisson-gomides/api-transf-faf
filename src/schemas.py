from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from datetime import date, datetime


# Template para paginacao
class PaginatedResponseTemplate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    data: List[Any]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int
# --------------------------------------


class EmpenhoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_empenho: Optional[int]
    numero_empenho: Optional[str]
    ano_empenho: Optional[str]
    gestao_emitente_empenho: Optional[str]
    ug_emitente_empenho: Optional[str]
    data_emissao_empenho: Optional[date]
    fonte_recurso_empenho: Optional[str]
    esfera_orcamentaria_empenho: Optional[int]
    descricao_esfera_orcamentaria_empenho: Optional[str]
    plano_interno_empenho: Optional[str]
    unidade_gestora_responsavel_empenho: Optional[str]
    observacao_empenho: Optional[str]
    cnpj_favorecido_empenho: Optional[str]
    numero_lista_empenho: Optional[str]
    unidade_gestora_referencia_empenho: Optional[str]
    gestao_referencia_empenho: Optional[str]
    numero_interno_empenho: Optional[int]
    objeto_empenho: Optional[str]
    numero_sistema_empenho: Optional[str]
    natureza_despesa_empenho: Optional[str]
    natureza_despesa_sub_item_empenho: Optional[int]
    tipo_empenho: Optional[int]
    descricao_tipo_empenho: Optional[str]
    codigo_tipo_nota_empenho: Optional[str]
    descricao_tipo_nota_empenho: Optional[str]
    situacao_empenho: Optional[int]
    descricao_situacao_empenho: Optional[str]
    valor_empenho: Optional[float]
    versao_empenho: Optional[int]
    id_plano_acao: Optional[int]
    

class PaginatedEmpenhoResponse(PaginatedResponseTemplate):
    data: List[EmpenhoResponse]
   

class GestaoFinanceiraCategoriasDespesaResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_categoria_despesa_gestao_financeira: Optional[int]
    id_nivel_pai_categoria_despesa_gestao_financeira: Optional[int]
    nome_nivel_atual_categoria_despesa_gestao_financeira: Optional[str]
    nivel_atual_categoria_despesa_gestao_financeira: Optional[int]
    nome_completo_niveis_categoria_despesa_gestao_financeira: Optional[str]
    codigo_programa_agil: Optional[int]
    nome_programa_agil: Optional[str]


class PaginatedGestaoFinanceiraCategoriasDespesaResponse(PaginatedResponseTemplate):
    data: List[GestaoFinanceiraCategoriasDespesaResponse]
 

class GestaoFinanceiraLancamentosResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_lancamento_gestao_financeira: Optional[int]
    origem_solicitacao_gestao_financeira: Optional[str]
    descricao_origem_solicitacao_gestao_financeira: Optional[str]
    cnpj_ente_solicitante_gestao_financeira: Optional[str]
    nome_ente_solicitante_gestao_financeira: Optional[str]
    nome_personalizado_ente_solicitante_gestao_financeira: Optional[str]
    codigo_programa_agil_ente_solicitante_gestao_financeira: Optional[str]
    codigo_banco_gestao_financeira: Optional[str]
    codigo_agencia_gestao_financeira: Optional[str]
    dv_agencia_gestao_financeira: Optional[str]
    codigo_conta_gestao_financeira: Optional[str]
    dv_conta_gestao_financeira: Optional[str]
    tipo_operacao_gestao_financeira: Optional[str]
    descricao_tipo_operacao_gestao_financeira: Optional[str]
    descricao_gestao_financeira: Optional[str]
    data_lancamento_gestao_financeira: Optional[date]
    data_evento_lancamento_gestao_financeira: Optional[date]
    numero_ordem_gestao_financeira: Optional[int]
    numero_referencia_unica_gestao_financeira: Optional[str]
    tipo_favorecido_gestao_financeira: Optional[int]
    descricao_tipo_favorecido_gestao_financeira: Optional[str]
    doc_favorecido_gestao_financeira_mask: Optional[str]
    nome_favorecido_gestao_financeira: Optional[str]
    codigo_banco_favorecido_gestao_financeira: Optional[str]
    codigo_agencia_favorecido_gestao_financeira: Optional[str]
    dv_agencia_favorecido_gestao_financeira: Optional[str]
    codigo_conta_favorecido_gestao_financeira: Optional[str]
    dv_conta_favorecido_gestao_financeira: Optional[str]
    valor_lancamento_gestao_financeira: Optional[float]
    id_categoria_despesa_gestao_financeira: Optional[int]
    quantidade_subtransacoes_lancamento_gestao_financeira: Optional[int]
    id_agencia_conta: Optional[str]


class PaginatedGestaoFinanceiraLancamentosResponse(PaginatedResponseTemplate):
    data: List[GestaoFinanceiraLancamentosResponse]
 

class GestaoFinanceiraSubtransacoesResponse(BaseModel):    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_subtransacao_gestao_financeira: Optional[str]
    estado_subtransacao_gestao_financeira: Optional[int]
    situacao_pagamento_subtransacao_gestao_financeira: Optional[int]
    descricao_situacao_pagamento_subtransacao_gestao_financeira: Optional[str]
    data_pagamento_subtransacao_gestao_financeira: Optional[date]
    tipo_pessoa_beneficiario_subtransacao_gestao_financeira: Optional[int]
    descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei: Optional[str]
    numero_documento_beneficiario_subtransacao_gestao_financeira_ma: Optional[str]
    nome_beneficiario_subtransacao_gestao_financeira: Optional[str]
    codigo_banco_beneficiario_subtransacao_gestao_financeira: Optional[str]
    codigo_agencia_beneficiario_subtransacao_gestao_financeira: Optional[str]
    codigo_conta_beneficiario_subtransacao_gestao_financeira: Optional[str]
    descricao_subtransacao_gestao_financeira: Optional[str]
    valor_subtransacao_gestao_financeira: Optional[float]
    id_categoria_despesa_gestao_financeira: Optional[int]
    id_lancamento_gestao_financeira: Optional[int]


class PaginatedGestaoFinanceiraSubtransacoesResponse(PaginatedResponseTemplate):
    data: List[GestaoFinanceiraSubtransacoesResponse]


class PlanoAcaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_plano_acao: Optional[int]
    codigo_plano_acao: Optional[str]
    data_inicio_vigencia_plano_acao: Optional[date]
    data_fim_vigencia_plano_acao: Optional[date]
    diagnostico_plano_acao: Optional[str]
    objetivos_plano_acao: Optional[str]
    situacao_plano_acao: Optional[str]
    valor_repasse_emenda_plano_acao: Optional[float]
    valor_repasse_especifico_plano_acao: Optional[float]
    valor_repasse_voluntario_plano_acao: Optional[float]
    valor_total_repasse_plano_acao: Optional[float]
    valor_recursos_proprios_plano_acao: Optional[float]
    valor_outros_plano_acao: Optional[float]
    valor_rendimentos_aplicacao_plano_acao: Optional[float]
    valor_total_plano_acao: Optional[float]
    valor_total_investimento_plano_acao: Optional[float]
    valor_total_custeio_plano_acao: Optional[float]
    valor_saldo_disponivel_plano_acao: Optional[float]
    id_orgao_repassador_plano_acao: Optional[int]
    sigla_orgao_repassador_plano_acao: Optional[str]
    cnpj_orgao_repassador_plano_acao: Optional[str]
    nome_orgao_repassador_plano_acao: Optional[str]
    id_ente_repassador_plano_acao: Optional[int]
    cnpj_ente_repassador_plano_acao: Optional[str]
    nome_ente_repassador_plano_acao: Optional[str]
    uf_ente_repassador_plano_acao: Optional[str]
    nome_municipio_ente_repassador_plano_acao: Optional[str]
    codigo_ibge_municipio_ente_repassador_plano_acao: Optional[int]
    id_ente_recebedor_plano_acao: Optional[int]
    cnpj_ente_recebedor_plano_acao: Optional[str]
    nome_ente_recebedor_plano_acao: Optional[str]
    uf_ente_recebedor_plano_acao: Optional[str]
    nome_municipio_ente_recebedor_plano_acao: Optional[str]
    codigo_ibge_municipio_ente_recebedor_plano_acao: Optional[int]
    id_fundo_repassador_plano_acao: Optional[int]
    cnpj_fundo_repassador_plano_acao: Optional[str]
    nome_fundo_repassador_plano_acao: Optional[str]
    uf_fundo_repassador_plano_acao: Optional[str]
    municipio_fundo_repassador_plano_acao: Optional[str]
    codigo_ibge_fundo_repassador_plano_acao: Optional[int]
    id_fundo_recebedor_plano_acao: Optional[int]
    cnpj_fundo_recebedor_plano_acao: Optional[str]
    nome_fundo_recebedor_plano_acao: Optional[str]
    uf_fundo_recebedor_plano_acao: Optional[str]
    municipio_fundo_recebedor_plano_acao: Optional[str]
    codigo_ibge_fundo_recebedor_plano_acao: Optional[int]
    id_programa: Optional[int]


class PaginatedPlanoAcaoResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoResponse]


class PlanoAcaoAnaliseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_analise_plano_acao: Optional[int]
    tipo_analise_plano_acao: Optional[str]
    tipo_analise_resultado_plano_acao: Optional[str]
    data_analise_plano_acao: Optional[date]
    parecer_analise_plano_acao: Optional[str]
    tipo_origem_analise_plano_acao: Optional[str]
    id_plano_acao: Optional[int]
    id_historico_plano_acao: Optional[int]


class PaginatedPlanoAcaoAnaliseResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoAnaliseResponse]


class PlanoAcaoAnaliseResponsavelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid", populate_by_name=True)
    
    plano_acao_analise_fk: Optional[int] = Field(alias="id_analise_plano_acao")
    nome_responsavel_analise_plano_acao: Optional[str]
    cargo_responsavel_analise_plano_acao: Optional[str]


class PaginatedPlanoAcaoAnaliseResponsavelResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoAnaliseResponsavelResponse]


class PlanoAcaoDadoBancarioResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_plano_acao_dado_bancario: Optional[int]
    id_agencia_conta: Optional[str]
    codigo_banco_plano_acao_dado_bancario: Optional[int]
    nome_banco_plano_acao_dado_bancario: Optional[str]
    numero_agencia_plano_acao_dado_bancario: Optional[int]
    dv_agencia_plano_acao_dado_bancario: Optional[str]
    numero_conta_plano_acao_dado_bancario: Optional[int]
    dv_conta_plano_acao_dado_bancario: Optional[str]
    situacao_conta_plano_acao_dado_bancario: Optional[str]
    data_abertura_conta_plano_acao_dado_bancario: Optional[date]
    nome_programa_agil_conta_plano_acao_dado_bancario: Optional[str]
    saldo_final_conta_plano_acao_dado_bancario: Optional[float]
    id_plano_acao: Optional[int]


class PaginatedPlanoAcaoDadoBancarioResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoDadoBancarioResponse]
 

class PlanoAcaoDestinacaoRecursosResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_destinacao_recursos_plano_acao: Optional[int]
    codigo_natureza_despesa_destinacao_recursos_plano_acao: Optional[str]
    descricao_natureza_despesa_destinacao_recursos_plano_acao: Optional[str]
    tipo_despesa_destinacao_recursos_plano_acao: Optional[str]
    valor_destinacao_recursos_plano_acao: Optional[float]
    id_plano_acao: Optional[int]


class PaginatedPlanoAcaoDestinacaoRecursosResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoDestinacaoRecursosResponse]


class PlanoAcaoHistoricoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_historico_plano_acao: Optional[int]
    situacao_historico_plano_acao: Optional[str]
    data_historico_plano_acao: Optional[date]
    versao_historico_plano_acao: Optional[int]
    id_plano_acao: Optional[int]


class PaginatedPlanoAcaoHistoricoResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoHistoricoResponse]


class PlanoAcaoMetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_meta_plano_acao: Optional[int]
    numero_meta_plano_acao: Optional[str]
    nome_meta_plano_acao: Optional[str]
    descricao_meta_plano_acao: Optional[str]
    valor_meta_plano_acao: Optional[float]
    versao_meta_plano_acao: Optional[int]
    sequencial_meta_plano_acao: Optional[int]
    id_plano_acao: Optional[int]


class PaginatedPlanoAcaoMetaResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoMetaResponse]


class PlanoAcaoMetaAcaoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_acao_meta_plano_acao: Optional[int]
    numero_acao_meta_plano_acao: Optional[str]
    nome_acao_meta_plano_acao: Optional[str]
    descricao_acao_meta_plano_acao: Optional[str]
    valor_acao_meta_plano_acao: Optional[float]
    versao_acao_meta_plano_acao: Optional[int]
    sequencial_acao_meta_plano_acao: Optional[int]
    id_meta_plano_acao: Optional[int]


class PaginatedPlanoAcaoMetaAcaoResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoMetaAcaoResponse]


class ProgramaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_programa: Optional[int]
    ano_programa: Optional[int]
    modalidade_programa: Optional[str]
    codigo_programa: Optional[str]
    nome_programa: Optional[str]
    id_unidade_gestora_programa: Optional[int]
    nome_institucional_programa: Optional[str]
    permite_transferencia_sem_fundo_programa: Optional[bool]
    objetivo_programa: Optional[str]
    descricao_programa: Optional[str]
    situacao_programa: Optional[str]
    valor_global_programa: Optional[float]
    quantidade_parcelas_programa: Optional[int]
    id_orgao_superior_programa: Optional[int]
    sigla_orgao_superior_programa: Optional[str]
    cnpj_orgao_superior_programa: Optional[str]
    nome_orgao_superior_programa: Optional[str]
    id_fundo_programa: Optional[int]
    cnpj_fundo_programa: Optional[str]
    nome_fundo_programa: Optional[str]
    uf_fundo_programa: Optional[str]
    municipio_fundo_programa: Optional[str]
    codigo_ibge_fundo_programa: Optional[int]
    grupo_natureza_despesa_programa: Optional[str]
    codigo_descricao_orcamentaria_programa: Optional[str]
    descricao_acao_orcamentaria_programa: Optional[str]
    valor_acao_orcamentaria_programa: Optional[float]
    data_inicio_recebimento_planos_acao_beneficiarios_especificos: Optional[date]
    data_fim_recebimento_planos_acao_beneficiarios_especificos: Optional[date]
    data_inicio_recebimento_planos_acao_beneficiarios_emendas: Optional[date]
    data_fim_recebimento_planos_acao_beneficiarios_emendas: Optional[date]
    data_inicio_recebimento_planos_acao_beneficiarios_voluntarios: Optional[date]
    data_fim_recebimento_planos_acao_beneficiarios_voluntarios: Optional[date]
    nome_gestao_agil_programa: Optional[str]


class PaginatedProgramaResponse(PaginatedResponseTemplate):
    data: List[ProgramaResponse]


class ProgramaBeneficiarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_beneficiario_programa: Optional[int]
    cnpj_beneficiario_programa: Optional[str]
    nome_beneficiario_programa: Optional[str]
    valor_beneficiario_programa: Optional[float]
    numero_emenda_beneficiario_programa: Optional[str]
    nome_parlamentar_beneficiario_programa: Optional[str]
    tipo_beneficiario_programa: Optional[str]
    uf_beneficiario_programa: Optional[str]
    id_programa: Optional[int]


class PaginatedProgramaBeneficiarioResponse(PaginatedResponseTemplate):
    data: List[ProgramaBeneficiarioResponse]


class ProgramaGestaoAgilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_programa_agil: Optional[int]
    id_programa_agil_bb: Optional[int]
    nome_programa_agil: Optional[str]
    codigo_programa_agil: Optional[str]
    codigo_siorg_orgao_programa_agil: Optional[int]
    sigla_orgao_programa_agil: Optional[str]
    cnpj_orgao_programa_agil: Optional[str]
    nome_orgao_programa_agil: Optional[str]
    id_programa: Optional[int]


class PaginatedProgramaGestaoAgilResponse(PaginatedResponseTemplate):
    data: List[ProgramaGestaoAgilResponse]


class RelatorioGestaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_relatorio_gestao: Optional[int]
    data_relatorio_gestao: Optional[date]
    data_e_hora_relatorio_gestao: Optional[str]
    tipo_relatorio_gestao: Optional[str]
    situacao_relatorio_gestao: Optional[str]
    valor_executado_relatorio_gestao: Optional[float]
    valor_pendente_relatorio_gestao: Optional[float]
    resultados_alcancados_metas_relatorio_gestao: Optional[str]
    descritivo_relatorio_gestao: Optional[str]
    contrapartida_relatorio_gestao: Optional[str]
    endereco_eletronico_publicidade_acoes_relatorio_gestao: Optional[str]
    declaracao_conformidade_relatorio_gestao: Optional[bool]
    id_plano_acao: Optional[int]


class PaginatedRelatorioGestaoResponse(PaginatedResponseTemplate):
    data: List[RelatorioGestaoResponse]


class RelatorioGestaoAcoesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_acao_relatorio_gestao: Optional[int]
    percentual_execucao_fisica_acao_relatorio_gestao_acao: Optional[str]
    observacoes_justificativas_relatorio_gestao_acao: Optional[str]
    id_relatorio_gestao: Optional[int]
    id_acao_meta_plano_acao: Optional[int]


class PaginatedRelatorioGestaoAcoesResponse(PaginatedResponseTemplate):
    data: List[RelatorioGestaoAcoesResponse]


class RelatorioGestaoAnaliseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_relatorio_gestao_analise: Optional[int]
    tipo_analise_relatorio_gestao_analise: Optional[str]
    resultado_analise_relatorio_gestao_analise: Optional[str]
    parecer_analise_relatorio_gestao_analise: Optional[str]
    origem_analise_relatorio_gestao_analise: Optional[str]
    data_analise_relatorio_gestao_analise: Optional[date]
    versao_analise_relatorio_gestao_analise: Optional[int]
    id_relatorio_gestao: Optional[int]


class PaginatedRelatorioGestaoAnaliseResponse(PaginatedResponseTemplate):
    data: List[RelatorioGestaoAnaliseResponse]


class RelatorioGestaoAnaliseResponsavelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid", populate_by_name=True)

    relatorio_gestao_analise_fk: Optional[int] = Field(alias="id_relatorio_gestao_analise")
    nome_responsavel_analise_relatorio_gestao_analise: Optional[str]
    cargo_responsavel_analise_relatorio_gestao_analise: Optional[str]


class PaginatedRelatorioGestaoAnaliseResponsavelResponse(PaginatedResponseTemplate):
    data: List[RelatorioGestaoAnaliseResponsavelResponse]


class TermoAdesaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_termo_adesao: Optional[int]
    numero_processo_termo_adesao: Optional[str]
    situacao_termo_adesao: Optional[str]
    objeto_termo_adesao: Optional[str]
    data_assinatura_termo_adesao: Optional[date]
    ano_termo_adesao: Optional[int]
    secao_publicacao_dou_termo_adesao: Optional[int]
    pagina_publicacao_dou_termo_adesao: Optional[int]
    data_publicacao_dou_termo_adesao: Optional[date]
    id_plano_acao: Optional[int]


class PaginatedTermoAdesaoResponse(PaginatedResponseTemplate):
    data: List[TermoAdesaoResponse]


class TermoAdesaoHistoricoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_historico_termo_adesao: Optional[int]
    situacao_historico_termo_adesao: Optional[str]
    data_historico_termo_adesao: Optional[date]
    id_termo_adesao: Optional[int]


class PaginatedTermoAdesaoHistoricoResponse(PaginatedResponseTemplate):
    data: List[TermoAdesaoHistoricoResponse]