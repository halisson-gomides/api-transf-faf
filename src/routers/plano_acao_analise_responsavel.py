from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoAnaliseResponsavelResponse
from datetime import date
from typing import Optional
from src.cache import cache


paar_router = APIRouter(tags=["Plano de Ação - Responsável pela Análise"])


@paar_router.get("/plano_acao_analise_responsavel",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Responsáveis pela Análise dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Responsáveis pela Análise dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoAnaliseResponsavelResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_analise_responsavel_faf(
    id_analise_plano_acao: Optional[int] = Query(None, description="Identificador Único da Análise do Plano de Ação"),
    nome_responsavel_analise_plano_acao: Optional[str] = Query(None, description="Nome do Responsável pela Análise do Plano de Ação"),
    cargo_responsavel_analise_plano_acao: Optional[str] = Query(None, description="Nome do Responsável pela Análise do Plano de Ação"),
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
        query = select(models.PlanoAcaoAnaliseResponsavel).where(
            and_(
                models.PlanoAcaoAnaliseResponsavel.plano_acao_analise_fk == id_analise_plano_acao if id_analise_plano_acao is not None else True,
                models.PlanoAcaoAnaliseResponsavel.nome_responsavel_analise_plano_acao.ilike(f"%{nome_responsavel_analise_plano_acao}%") if nome_responsavel_analise_plano_acao is not None else True,
                models.PlanoAcaoAnaliseResponsavel.cargo_responsavel_analise_plano_acao.ilike(f"%{cargo_responsavel_analise_plano_acao}%") if cargo_responsavel_analise_plano_acao is not None else True
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