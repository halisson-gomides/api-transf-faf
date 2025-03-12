from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoAnaliseResponse
from datetime import date
from typing import Optional
from src.cache import cache


paa_router = APIRouter(tags=["Plano de Ação - Análise"])


@paa_router.get("/plano_acao_analise",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Análises dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Análises dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoAnaliseResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_analise_faf(
    id_analise_plano_acao: Optional[int] = Query(None, description="Identificador Único da Análise do Plano de Ação"),
    tipo_analise_plano_acao: Optional[str] = Query(None, description="Tipo de Análise do Plano de Ação (MERITO, TECNICA, FINANCEIRA, TECNICA_FINANCEIRA)"),
    tipo_analise_resultado_plano_acao: Optional[str] = Query(None, description="Tipo de Resultado da Análise do Plano de Ação (COMPLEMENTACAO, APROVADO, COM_RESSALVA, REJEITADO)"),
    data_analise_plano_acao: Optional[str] = Query(None, description="Data da Análise do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    parecer_analise_plano_acao: Optional[str] = Query(None, description="Parecer da Análise do Plano de Ação"),
    tipo_origem_analise_plano_acao: Optional[str] = Query(None, description="Tipo de Origem da Análise realizada no Plano de Ação"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    id_historico_plano_acao: Optional[int] = Query(None, description="Identificador Único do Histórico do Plano de Ação"),
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
        query = select(models.PlanoAcaoAnalise).where(
            and_(
                models.PlanoAcaoAnalise.id_analise_plano_acao == id_analise_plano_acao if id_analise_plano_acao is not None else True,
                models.PlanoAcaoAnalise.tipo_analise_plano_acao.ilike(f"%{tipo_analise_plano_acao}%") if tipo_analise_plano_acao is not None else True,
                models.PlanoAcaoAnalise.tipo_analise_resultado_plano_acao.ilike(f"%{tipo_analise_resultado_plano_acao}%") if tipo_analise_resultado_plano_acao is not None else True,
                cast(models.PlanoAcaoAnalise.data_analise_plano_acao, Date) == date.fromisoformat(data_analise_plano_acao) if data_analise_plano_acao is not None else True,
                models.PlanoAcaoAnalise.parecer_analise_plano_acao.ilike(f"%{parecer_analise_plano_acao}%") if parecer_analise_plano_acao is not None else True,
                models.PlanoAcaoAnalise.tipo_origem_analise_plano_acao.ilike(f"%{tipo_origem_analise_plano_acao}%") if tipo_origem_analise_plano_acao is not None else True,
                models.PlanoAcaoAnalise.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.PlanoAcaoAnalise.id_historico_plano_acao == id_historico_plano_acao if id_historico_plano_acao is not None else True
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