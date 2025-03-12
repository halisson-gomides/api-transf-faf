from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaBeneficiarioResponse
from datetime import date
from typing import Optional
from src.cache import cache


pgb_router = APIRouter(tags=["Programa - Beneficiário"])


@pgb_router.get("/programa_beneficiario",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Beneficiários dos Programas - FaF.",
                response_description="Lista Paginada de Beneficiários dos Programas - FaF",
                response_model=PaginatedProgramaBeneficiarioResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_programa_beneficiario_faf(
    id_beneficiario_programa: Optional[int] = Query(None, description="Identificador Único do Beneficiário do Programa"),
    cnpj_beneficiario_programa: Optional[str] = Query(None, description="CNPJ do Beneficiário do Programa"),
    nome_beneficiario_programa: Optional[str] = Query(None, description="Nome do Beneficiário do Programa"),
    valor_beneficiario_programa: Optional[float] = Query(None, description="Valor Destinado ao Beneficiário do Programa", ge=0),
    numero_emenda_beneficiario_programa: Optional[str] = Query(None, description="Número da Emenda do Beneficiário do Programa"),
    nome_parlamentar_beneficiario_programa: Optional[str] = Query(None, description="Nome do Parlamentar Autor da Emenda do Beneficiário do Programa"),
    tipo_beneficiario_programa: Optional[str] = Query(None, description="Tipo do Beneficiário do Programa"),
    uf_beneficiario_programa: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Beneficiário do Programa"),
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
        query = select(models.ProgramaBeneficiario).where(
            and_(
                models.ProgramaBeneficiario.id_beneficiario_programa == id_beneficiario_programa if id_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.cnpj_beneficiario_programa == cnpj_beneficiario_programa if cnpj_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.nome_beneficiario_programa.ilike(f"%{nome_beneficiario_programa}%") if nome_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.valor_beneficiario_programa == valor_beneficiario_programa if valor_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.numero_emenda_beneficiario_programa == numero_emenda_beneficiario_programa if numero_emenda_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.nome_parlamentar_beneficiario_programa == nome_parlamentar_beneficiario_programa if nome_parlamentar_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.tipo_beneficiario_programa.ilike(f"%{tipo_beneficiario_programa}%") if tipo_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.uf_beneficiario_programa == uf_beneficiario_programa if uf_beneficiario_programa is not None else True,
                models.ProgramaBeneficiario.id_programa == id_programa if id_programa is not None else True
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