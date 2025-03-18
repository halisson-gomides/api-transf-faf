from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedRelatorioGestaoAnaliseResponse
from datetime import date
from typing import Optional
from src.cache import cache


rgan_router = APIRouter(tags=["Relatório de Gestão - Análise"])


@rgan_router.get("/relatorio_gestao_analise",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Análises associadas ao Relatório de Gestão - FaF.",
                response_description="Lista Paginada de Análises associadas ao Relatório de Gestão - FaF",
                response_model=PaginatedRelatorioGestaoAnaliseResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_relatorio_gestao_analise_faf(
    id_relatorio_gestao_analise: Optional[int] = Query(None, description="Identificador Único da Análise do Relatório de Gestão"),
    tipo_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Tipo de Análise realizada no Relatório de Gestão"),
    resultado_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Tipo do resultado da Análise do Relatório de Gestão"),
    parecer_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Parecer da Análise do Relatório de Gestão"),
    origem_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Tipo de Origem da Análise realizada no Relatório de Gestão"),
    data_analise_relatorio_gestao_analise: Optional[date] = Query(None, description="Data de Realização da Análise no Relatório de Gestão", pattern="^\d{4}-\d{2}-\d{2}$"),
    versao_analise_relatorio_gestao_analise: Optional[int] = Query(None, description="Versão da Análise do Relatório de Gestão"),
    id_relatorio_gestao: Optional[int] = Query(None, description="Identificador Único do Relatório de Gestão"),
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
        query = select(models.RelatorioGestaoAnalise).where(
            and_(
                models.RelatorioGestaoAnalise.id_relatorio_gestao_analise == id_relatorio_gestao_analise if id_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.tipo_analise_relatorio_gestao_analise.ilike(f"%{tipo_analise_relatorio_gestao_analise}%") if tipo_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.resultado_analise_relatorio_gestao_analise.ilike(f"%{resultado_analise_relatorio_gestao_analise}%") if resultado_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.parecer_analise_relatorio_gestao_analise.ilike(f"%{parecer_analise_relatorio_gestao_analise}%") if parecer_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.origem_analise_relatorio_gestao_analise == origem_analise_relatorio_gestao_analise if origem_analise_relatorio_gestao_analise is not None else True,
                cast(models.RelatorioGestaoAnalise.data_analise_relatorio_gestao_analise, Date) == date.fromisoformat(data_analise_relatorio_gestao_analise) if data_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.versao_analise_relatorio_gestao_analise == versao_analise_relatorio_gestao_analise if versao_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnalise.id_relatorio_gestao == id_relatorio_gestao if id_relatorio_gestao is not None else True
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