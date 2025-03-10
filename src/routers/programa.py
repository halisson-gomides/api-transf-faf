from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaResponse
from datetime import date
from typing import Optional
from src.cache import cache


pg_router = APIRouter(tags=["Programa"])


@pg_router.get("/programa",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Progrma - FaF.",
                response_description="Lista Paginada de Programas - FaF",
                response_model=PaginatedProgramaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_programa_faf(
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
    ano_programa: Optional[int] = Query(None, description="Ano do Programa"),
    modalidade_programa: Optional[str] = Query(None, description="Modalidade do Programa"),
    codigo_programa: Optional[str] = Query(None, description="Código do Prefixo do Programa concatenado com o Ano do Programa seguido do Código do Sufixo do Programa"),
    nome_programa: Optional[str] = Query(None, description="Nome do Programa"),
    id_unidade_gestora_programa: Optional[int] = Query(None, description="Identificador Único do Código UG - Unidade Gestora do Orgão do Programa"),
    nome_institucional_programa: Optional[str] = Query(None, description="Nome Institucional do Programa"),
    permite_transferencia_sem_fundo_programa: Optional[bool] = Query(None, description="Indicador de Permissão de Transferência para Ente"),
    objetivo_programa: Optional[str] = Query(None, description="Objetivo do Programa"),
    descricao_programa: Optional[str] = Query(None, description="Descrição do Programa"),
    situacao_programa: Optional[str] = Query(None, description="Situação do Programa"),
    valor_global_programa: Optional[float] = Query(None, description="Valor Global do Programa", ge=0),
    quantidade_parcelas_programa: Optional[int] = Query(None, description="Quantidade de Parcelas do Programa", ge=0),
    id_orgao_superior_programa: Optional[int] = Query(None, description="Identificador Único do Orgão Superior do Programa"),
    sigla_orgao_superior_programa: Optional[str] = Query(None, description="Sigla do Orgão Superior do Programa"),
    cnpj_orgao_superior_programa: Optional[str] = Query(None, description="CNPJ do Orgão Superior do Programa"),
    nome_orgao_superior_programa: Optional[str] = Query(None, description="Nome do Orgão Superior do Programa"),
    id_fundo_programa: Optional[int] = Query(None, description="Identificador Único do Fundo do Programa"),
    cnpj_fundo_programa: Optional[str] = Query(None, description="CNPJ do Fundo do Programa"),
    nome_fundo_programa: Optional[str] = Query(None, description="Nome do Fundo do Programa"),
    uf_fundo_programa: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Fundo do Programa"),
    municipio_fundo_programa: Optional[str] = Query(None, description="Nome do Município do Fundo do Programa"),
    codigo_ibge_fundo_programa: Optional[int] = Query(None, description="Código IBGE do Município do Fundo do Programa"),
    grupo_natureza_despesa_programa: Optional[str] = Query(None, description="Grupos Natureza Despesa do Programa"),
    codigo_descricao_orcamentaria_programa: Optional[str] = Query(None, description="Código da Ação Orçamentária do Programa"),
    descricao_acao_orcamentaria_programa: Optional[str] = Query(None, description="Descrição da Ação Orçamentária do Programa"),
    valor_acao_orcamentaria_programa: Optional[float] = Query(None, description="Valor da Ação Orçamentária do Programa", ge=0),
    data_inicio_recebimento_planos_acao_beneficiarios_especificos: Optional[str] = Query(None, description="Data de Início do Recebimento dos Planos de Ação para Beneficiários Específicos", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_fim_recebimento_planos_acao_beneficiarios_especificos: Optional[str] = Query(None, description="Data Final do Recebimento dos Planos de Ação para Beneficiários Específicos", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_inicio_recebimento_planos_acao_beneficiarios_emendas: Optional[str] = Query(None, description="Data de Início do Recebimento dos Planos de Ação para Beneficiários de Emenda Parlamentar", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_fim_recebimento_planos_acao_beneficiarios_emendas: Optional[str] = Query(None, description="Data Final do Recebimento dos Planos de Ação para Beneficiários de Emenda Parlamentar", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_inicio_recebimento_planos_acao_beneficiarios_voluntarios: Optional[str] = Query(None, description="Data de Início do Recebimento dos Planos de Ação para Beneficiários Voluntários", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_fim_recebimento_planos_acao_beneficiarios_voluntarios: Optional[str] = Query(None, description="Data Final do Recebimento dos Planos de Ação para Beneficiários Voluntários", pattern="^\d{4}-\d{2}-\d{2}$"),
    nome_gestao_agil_programa: Optional[str] = Query(None, description="Nomes dos Programas no Sistema de Gestão Ágil BB"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)
    
    try:
        query = select(models.Programa).where(
            and_(
                models.Programa.id_programa == id_programa if id_programa is not None else True,
                models.Programa.ano_programa == ano_programa if ano_programa is not None else True,
                models.Programa.modalidade_programa == modalidade_programa if modalidade_programa is not None else True,
                models.Programa.codigo_programa == codigo_programa if codigo_programa is not None else True,
                models.Programa.nome_programa.ilike(f"%{nome_programa}%") if nome_programa is not None else True,
                models.Programa.id_unidade_gestora_programa == id_unidade_gestora_programa if id_unidade_gestora_programa is not None else True,
                models.Programa.nome_institucional_programa.ilike(f"%{nome_institucional_programa}%") if nome_institucional_programa is not None else True,
                models.Programa.permite_transferencia_sem_fundo_programa == permite_transferencia_sem_fundo_programa if permite_transferencia_sem_fundo_programa is not None else True,
                models.Programa.objetivo_programa.ilike(f"%{objetivo_programa}%") if objetivo_programa is not None else True,
                models.Programa.descricao_programa.ilike(f"%{descricao_programa}%") if descricao_programa is not None else True,
                models.Programa.situacao_programa.ilike(f"%{situacao_programa}%") if situacao_programa is not None else True,
                models.Programa.valor_global_programa == valor_global_programa if valor_global_programa is not None else True,
                models.Programa.quantidade_parcelas_programa == quantidade_parcelas_programa if quantidade_parcelas_programa is not None else True,
                models.Programa.id_orgao_superior_programa == id_orgao_superior_programa if id_orgao_superior_programa is not None else True,
                models.Programa.sigla_orgao_superior_programa == sigla_orgao_superior_programa if sigla_orgao_superior_programa is not None else True,
                models.Programa.cnpj_orgao_superior_programa == cnpj_orgao_superior_programa if cnpj_orgao_superior_programa is not None else True,
                models.Programa.nome_orgao_superior_programa.ilike(f"%{nome_orgao_superior_programa}%") if nome_orgao_superior_programa is not None else True,
                models.Programa.id_fundo_programa == id_fundo_programa if id_fundo_programa is not None else True,
                models.Programa.cnpj_fundo_programa == cnpj_fundo_programa if cnpj_fundo_programa is not None else True,
                models.Programa.nome_fundo_programa.ilike(f"%{nome_fundo_programa}%") if nome_fundo_programa is not None else True,
                models.Programa.uf_fundo_programa == uf_fundo_programa if uf_fundo_programa is not None else True,
                models.Programa.municipio_fundo_programa == municipio_fundo_programa if municipio_fundo_programa is not None else True,
                models.Programa.codigo_ibge_fundo_programa == codigo_ibge_fundo_programa if codigo_ibge_fundo_programa is not None else True,
                models.Programa.grupo_natureza_despesa_programa.ilike(f"%{grupo_natureza_despesa_programa}%") if grupo_natureza_despesa_programa is not None else True,
                models.Programa.codigo_descricao_orcamentaria_programa == codigo_descricao_orcamentaria_programa if codigo_descricao_orcamentaria_programa is not None else True,
                models.Programa.descricao_acao_orcamentaria_programa.ilike(f"%{descricao_acao_orcamentaria_programa}%") if descricao_acao_orcamentaria_programa is not None else True,
                models.Programa.valor_acao_orcamentaria_programa == valor_acao_orcamentaria_programa if valor_acao_orcamentaria_programa is not None else True,
                cast(models.Programa.data_inicio_recebimento_planos_acao_beneficiarios_especificos, Date) == date.fromisoformat(data_inicio_recebimento_planos_acao_beneficiarios_especificos) if data_inicio_recebimento_planos_acao_beneficiarios_especificos is not None else True,
                cast(models.Programa.data_fim_recebimento_planos_acao_beneficiarios_especificos, Date) == date.fromisoformat(data_fim_recebimento_planos_acao_beneficiarios_especificos) if data_fim_recebimento_planos_acao_beneficiarios_especificos is not None else True,
                cast(models.Programa.data_inicio_recebimento_planos_acao_beneficiarios_emendas, Date) == date.fromisoformat(data_inicio_recebimento_planos_acao_beneficiarios_emendas) if data_inicio_recebimento_planos_acao_beneficiarios_emendas is not None else True,
                cast(models.Programa.data_fim_recebimento_planos_acao_beneficiarios_emendas, Date) == date.fromisoformat(data_fim_recebimento_planos_acao_beneficiarios_emendas) if data_fim_recebimento_planos_acao_beneficiarios_emendas is not None else True,
                cast(models.Programa.data_inicio_recebimento_planos_acao_beneficiarios_voluntarios, Date) == date.fromisoformat(data_inicio_recebimento_planos_acao_beneficiarios_voluntarios) if data_inicio_recebimento_planos_acao_beneficiarios_voluntarios is not None else True,
                cast(models.Programa.data_fim_recebimento_planos_acao_beneficiarios_voluntarios, Date) == date.fromisoformat(data_fim_recebimento_planos_acao_beneficiarios_voluntarios) if data_fim_recebimento_planos_acao_beneficiarios_voluntarios is not None else True,
                models.Programa.nome_gestao_agil_programa.ilike(f"%{nome_gestao_agil_programa}%") if nome_gestao_agil_programa is not None else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)