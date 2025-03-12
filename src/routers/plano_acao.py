from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoResponse
from datetime import date
from typing import Optional
from src.cache import cache


pa_router = APIRouter(tags=["Plano de Ação"])


@pa_router.get("/plano_acao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Plano de Ação - FaF.",
                response_description="Lista Paginada de Plano de Ação - FaF",
                response_model=PaginatedPlanoAcaoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_faf(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    codigo_plano_acao: Optional[str] = Query(None, description="Código do Programa concatenado com o Identificador Único do Plano de Ação"),
    data_inicio_vigencia_plano_acao: Optional[str] = Query(None, description="Data do Ínicio da Vigência do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_fim_vigencia_plano_acao: Optional[str] = Query(None, description="Data do Fim da Vigência do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    diagnostico_plano_acao: Optional[str] = Query(None, description="Diagnóstico do Plano de Ação"),
    objetivos_plano_acao: Optional[str] = Query(None, description="Objetivos do Plano de Ação"),
    situacao_plano_acao: Optional[str] = Query(None, description="Situação do Plano de Ação"),
    valor_repasse_emenda_plano_acao: Optional[float] = Query(None, description="Valor de Repasse da Emenda Parlamentar do Plano de Ação", ge=0),
    valor_repasse_especifico_plano_acao: Optional[float] = Query(None, description="Valor do Repasse Específico do Plano de Ação", ge=0),
    valor_repasse_voluntario_plano_acao: Optional[float] = Query(None, description="Valor do Repasse Voluntário do Plano de Ação", ge=0),
    valor_total_repasse_plano_acao: Optional[float] = Query(None, description="Valor Total do Repasse do Plano de Ação", ge=0),
    valor_recursos_proprios_plano_acao: Optional[float] = Query(None, description="Valor dos Recursos Próprios do Plano de Ação", ge=0),
    valor_outros_plano_acao: Optional[float] = Query(None, description="Valor Outros do Plano de Ação", ge=0),
    valor_rendimentos_aplicacao_plano_acao: Optional[float] = Query(None, description="Valor dos Rendimentos da Aplicação do Plano de Ação", ge=0),
    valor_total_plano_acao: Optional[float] = Query(None, description="Valor Total do Plano de Ação", ge=0),
    valor_total_investimento_plano_acao: Optional[float] = Query(None, description="Valor Total de Investimento do Plano de Ação", ge=0),
    valor_total_custeio_plano_acao: Optional[float] = Query(None, description="Valor Total de Custeio do Plano de Ação", ge=0),
    valor_saldo_disponivel_plano_acao: Optional[float] = Query(None, description="Valor do Saldo Disponível do Plano de Ação", ge=0),
    id_orgao_repassador_plano_acao: Optional[int] = Query(None, description="Identificador Único do Órgão Repassador no cadastro do Plano de Ação"),
    sigla_orgao_repassador_plano_acao: Optional[str] = Query(None, description="Sigla do Órgão Repassador do Plano de Ação"),
    cnpj_orgao_repassador_plano_acao: Optional[str] = Query(None, description="CNPJ do Órgão Repassador do Plano de Ação"),
    nome_orgao_repassador_plano_acao: Optional[str] = Query(None, description="Nome do Órgão Repassador do Plano de Ação"),
    id_ente_repassador_plano_acao: Optional[int] = Query(None, description="Identificador Único do Ente Repassador no cadastro do Plano de Ação"),
    cnpj_ente_repassador_plano_acao: Optional[str] = Query(None, description="CNPJ do Ente Repassador do Plano de Ação"),
    nome_ente_repassador_plano_acao: Optional[str] = Query(None, description="Nome do Ente Repassador do Plano de Ação"),
    uf_ente_repassador_plano_acao: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Ente Repassador do Plano de Ação"),
    nome_municipio_ente_repassador_plano_acao: Optional[str] = Query(None, description="Nome do Município do Ente Repassador do Plano de Ação"),
    codigo_ibge_municipio_ente_repassador_plano_acao: Optional[int] = Query(None, description="Código IBGE do Município do Ente Repassador do Plano de Ação"),
    id_ente_recebedor_plano_acao: Optional[int] = Query(None, description="Identificador Único do Ente Recebedor no cadastro do Plano de Ação"),
    cnpj_ente_recebedor_plano_acao: Optional[str] = Query(None, description="CNPJ do Ente Recebedor do Plano de Ação"),
    nome_ente_recebedor_plano_acao: Optional[str] = Query(None, description="Nome do Ente Recebedor do Plano de Ação"),
    uf_ente_recebedor_plano_acao: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Ente Recebedor do Plano de Ação"),
    nome_municipio_ente_recebedor_plano_acao: Optional[str] = Query(None, description="Nome do Município do Ente Recebedor do Plano de Ação"),
    codigo_ibge_municipio_ente_recebedor_plano_acao: Optional[int] = Query(None, description="Código IBGE do Município do Ente Recebedor do Plano de Ação"),
    id_fundo_repassador_plano_acao: Optional[int] = Query(None, description="Identificador Único do Fundo Repassador no cadastro do Plano de Ação"),
    cnpj_fundo_repassador_plano_acao: Optional[str] = Query(None, description="CNPJ do Fundo Repassador do Plano de Ação"),
    nome_fundo_repassador_plano_acao: Optional[str] = Query(None, description="Nome do Fundo Repassador do Plano de Ação"),
    uf_fundo_repassador_plano_acao: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Fundo Repassador do Plano de Ação"),
    municipio_fundo_repassador_plano_acao: Optional[str] = Query(None, description="Nome do Município do Fundo Repassador do Plano de Ação"),
    codigo_ibge_fundo_repassador_plano_acao: Optional[int] = Query(None, description="Código IBGE do Município do Fundo Repassador do Plano de Ação"),
    id_fundo_recebedor_plano_acao: Optional[int] = Query(None, description="Identificador Único do Fundo Recebedor no cadastro do Plano de Ação"),
    cnpj_fundo_recebedor_plano_acao: Optional[str] = Query(None, description="CNPJ do Fundo Recebedor do Plano de Ação"),
    nome_fundo_recebedor_plano_acao: Optional[str] = Query(None, description="Nome do Fundo Recebedor do Plano de Ação"),
    uf_fundo_recebedor_plano_acao: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Fundo Recebedor do Plano de Ação"),
    municipio_fundo_recebedor_plano_acao: Optional[str] = Query(None, description="Nome do Município do Fundo Recebedor do Plano de Ação"),
    codigo_ibge_fundo_recebedor_plano_acao: Optional[int] = Query(None, description="Código IBGE do Município do Fundo Recebedor do Plano de Ação"),
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),    
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
        query = select(models.PlanoAcao).where(
            and_(
                models.PlanoAcao.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.PlanoAcao.codigo_plano_acao == codigo_plano_acao if codigo_plano_acao is not None else True,
                cast(models.PlanoAcao.data_inicio_vigencia_plano_acao, Date) == date.fromisoformat(data_inicio_vigencia_plano_acao) if data_inicio_vigencia_plano_acao is not None else True,
                cast(models.PlanoAcao.data_fim_vigencia_plano_acao, Date) == date.fromisoformat(data_fim_vigencia_plano_acao) if data_fim_vigencia_plano_acao is not None else True,
                models.PlanoAcao.diagnostico_plano_acao.ilike(f"%{diagnostico_plano_acao}%") if diagnostico_plano_acao is not None else True,
                models.PlanoAcao.objetivos_plano_acao.ilike(f"%{objetivos_plano_acao}%") if objetivos_plano_acao is not None else True,
                models.PlanoAcao.situacao_plano_acao.ilike(f"%{situacao_plano_acao}%") if situacao_plano_acao is not None else True,
                models.PlanoAcao.valor_repasse_emenda_plano_acao == valor_repasse_emenda_plano_acao if valor_repasse_emenda_plano_acao is not None else True,
                models.PlanoAcao.valor_repasse_especifico_plano_acao == valor_repasse_especifico_plano_acao if valor_repasse_especifico_plano_acao is not None else True,
                models.PlanoAcao.valor_repasse_voluntario_plano_acao == valor_repasse_voluntario_plano_acao if valor_repasse_voluntario_plano_acao is not None else True,
                models.PlanoAcao.valor_total_repasse_plano_acao == valor_total_repasse_plano_acao if valor_total_repasse_plano_acao is not None else True,
                models.PlanoAcao.valor_recursos_proprios_plano_acao == valor_recursos_proprios_plano_acao if valor_recursos_proprios_plano_acao is not None else True,
                models.PlanoAcao.valor_outros_plano_acao == valor_outros_plano_acao if valor_outros_plano_acao is not None else True,
                models.PlanoAcao.valor_rendimentos_aplicacao_plano_acao == valor_rendimentos_aplicacao_plano_acao if valor_rendimentos_aplicacao_plano_acao is not None else True,
                models.PlanoAcao.valor_total_plano_acao == valor_total_plano_acao if valor_total_plano_acao is not None else True,
                models.PlanoAcao.valor_total_investimento_plano_acao == valor_total_investimento_plano_acao if valor_total_investimento_plano_acao is not None else True,
                models.PlanoAcao.valor_total_custeio_plano_acao == valor_total_custeio_plano_acao if valor_total_custeio_plano_acao is not None else True,
                models.PlanoAcao.valor_saldo_disponivel_plano_acao == valor_saldo_disponivel_plano_acao if valor_saldo_disponivel_plano_acao is not None else True,
                models.PlanoAcao.id_orgao_repassador_plano_acao == id_orgao_repassador_plano_acao if id_orgao_repassador_plano_acao is not None else True,
                models.PlanoAcao.sigla_orgao_repassador_plano_acao == sigla_orgao_repassador_plano_acao if sigla_orgao_repassador_plano_acao is not None else True,
                models.PlanoAcao.cnpj_orgao_repassador_plano_acao == cnpj_orgao_repassador_plano_acao if cnpj_orgao_repassador_plano_acao is not None else True,
                models.PlanoAcao.nome_orgao_repassador_plano_acao.ilike(f"%{nome_orgao_repassador_plano_acao}%") if nome_orgao_repassador_plano_acao is not None else True,
                models.PlanoAcao.id_ente_repassador_plano_acao == id_ente_repassador_plano_acao if id_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.cnpj_ente_repassador_plano_acao == cnpj_ente_repassador_plano_acao if cnpj_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.nome_ente_repassador_plano_acao.ilike(f"%{nome_ente_repassador_plano_acao}%") if nome_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.uf_ente_repassador_plano_acao == uf_ente_repassador_plano_acao if uf_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.nome_municipio_ente_repassador_plano_acao.ilike(f"%{nome_municipio_ente_repassador_plano_acao}%") if nome_municipio_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.codigo_ibge_municipio_ente_repassador_plano_acao == codigo_ibge_municipio_ente_repassador_plano_acao if codigo_ibge_municipio_ente_repassador_plano_acao is not None else True,
                models.PlanoAcao.id_ente_recebedor_plano_acao == id_ente_recebedor_plano_acao if id_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.cnpj_ente_recebedor_plano_acao == cnpj_ente_recebedor_plano_acao if cnpj_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.nome_ente_recebedor_plano_acao.ilike(f"%{nome_ente_recebedor_plano_acao}%") if nome_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.uf_ente_recebedor_plano_acao == uf_ente_recebedor_plano_acao if uf_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.nome_municipio_ente_recebedor_plano_acao.ilike(f"%{nome_municipio_ente_recebedor_plano_acao}%") if nome_municipio_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.codigo_ibge_municipio_ente_recebedor_plano_acao == codigo_ibge_municipio_ente_recebedor_plano_acao if codigo_ibge_municipio_ente_recebedor_plano_acao is not None else True,
                models.PlanoAcao.id_fundo_repassador_plano_acao == id_fundo_repassador_plano_acao if id_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.cnpj_fundo_repassador_plano_acao == cnpj_fundo_repassador_plano_acao if cnpj_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.nome_fundo_repassador_plano_acao.ilike(f"%{nome_fundo_repassador_plano_acao}%") if nome_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.uf_fundo_repassador_plano_acao == uf_fundo_repassador_plano_acao if uf_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.municipio_fundo_repassador_plano_acao.ilike(f"%{municipio_fundo_repassador_plano_acao}%") if municipio_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.codigo_ibge_fundo_repassador_plano_acao == codigo_ibge_fundo_repassador_plano_acao if codigo_ibge_fundo_repassador_plano_acao is not None else True,
                models.PlanoAcao.id_fundo_recebedor_plano_acao == id_fundo_recebedor_plano_acao if id_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.cnpj_fundo_recebedor_plano_acao == cnpj_fundo_recebedor_plano_acao if cnpj_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.nome_fundo_recebedor_plano_acao.ilike(f"%{nome_fundo_recebedor_plano_acao}%") if nome_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.uf_fundo_recebedor_plano_acao == uf_fundo_recebedor_plano_acao if uf_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.municipio_fundo_recebedor_plano_acao.ilike(f"%{municipio_fundo_recebedor_plano_acao}%") if municipio_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.codigo_ibge_fundo_recebedor_plano_acao == codigo_ibge_fundo_recebedor_plano_acao if codigo_ibge_fundo_recebedor_plano_acao is not None else True,
                models.PlanoAcao.id_programa == id_programa if id_programa is not None else True
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