from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoHistoricoResponse
from datetime import date
from typing import Optional
from src.cache import cache


pah_router = APIRouter(tags=["Plano de Ação - Histórico"])


@pah_router.get("/plano_acao_historico",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Histórico do Plano de Ação - FaF.",
                response_description="Lista Paginada de Históricos do Plano de Ação - FaF",
                response_model=PaginatedPlanoAcaoHistoricoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_historico_faf(
    id_historico_plano_acao: Optional[int] = Query(None, description="Identificador Único do Histórico do Plano de Ação"),
    situacao_historico_plano_acao: Optional[str] = Query(None, description="Situação do Histórico do Plano de Ação"),
    data_historico_plano_acao: Optional[str] = Query(None, description="Data do Registro no Histórico do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    versao_historico_plano_acao: Optional[int] = Query(None, description="Versão do Histórico do Plano de Ação"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
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
        query = select(models.PlanoAcaoHistorico).where(
            and_(
                models.PlanoAcaoHistorico.id_historico_plano_acao == id_historico_plano_acao if id_historico_plano_acao is not None else True,
                models.PlanoAcaoHistorico.situacao_historico_plano_acao.ilike(f"%{situacao_historico_plano_acao}%") if situacao_historico_plano_acao is not None else True,
                cast(models.PlanoAcaoHistorico.data_historico_plano_acao, Date) == date.fromisoformat(data_historico_plano_acao) if data_historico_plano_acao is not None else True,
                models.PlanoAcaoHistorico.versao_historico_plano_acao == versao_historico_plano_acao if versao_historico_plano_acao is not None else True,
                models.PlanoAcaoHistorico.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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