from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedRelatorioGestaoAcoesResponse
from datetime import date
from typing import Optional
from src.cache import cache


rga_router = APIRouter(tags=["Relatório de Gestão - Ações"])


@rga_router.get("/relatorio_gestao_acoes",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Ações associadas ao Relatório de Gestão - FaF.",
                response_description="Lista Paginada de Ações associadas ao Relatório de Gestão - FaF",
                response_model=PaginatedRelatorioGestaoAcoesResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_relatorio_gestao_acoes_faf(
    id_acao_relatorio_gestao: Optional[int] = Query(None, description="Identificador Único da Ação associada ao Relatório de Gestão"),
    percentual_execucao_fisica_acao_relatorio_gestao_acao: Optional[str] = Query(None, description="Percentual de Conclusão da Ação do Relatório de Gestão"),
    observacoes_justificativas_relatorio_gestao_acao: Optional[str] = Query(None, description="Justificativa referente ao Percentual de Conclusão da Ação do Relatório de Gestão"),
    id_relatorio_gestao: Optional[int] = Query(None, description="Identificador Único do Relatório de Gestão"),
    id_acao_meta_plano_acao: Optional[int] = Query(None, description="Identificador Único da Ação da Meta do Plano de Ação"),
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
        query = select(models.RelatorioGestaoAcoes).where(
            and_(
                models.RelatorioGestaoAcoes.id_acao_relatorio_gestao == id_acao_relatorio_gestao if id_acao_relatorio_gestao is not None else True,
                models.RelatorioGestaoAcoes.percentual_execucao_fisica_acao_relatorio_gestao_acao == percentual_execucao_fisica_acao_relatorio_gestao_acao if percentual_execucao_fisica_acao_relatorio_gestao_acao is not None else True,
                models.RelatorioGestaoAcoes.observacoes_justificativas_relatorio_gestao_acao.ilike(f"%{observacoes_justificativas_relatorio_gestao_acao}%") if observacoes_justificativas_relatorio_gestao_acao is not None else True,
                models.RelatorioGestaoAcoes.id_relatorio_gestao == id_relatorio_gestao if id_relatorio_gestao is not None else True,
                models.RelatorioGestaoAcoes.id_acao_meta_plano_acao == id_acao_meta_plano_acao if id_acao_meta_plano_acao is not None else True
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