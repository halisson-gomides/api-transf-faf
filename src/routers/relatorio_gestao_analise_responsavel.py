from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedRelatorioGestaoAnaliseResponsavelResponse
from datetime import date
from typing import Optional
from src.cache import cache


rgra_router = APIRouter(tags=["Relatório de Gestão - Responsável pela Análise"])


@rgra_router.get("/relatorio_gestao_analise_responsavel",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Responsáveis pela Análise do Relatório de Gestão - FaF.",
                response_description="Lista Paginada de Responsáveis pela Análise do Relatório de Gestão - FaF",
                response_model=PaginatedRelatorioGestaoAnaliseResponsavelResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_relatorio_gestao_analise_responsavel_faf(
    id_relatorio_gestao_analise: Optional[int] = Query(None, description="Identificador Único da Análise do Relatório de Gestão"),
    nome_responsavel_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Nome do Responsável pela Análise do Relatório de Gestão"),
    cargo_responsavel_analise_relatorio_gestao_analise: Optional[str] = Query(None, description="Cargo do Responsável pela Análise do Relatório de Gestão"),
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
        query = select(models.RelatorioGestaoAnaliseResponsavel).where(
            and_(
                models.RelatorioGestaoAnaliseResponsavel.relatorio_gestao_analise_fk == id_relatorio_gestao_analise if id_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnaliseResponsavel.nome_responsavel_analise_relatorio_gestao_analise.ilike(f"%{nome_responsavel_analise_relatorio_gestao_analise}%") if nome_responsavel_analise_relatorio_gestao_analise is not None else True,
                models.RelatorioGestaoAnaliseResponsavel.cargo_responsavel_analise_relatorio_gestao_analise.ilike(f"%{cargo_responsavel_analise_relatorio_gestao_analise}%") if cargo_responsavel_analise_relatorio_gestao_analise is not None else True
            )
        )
        # print(str(query))
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)