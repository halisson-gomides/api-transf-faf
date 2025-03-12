from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoDestinacaoRecursosResponse
from datetime import date
from typing import Optional
from src.cache import cache


padr_router = APIRouter(tags=["Plano de Ação - Destinação de Recursos"])


@padr_router.get("/plano_acao_destinacao_recursos",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Itens de Despesa dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Itens de Despesa dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoDestinacaoRecursosResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_destinacao_recursos_faf(
    id_destinacao_recursos_plano_acao: Optional[int] = Query(None, description="Identificador Único do Item de Despesa Cadastrado no Plano de Ação"),
    codigo_natureza_despesa_destinacao_recursos_plano_acao: Optional[str] = Query(None, description="Código da Natureza de Despesa no SIAFI do Item de Despesa Cadastrado no Plano de Ação"),
    descricao_natureza_despesa_destinacao_recursos_plano_acao: Optional[str] = Query(None, description="Descrição da Natureza de Despesa no SIAFI do Item de Despesa Cadastrado no Plano de Ação"),
    tipo_despesa_destinacao_recursos_plano_acao: Optional[str] = Query(None, description="Tipo da Natureza de Despesa do Item de Despesa Cadastrado no Plano de Ação"),
    valor_destinacao_recursos_plano_acao: Optional[float] = Query(None, description="Valor do Recurso destinado ao Item de Despesa Cadastrado no Plano de Ação", ge=0),
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
        query = select(models.PlanoAcaoDestinacaoRecursos).where(
            and_(
                models.PlanoAcaoDestinacaoRecursos.id_destinacao_recursos_plano_acao == id_destinacao_recursos_plano_acao if id_destinacao_recursos_plano_acao is not None else True,
                models.PlanoAcaoDestinacaoRecursos.codigo_natureza_despesa_destinacao_recursos_plano_acao == codigo_natureza_despesa_destinacao_recursos_plano_acao if codigo_natureza_despesa_destinacao_recursos_plano_acao is not None else True,
                models.PlanoAcaoDestinacaoRecursos.descricao_natureza_despesa_destinacao_recursos_plano_acao.ilike(f"%{descricao_natureza_despesa_destinacao_recursos_plano_acao}%") if descricao_natureza_despesa_destinacao_recursos_plano_acao is not None else True,
                models.PlanoAcaoDestinacaoRecursos.tipo_despesa_destinacao_recursos_plano_acao.ilike(f"%{tipo_despesa_destinacao_recursos_plano_acao}%") if tipo_despesa_destinacao_recursos_plano_acao is not None else True,
                models.PlanoAcaoDestinacaoRecursos.valor_destinacao_recursos_plano_acao == valor_destinacao_recursos_plano_acao if valor_destinacao_recursos_plano_acao is not None else True,
                models.PlanoAcaoDestinacaoRecursos.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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