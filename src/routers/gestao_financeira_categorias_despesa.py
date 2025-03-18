from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedGestaoFinanceiraCategoriasDespesaResponse
from datetime import date
from typing import Optional, Literal
from src.cache import cache


gfcd_router = APIRouter(tags=["Gestão Financeira - Categorias de Despesa"])


@gfcd_router.get("/gestao_financeira_categorias_despesa",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Categorias de Despesa - FaF.",
                response_description="Lista Paginada de Categorias de Despesa - FaF",
                response_model=PaginatedGestaoFinanceiraCategoriasDespesaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_gestao_financeira_categorias_despesa_faf(
    id_categoria_despesa_gestao_financeira: Optional[int] = Query(None, description="Identificador Único da Categoria de Despesa"),
    id_nivel_pai_categoria_despesa_gestao_financeira: Optional[int] = Query(None, description="Identificador Único da Categoria Pai da Categoria de Despesa"),
    nome_nivel_atual_categoria_despesa_gestao_financeira: Optional[str] = Query(None, description="Nome da Categoria de Despesa"),
    nivel_atual_categoria_despesa_gestao_financeira: Optional[int] = Query(None, description="Nível Atual da Hierarquia da Categoria de Despesa (onde 0 representa o primeiro nível)"),
    nome_completo_niveis_categoria_despesa_gestao_financeira: Optional[str] = Query(None, description="Caminho Completo da Estrutura Hierárquica da Categoria de Despesa"),
    codigo_programa_agil: Optional[int] = Query(None, description="Código do Programa no Sistema de Gestão Ágil BB"),
    nome_programa_agil: Optional[str] = Query(None, description="Nome do Programa no Sistema de Gestão Ágil BB"),
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
        query = select(models.GestaoFinanceiraCategoriasDespesa).where(
            and_(
                models.GestaoFinanceiraCategoriasDespesa.id_categoria_despesa_gestao_financeira == id_categoria_despesa_gestao_financeira if id_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.id_nivel_pai_categoria_despesa_gestao_financeira == id_nivel_pai_categoria_despesa_gestao_financeira if id_nivel_pai_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.nome_nivel_atual_categoria_despesa_gestao_financeira.ilike(f"%{nome_nivel_atual_categoria_despesa_gestao_financeira}%") if nome_nivel_atual_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.nivel_atual_categoria_despesa_gestao_financeira == nivel_atual_categoria_despesa_gestao_financeira if nivel_atual_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.nome_completo_niveis_categoria_despesa_gestao_financeira.ilike(f"%{nome_completo_niveis_categoria_despesa_gestao_financeira}%") if nome_completo_niveis_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.codigo_programa_agil == codigo_programa_agil if codigo_programa_agil is not None else True,
                models.GestaoFinanceiraCategoriasDespesa.nome_programa_agil.ilike(f"%{nome_programa_agil}%") if nome_programa_agil is not None else True
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