from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoMetaResponse
from datetime import date
from typing import Optional
from src.cache import cache


pam_router = APIRouter(tags=["Plano de Ação - Meta"])


@pam_router.get("/plano_acao_meta",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Metas dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Metas dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoMetaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_meta_faf(
    id_meta_plano_acao: Optional[int] = Query(None, description="Identificador Único da Meta do Plano de Ação"),
    numero_meta_plano_acao: Optional[str] = Query(None, description="Número da Meta do Plano de Ação (Letra 'M' seguida do Sequencial da Meta do Plano de Ação)"),
    nome_meta_plano_acao: Optional[str] = Query(None, description="Nome da Meta do Plano de Ação"),
    descricao_meta_plano_acao: Optional[str] = Query(None, description="Descrição da Meta do Plano de Ação"),
    valor_meta_plano_acao: Optional[float] = Query(None, description="Somatório dos Valores das Ações da Meta do Plano de Ação"),
    versao_meta_plano_acao: Optional[int] = Query(None, description="Versão da Meta do Plano de Ação"),
    sequencial_meta_plano_acao: Optional[int] = Query(None, description="Número Sequencial da Meta do Plano de Ação"),
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
        query = select(models.PlanoAcaoMeta).where(
            and_(
                models.PlanoAcaoMeta.id_meta_plano_acao == id_meta_plano_acao if id_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.numero_meta_plano_acao == numero_meta_plano_acao if numero_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.nome_meta_plano_acao.ilike(f"%{nome_meta_plano_acao}%") if nome_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.descricao_meta_plano_acao.ilike(f"%{descricao_meta_plano_acao}%") if descricao_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.valor_meta_plano_acao == valor_meta_plano_acao if valor_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.versao_meta_plano_acao == versao_meta_plano_acao if versao_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.sequencial_meta_plano_acao == sequencial_meta_plano_acao if sequencial_meta_plano_acao is not None else True,
                models.PlanoAcaoMeta.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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