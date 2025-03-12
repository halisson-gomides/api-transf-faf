from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoMetaAcaoResponse
from datetime import date
from typing import Optional
from src.cache import cache


pama_router = APIRouter(tags=["Plano de Ação - Ações da Meta"])


@pama_router.get("/plano_acao_meta_acao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Ações das Metas dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Ações das Metas dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoMetaAcaoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_meta_acao_faf(
    id_acao_meta_plano_acao: Optional[int] = Query(None, description="Identificador Único da Ação da Meta do Plano de Ação"),
    numero_acao_meta_plano_acao: Optional[str] = Query(None, description="Número da Ação da Meta do Plano de Ação (Letra 'A' seguida do sequencial da Meta do Plano de Ação, seguido de '.', seguida do Sequencial da Ação da Meta do Plano de Ação )"),
    nome_acao_meta_plano_acao: Optional[str] = Query(None, description="Nome da Ação da Meta do Plano de Ação"),
    descricao_acao_meta_plano_acao: Optional[str] = Query(None, description="Descrição da Ação da Meta do Plano de Ação"),
    valor_acao_meta_plano_acao: Optional[float] = Query(None, description="Valor da Ação da Meta do Plano de Ação", ge=0),
    versao_acao_meta_plano_acao: Optional[int] = Query(None, description="Versão da Ação da Meta do Plano de Ação"),
    sequencial_acao_meta_plano_acao: Optional[int] = Query(None, description="Número Sequencial da Ação da Meta do Plano de Ação"),
    id_meta_plano_acao: Optional[int] = Query(None, description="Identificador Único da Meta do Plano de Ação"),
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
        query = select(models.PlanoAcaoMetaAcao).where(
            and_(
                models.PlanoAcaoMetaAcao.id_acao_meta_plano_acao == id_acao_meta_plano_acao if id_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.numero_acao_meta_plano_acao == numero_acao_meta_plano_acao if numero_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.nome_acao_meta_plano_acao.ilike(f"%{nome_acao_meta_plano_acao}%") if nome_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.descricao_acao_meta_plano_acao.ilike(f"%{descricao_acao_meta_plano_acao}%") if descricao_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.valor_acao_meta_plano_acao == valor_acao_meta_plano_acao if valor_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.versao_acao_meta_plano_acao == versao_acao_meta_plano_acao if versao_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.sequencial_acao_meta_plano_acao == sequencial_acao_meta_plano_acao if sequencial_acao_meta_plano_acao is not None else True,
                models.PlanoAcaoMetaAcao.id_meta_plano_acao == id_meta_plano_acao if id_meta_plano_acao is not None else True
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