from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedTermoAdesaoHistoricoResponse
from datetime import date
from typing import Optional
from src.cache import cache


tah_router = APIRouter(tags=["Termo de Adesão - Histórico"])


@tah_router.get("/termo_adesao_historico",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Histórico dos Termos de Adesão - FaF.",
                response_description="Lista Paginada de Históricos dos Termos de Adesão - FaF",
                response_model=PaginatedTermoAdesaoHistoricoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_termo_adesao_historico_faf(
    id_historico_termo_adesao: Optional[int] = Query(None, description="Identificador Único do Histórico do Termo de Adesão"),
    situacao_historico_termo_adesao: Optional[str] = Query(None, description="Situação do Histórico do Termo de Adesão"),
    data_historico_termo_adesao: Optional[str] = Query(None, description="Data do Registro no Histórico do Termo de Adesão", pattern="^\d{4}-\d{2}-\d{2}$"),
    id_termo_adesao: Optional[int] = Query(None, description="Identificador Único do Termo de Adesão"),
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
        query = select(models.TermoAdesaoHistorico).where(
            and_(
                models.TermoAdesaoHistorico.id_historico_termo_adesao == id_historico_termo_adesao if id_historico_termo_adesao is not None else True,
                models.TermoAdesaoHistorico.situacao_historico_termo_adesao.ilike(f"%{situacao_historico_termo_adesao}%") if situacao_historico_termo_adesao is not None else True,
                cast(models.TermoAdesaoHistorico.data_historico_termo_adesao, Date) == date.fromisoformat(data_historico_termo_adesao) if data_historico_termo_adesao is not None else True,
                models.TermoAdesaoHistorico.id_termo_adesao == id_termo_adesao if id_termo_adesao is not None else True
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