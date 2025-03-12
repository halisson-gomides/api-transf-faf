from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaGestaoAgilResponse
from datetime import date
from typing import Optional
from src.cache import cache


pgga_router = APIRouter(tags=["Programa - Gestão Ágil"])


@pgga_router.get("/programa_gestao_agil",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Programas cadastrados no Sistema Gestão Ágil - FaF.",
                response_description="Lista Paginada de Programas cadastrados no Sistema Gestão Ágil - FaF",
                response_model=PaginatedProgramaGestaoAgilResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_programa_gestao_agil_faf(
    id_programa_agil: Optional[int] = Query(None, description="Identificador Único do Programa Ágil"),
    id_programa_agil_bb: Optional[int] = Query(None, description="Identificador Único do Programa no Sistema Gestão Ágil no cadastro do Programa no Sistema Gestão Ágil"),
    nome_programa_agil: Optional[str] = Query(None, description="Nome do Programa no Sistema de Gestão Ágil BB"),
    codigo_programa_agil: Optional[str] = Query(None, description="Código do Programa no Sistema de Gestão Ágil BB"),
    codigo_siorg_orgao_programa_agil: Optional[int] = Query(None, description="Código SIORG do Órgão do Programa"),
    sigla_orgao_programa_agil: Optional[str] = Query(None, description="Sigla do Órgão do Programa"),
    cnpj_orgao_programa_agil: Optional[str] = Query(None, description="CNPJ do Órgão do Programa"),
    nome_orgao_programa_agil: Optional[str] = Query(None, description="Nome do Órgão do Programa"),
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
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
        query = select(models.ProgramaGestaoAgil).where(
            and_(
                models.ProgramaGestaoAgil.id_programa_agil == id_programa_agil if id_programa_agil is not None else True,
                models.ProgramaGestaoAgil.id_programa_agil_bb == id_programa_agil_bb if id_programa_agil_bb is not None else True,
                models.ProgramaGestaoAgil.nome_programa_agil.ilike(f"%{nome_programa_agil}%") if nome_programa_agil is not None else True,
                models.ProgramaGestaoAgil.codigo_programa_agil == codigo_programa_agil if codigo_programa_agil is not None else True,
                models.ProgramaGestaoAgil.codigo_siorg_orgao_programa_agil == codigo_siorg_orgao_programa_agil if codigo_siorg_orgao_programa_agil is not None else True,
                models.ProgramaGestaoAgil.sigla_orgao_programa_agil == sigla_orgao_programa_agil if sigla_orgao_programa_agil is not None else True,
                models.ProgramaGestaoAgil.cnpj_orgao_programa_agil == cnpj_orgao_programa_agil if cnpj_orgao_programa_agil is not None else True,
                models.ProgramaGestaoAgil.nome_orgao_programa_agil.ilike(f"%{nome_orgao_programa_agil}%") if nome_orgao_programa_agil is not None else True,
                models.ProgramaGestaoAgil.id_programa == id_programa if id_programa is not None else True
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