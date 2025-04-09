from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional

db_schema = 'api_transferegov_faf'

class BaseModel(SQLModel, table=False):
    __table_args__ = {"schema": db_schema}

# Tabela empenho
class Empenho(BaseModel, table=True):
    __tablename__ = "empenho"
    
    id_empenho: int = Field(primary_key=True)
    numero_empenho: str
    ano_empenho: str
    gestao_emitente_empenho: str
    ug_emitente_empenho: str
    data_emissao_empenho: date
    fonte_recurso_empenho: str
    esfera_orcamentaria_empenho: int
    descricao_esfera_orcamentaria_empenho: str
    plano_interno_empenho: str
    unidade_gestora_responsavel_empenho: str
    observacao_empenho: str
    cnpj_favorecido_empenho: str
    numero_lista_empenho: str
    unidade_gestora_referencia_empenho: str
    gestao_referencia_empenho: str
    numero_interno_empenho: int
    objeto_empenho: str
    numero_sistema_empenho: str
    natureza_despesa_empenho: str
    natureza_despesa_sub_item_empenho: int
    tipo_empenho: int
    descricao_tipo_empenho: str
    codigo_tipo_nota_empenho: str
    descricao_tipo_nota_empenho: str
    situacao_empenho: int
    descricao_situacao_empenho: str
    valor_empenho: float
    versao_empenho: int
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela gestao_financeira_categorias_despesa
class GestaoFinanceiraCategoriasDespesa(BaseModel, table=True):
    __tablename__ = "gestao_financeira_categorias_despesa"
    
    id_categoria_despesa_gestao_financeira: int = Field(primary_key=True)
    id_nivel_pai_categoria_despesa_gestao_financeira: int
    nome_nivel_atual_categoria_despesa_gestao_financeira: str
    nivel_atual_categoria_despesa_gestao_financeira: int
    nome_completo_niveis_categoria_despesa_gestao_financeira: str
    codigo_programa_agil: int
    nome_programa_agil: str


# Tabela gestao_financeira_lancamentos
class GestaoFinanceiraLancamentos(BaseModel, table=True):
    __tablename__ = "gestao_financeira_lancamentos"
    
    id_lancamento_gestao_financeira: int = Field(primary_key=True)
    origem_solicitacao_gestao_financeira: str
    descricao_origem_solicitacao_gestao_financeira: str
    cnpj_ente_solicitante_gestao_financeira: str
    nome_ente_solicitante_gestao_financeira: str
    nome_personalizado_ente_solicitante_gestao_financeira: str
    codigo_programa_agil_ente_solicitante_gestao_financeira: str
    codigo_banco_gestao_financeira: str
    codigo_agencia_gestao_financeira: str
    dv_agencia_gestao_financeira: str
    codigo_conta_gestao_financeira: str
    dv_conta_gestao_financeira: str
    tipo_operacao_gestao_financeira: str
    descricao_tipo_operacao_gestao_financeira: str
    descricao_gestao_financeira: str
    data_lancamento_gestao_financeira: date
    data_evento_lancamento_gestao_financeira: date
    numero_ordem_gestao_financeira: int
    numero_referencia_unica_gestao_financeira: str
    tipo_favorecido_gestao_financeira: int
    descricao_tipo_favorecido_gestao_financeira: str
    doc_favorecido_gestao_financeira_mask: str
    nome_favorecido_gestao_financeira: str
    codigo_banco_favorecido_gestao_financeira: str
    codigo_agencia_favorecido_gestao_financeira: str
    dv_agencia_favorecido_gestao_financeira: str
    codigo_conta_favorecido_gestao_financeira: str
    dv_conta_favorecido_gestao_financeira: str
    valor_lancamento_gestao_financeira: float
    id_categoria_despesa_gestao_financeira: int = Field(foreign_key=f"{db_schema}.gestao_financeira_categorias_despesa.id_categoria_despesa_gestao_financeira")
    quantidade_subtransacoes_lancamento_gestao_financeira: int
    id_agencia_conta: str


# Tabela gestao_financeira_subtransacoes
class GestaoFinanceiraSubtransacoes(BaseModel, table=True):
    __tablename__ = "gestao_financeira_subtransacoes"
    
    id_subtransacao_gestao_financeira: str = Field(primary_key=True)
    estado_subtransacao_gestao_financeira: int
    situacao_pagamento_subtransacao_gestao_financeira: int
    descricao_situacao_pagamento_subtransacao_gestao_financeira: str
    data_pagamento_subtransacao_gestao_financeira: date
    tipo_pessoa_beneficiario_subtransacao_gestao_financeira: int
    descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei: str
    numero_documento_beneficiario_subtransacao_gestao_financeira_ma: str
    nome_beneficiario_subtransacao_gestao_financeira: str
    codigo_banco_beneficiario_subtransacao_gestao_financeira: str
    codigo_agencia_beneficiario_subtransacao_gestao_financeira: str
    codigo_conta_beneficiario_subtransacao_gestao_financeira: str
    descricao_subtransacao_gestao_financeira: str
    valor_subtransacao_gestao_financeira: float
    id_categoria_despesa_gestao_financeira: int = Field(foreign_key=f"{db_schema}.gestao_financeira_categorias_despesa.id_categoria_despesa_gestao_financeira")
    id_lancamento_gestao_financeira: int = Field(foreign_key=f"{db_schema}.gestao_financeira_lancamentos.id_lancamento_gestao_financeira")


# Tabela plano_acao
class PlanoAcao(BaseModel, table=True):
    __tablename__ = "plano_acao"
    
    id_plano_acao: int = Field(primary_key=True)
    codigo_plano_acao: str
    data_inicio_vigencia_plano_acao: date
    data_fim_vigencia_plano_acao: date
    diagnostico_plano_acao: str
    objetivos_plano_acao: str
    situacao_plano_acao: str
    valor_repasse_emenda_plano_acao: float
    valor_repasse_especifico_plano_acao: float
    valor_repasse_voluntario_plano_acao: float
    valor_total_repasse_plano_acao: float
    valor_recursos_proprios_plano_acao: float
    valor_outros_plano_acao: float
    valor_rendimentos_aplicacao_plano_acao: float
    valor_total_plano_acao: float
    valor_total_investimento_plano_acao: float
    valor_total_custeio_plano_acao: float
    valor_saldo_disponivel_plano_acao: float
    id_orgao_repassador_plano_acao: int
    sigla_orgao_repassador_plano_acao: str
    cnpj_orgao_repassador_plano_acao: str
    nome_orgao_repassador_plano_acao: str
    id_ente_repassador_plano_acao: int
    cnpj_ente_repassador_plano_acao: str
    nome_ente_repassador_plano_acao: str
    uf_ente_repassador_plano_acao: str
    nome_municipio_ente_repassador_plano_acao: str
    codigo_ibge_municipio_ente_repassador_plano_acao: int
    id_ente_recebedor_plano_acao: int
    cnpj_ente_recebedor_plano_acao: str
    nome_ente_recebedor_plano_acao: str
    uf_ente_recebedor_plano_acao: str
    nome_municipio_ente_recebedor_plano_acao: str
    codigo_ibge_municipio_ente_recebedor_plano_acao: int
    id_fundo_repassador_plano_acao: int
    cnpj_fundo_repassador_plano_acao: str
    nome_fundo_repassador_plano_acao: str
    uf_fundo_repassador_plano_acao: str
    municipio_fundo_repassador_plano_acao: str
    codigo_ibge_fundo_repassador_plano_acao: int
    id_fundo_recebedor_plano_acao: int
    cnpj_fundo_recebedor_plano_acao: str
    nome_fundo_recebedor_plano_acao: str
    uf_fundo_recebedor_plano_acao: str
    municipio_fundo_recebedor_plano_acao: str
    codigo_ibge_fundo_recebedor_plano_acao: int
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)


# Tabela plano_acao_analise
class PlanoAcaoAnalise(BaseModel, table=True):
    __tablename__ = "plano_acao_analise"
    
    id_analise_plano_acao: int = Field(primary_key=True)
    tipo_analise_plano_acao: str
    tipo_analise_resultado_plano_acao: str
    data_analise_plano_acao: date
    parecer_analise_plano_acao: str
    tipo_origem_analise_plano_acao: str
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)
    id_historico_plano_acao: int


# Tabela plano_acao_analise_responsavel
class PlanoAcaoAnaliseResponsavel(BaseModel, table=True):
    __tablename__ = "plano_acao_analise_responsavel"
    
    plano_acao_analise_fk: int = Field(foreign_key=f"{db_schema}.plano_acao_analise.id_analise_plano_acao", primary_key=True)
    nome_responsavel_analise_plano_acao: str = Field(primary_key=True)
    cargo_responsavel_analise_plano_acao: str = Field(primary_key=True)


# Tabela plano_acao_dado_bancario
class PlanoAcaoDadoBancario(BaseModel, table=True):
    __tablename__ = "plano_acao_dado_bancario"
    
    id_plano_acao_dado_bancario: int = Field(primary_key=True)
    id_agencia_conta: str
    codigo_banco_plano_acao_dado_bancario: int
    nome_banco_plano_acao_dado_bancario: str
    numero_agencia_plano_acao_dado_bancario: int
    dv_agencia_plano_acao_dado_bancario: str
    numero_conta_plano_acao_dado_bancario: int
    dv_conta_plano_acao_dado_bancario: str
    situacao_conta_plano_acao_dado_bancario: str
    data_abertura_conta_plano_acao_dado_bancario: date
    nome_programa_agil_conta_plano_acao_dado_bancario: str
    saldo_final_conta_plano_acao_dado_bancario: float
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela plano_acao_destinacao_recursos
class PlanoAcaoDestinacaoRecursos(BaseModel, table=True):
    __tablename__ = "plano_acao_destinacao_recursos"
    
    id_destinacao_recursos_plano_acao: int = Field(primary_key=True)
    codigo_natureza_despesa_destinacao_recursos_plano_acao: str
    descricao_natureza_despesa_destinacao_recursos_plano_acao: str
    tipo_despesa_destinacao_recursos_plano_acao: str
    valor_destinacao_recursos_plano_acao: float
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela plano_acao_historico
class PlanoAcaoHistorico(BaseModel, table=True):
    __tablename__ = "plano_acao_historico"
    
    id_historico_plano_acao: int = Field(primary_key=True)
    situacao_historico_plano_acao: str
    data_historico_plano_acao: date
    versao_historico_plano_acao: int
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela plano_acao_meta
class PlanoAcaoMeta(BaseModel, table=True):
    __tablename__ = "plano_acao_meta"
    
    id_meta_plano_acao: int = Field(primary_key=True)
    numero_meta_plano_acao: str
    nome_meta_plano_acao: str
    descricao_meta_plano_acao: str
    valor_meta_plano_acao: float
    versao_meta_plano_acao: int
    sequencial_meta_plano_acao: int
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela plano_acao_meta_acao
class PlanoAcaoMetaAcao(BaseModel, table=True):
    __tablename__ = "plano_acao_meta_acao"
    
    id_acao_meta_plano_acao: int = Field(primary_key=True)
    numero_acao_meta_plano_acao: str
    nome_acao_meta_plano_acao: str
    descricao_acao_meta_plano_acao: str
    valor_acao_meta_plano_acao: float
    versao_acao_meta_plano_acao: int
    sequencial_acao_meta_plano_acao: int
    id_meta_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao_meta.id_meta_plano_acao", primary_key=True)


# Tabela programa
class Programa(BaseModel, table=True):
    __tablename__ = "programa"
    
    id_programa: int = Field(primary_key=True)
    ano_programa: int
    modalidade_programa: str
    codigo_programa: str
    nome_programa: str
    id_unidade_gestora_programa: int
    nome_institucional_programa: str
    permite_transferencia_sem_fundo_programa: bool
    objetivo_programa: str
    descricao_programa: str
    situacao_programa: str
    valor_global_programa: float
    quantidade_parcelas_programa: int
    id_orgao_superior_programa: int
    sigla_orgao_superior_programa: str
    cnpj_orgao_superior_programa: str
    nome_orgao_superior_programa: str
    id_fundo_programa: int
    cnpj_fundo_programa: str
    nome_fundo_programa: str
    uf_fundo_programa: str
    municipio_fundo_programa: str
    codigo_ibge_fundo_programa: int
    grupo_natureza_despesa_programa: str
    codigo_descricao_orcamentaria_programa: str
    descricao_acao_orcamentaria_programa: str
    valor_acao_orcamentaria_programa: float
    data_inicio_recebimento_planos_acao_beneficiarios_especificos: date
    data_fim_recebimento_planos_acao_beneficiarios_especificos: date
    data_inicio_recebimento_planos_acao_beneficiarios_emendas: date
    data_fim_recebimento_planos_acao_beneficiarios_emendas: date
    data_inicio_recebimento_planos_acao_beneficiarios_voluntarios: date
    data_fim_recebimento_planos_acao_beneficiarios_voluntarios: date
    nome_gestao_agil_programa: str


# Tabela programa_beneficiario
class ProgramaBeneficiario(BaseModel, table=True):
    __tablename__ = "programa_beneficiario"
    
    id_beneficiario_programa: int = Field(primary_key=True)
    cnpj_beneficiario_programa: str
    nome_beneficiario_programa: str
    valor_beneficiario_programa: float
    numero_emenda_beneficiario_programa: str
    nome_parlamentar_beneficiario_programa: str
    tipo_beneficiario_programa: str
    uf_beneficiario_programa: str
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)


# Tabela programa_gestao_agil
class ProgramaGestaoAgil(BaseModel, table=True):
    __tablename__ = "programa_gestao_agil"
    
    id_programa_agil: int = Field(primary_key=True)
    id_programa_agil_bb: int
    nome_programa_agil: str
    codigo_programa_agil: str
    codigo_siorg_orgao_programa_agil: int
    sigla_orgao_programa_agil: str
    cnpj_orgao_programa_agil: str
    nome_orgao_programa_agil: str
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)


# Tabela relatorio_gestao
class RelatorioGestao(BaseModel, table=True):
    __tablename__ = "relatorio_gestao"
    
    id_relatorio_gestao: int = Field(primary_key=True)
    data_relatorio_gestao: date
    data_e_hora_relatorio_gestao: str
    tipo_relatorio_gestao: str
    situacao_relatorio_gestao: str
    valor_executado_relatorio_gestao: float
    valor_pendente_relatorio_gestao: float
    resultados_alcancados_metas_relatorio_gestao: str
    descritivo_relatorio_gestao: str
    contrapartida_relatorio_gestao: str
    endereco_eletronico_publicidade_acoes_relatorio_gestao: str
    declaracao_conformidade_relatorio_gestao: bool
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela relatorio_gestao_acoes
class RelatorioGestaoAcoes(BaseModel, table=True):
    __tablename__ = "relatorio_gestao_acoes"
    
    id_acao_relatorio_gestao: int = Field(primary_key=True)
    percentual_execucao_fisica_acao_relatorio_gestao_acao: str
    observacoes_justificativas_relatorio_gestao_acao: str
    id_relatorio_gestao: int = Field(foreign_key=f"{db_schema}.relatorio_gestao.id_relatorio_gestao", primary_key=True)
    id_acao_meta_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao_meta.id_meta_plano_acao", primary_key=True)


# Tabela relatorio_gestao_analise
class RelatorioGestaoAnalise(BaseModel, table=True):
    __tablename__ = "relatorio_gestao_analise"
    
    id_relatorio_gestao_analise: int = Field(primary_key=True)
    tipo_analise_relatorio_gestao_analise: str
    resultado_analise_relatorio_gestao_analise: str
    parecer_analise_relatorio_gestao_analise: str
    origem_analise_relatorio_gestao_analise: str
    data_analise_relatorio_gestao_analise: date
    versao_analise_relatorio_gestao_analise: int
    id_relatorio_gestao: int = Field(foreign_key=f"{db_schema}.relatorio_gestao.id_relatorio_gestao", primary_key=True)


# Tabela relatorio_gestao_analise_responsavel
class RelatorioGestaoAnaliseResponsavel(BaseModel, table=True):
    __tablename__ = "relatorio_gestao_analise_responsavel"
    
    relatorio_gestao_analise_fk: int = Field(foreign_key=f"{db_schema}.relatorio_gestao_analise.id_relatorio_gestao_analise", primary_key=True)
    nome_responsavel_analise_relatorio_gestao_analise: str = Field(primary_key=True)
    cargo_responsavel_analise_relatorio_gestao_analise: str = Field(primary_key=True)


# Tabela termo_adesao
class TermoAdesao(BaseModel, table=True):
    __tablename__ = "termo_adesao"
    
    id_termo_adesao: int = Field(primary_key=True)
    numero_processo_termo_adesao: str
    situacao_termo_adesao: str
    objeto_termo_adesao: str
    data_assinatura_termo_adesao: date
    ano_termo_adesao: int
    secao_publicacao_dou_termo_adesao: int
    pagina_publicacao_dou_termo_adesao: int
    data_publicacao_dou_termo_adesao: date
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao", primary_key=True)


# Tabela termo_adesao_historico
class TermoAdesaoHistorico(BaseModel, table=True):
    __tablename__ = "termo_adesao_historico"
    
    id_historico_termo_adesao: int = Field(primary_key=True)
    situacao_historico_termo_adesao: str
    data_historico_termo_adesao: date
    id_termo_adesao: int = Field(foreign_key=f"{db_schema}.termo_adesao.id_termo_adesao", primary_key=True)