from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedTermoAdesaoResponse
from datetime import date
from typing import Optional
from src.cache import cache


ta_router = APIRouter(tags=["Termo de Adesão"])


@ta_router.get("/termo_adesao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Termo de Adesão - FaF.",
                response_description="Lista Paginada de Termos de Adesão - FaF",
                response_model=PaginatedTermoAdesaoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_termo_adesao_faf(
    id_termo_adesao: Optional[int] = Query(None, description="Identificador Único do Termo de Adesão"),
    numero_processo_termo_adesao: Optional[str] = Query(None, description="Número do Processo do Termo de Adesão"),
    situacao_termo_adesao: Optional[str] = Query(None, description="Situação do Termo de Adesão (Podendo ser: Em Elaboração; Enviado para o Recebedor; Assinado)"),
    objeto_termo_adesao: Optional[str] = Query(None, description="Objeto do Termo de Adesão"),
    data_assinatura_termo_adesao: Optional[str] = Query(None, description="Data de Assinatura do Termo de Adesão", pattern="^\d{4}-\d{2}-\d{2}$"),
    ano_termo_adesao: Optional[int] = Query(None, description="Ano do Termo de Adesão", gt=0),
    secao_publicacao_dou_termo_adesao: Optional[int] = Query(None, description="Seção no DOU (Diário Oficial da União) do Termo de Adesão"),
    pagina_publicacao_dou_termo_adesao: Optional[int] = Query(None, description="Página no DOU (Diário Oficial da União) do Termo de Adesão", gt=0),
    data_publicacao_dou_termo_adesao: Optional[str] = Query(None, description="Data da Publicação no DOU (Diário Oficial da União) do Termo de Adesão", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.TermoAdesao).where(
            and_(
                models.TermoAdesao.id_termo_adesao == id_termo_adesao if id_termo_adesao is not None else True,
                models.TermoAdesao.numero_processo_termo_adesao == numero_processo_termo_adesao if numero_processo_termo_adesao is not None else True,
                models.TermoAdesao.situacao_termo_adesao.ilike(f"%{situacao_termo_adesao}%") if situacao_termo_adesao is not None else True,
                models.TermoAdesao.objeto_termo_adesao == objeto_termo_adesao if objeto_termo_adesao is not None else True,
                cast(models.TermoAdesao.data_assinatura_termo_adesao, Date) == date.fromisoformat(data_assinatura_termo_adesao) if data_assinatura_termo_adesao is not None else True,
                models.TermoAdesao.ano_termo_adesao == ano_termo_adesao if ano_termo_adesao is not None else True,
                models.TermoAdesao.secao_publicacao_dou_termo_adesao == secao_publicacao_dou_termo_adesao if secao_publicacao_dou_termo_adesao is not None else True,
                models.TermoAdesao.pagina_publicacao_dou_termo_adesao == pagina_publicacao_dou_termo_adesao if pagina_publicacao_dou_termo_adesao is not None else True,
                cast(models.TermoAdesao.data_publicacao_dou_termo_adesao, Date) == date.fromisoformat(data_publicacao_dou_termo_adesao) if data_publicacao_dou_termo_adesao is not None else True,
                models.TermoAdesao.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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