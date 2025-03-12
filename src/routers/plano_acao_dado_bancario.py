from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoDadoBancarioResponse
from datetime import date
from typing import Optional
from src.cache import cache


padb_router = APIRouter(tags=["Plano de Ação - Dado Bancário"])


@padb_router.get("/plano_acao_dado_bancario",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos Dados Bancários dos Planos de Ação - FaF.",
                response_description="Lista Paginada de Dados Bancários dos Planos de Ação - FaF",
                response_model=PaginatedPlanoAcaoDadoBancarioResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_acao_dado_bancario_faf(
    id_plano_acao_dado_bancario: Optional[int] = Query(None, description="Identificador Único do Dado Bancário do Plano de Ação"),
    id_agencia_conta: Optional[str] = Query(None, description="Número da Agência seguido do caracter '-' seguido do Número da Conta do Dado Bancário do Plano de Ação"),
    codigo_banco_plano_acao_dado_bancario: Optional[int] = Query(None, description="Código do Banco do Dado Bancário do Plano de Ação"),
    nome_banco_plano_acao_dado_bancario: Optional[str] = Query(None, description="Nome do Banco do Dado Bancário do Plano de Ação"),
    numero_agencia_plano_acao_dado_bancario: Optional[int] = Query(None, description="Número da Agência do Dado Bancário do Plano de Ação"),
    dv_agencia_plano_acao_dado_bancario: Optional[str] = Query(None, description="Dígito Verificador (DV) da Agência do Dado Bancário do Plano de Ação"),
    numero_conta_plano_acao_dado_bancario: Optional[int] = Query(None, description="Número da Conta Corrente do Dado Bancário do Plano de Ação"),
    dv_conta_plano_acao_dado_bancario: Optional[str] = Query(None, description="Dígito Verificador (DV) da Conta Corrente do Dado Bancário do Plano de Ação"),
    situacao_conta_plano_acao_dado_bancario: Optional[str] = Query(None, description="Descrição da Situação Dado Bancário do Plano de Ação"),
    data_abertura_conta_plano_acao_dado_bancario: Optional[str] = Query(None, description="Data de Abertura da Conta Corrente do Dado Bancário do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    nome_programa_agil_conta_plano_acao_dado_bancario: Optional[str] = Query(None, description="Nome do Programa Gestão Ágil do Dado Bancário do Plano de Ação"),
    saldo_final_conta_plano_acao_dado_bancario: Optional[float] = Query(None, description="Saldo Final na Conta Corrente do Dado Bancário do Plano de Ação"),
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
        query = select(models.PlanoAcaoDadoBancario).where(
            and_(
                models.PlanoAcaoDadoBancario.id_plano_acao_dado_bancario == id_plano_acao_dado_bancario if id_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.id_agencia_conta == id_agencia_conta if id_agencia_conta is not None else True,
                models.PlanoAcaoDadoBancario.codigo_banco_plano_acao_dado_bancario == codigo_banco_plano_acao_dado_bancario if codigo_banco_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.nome_banco_plano_acao_dado_bancario.ilike(f"%{nome_banco_plano_acao_dado_bancario}%") if nome_banco_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.numero_agencia_plano_acao_dado_bancario == numero_agencia_plano_acao_dado_bancario if numero_agencia_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.dv_agencia_plano_acao_dado_bancario == dv_agencia_plano_acao_dado_bancario if dv_agencia_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.numero_conta_plano_acao_dado_bancario == numero_conta_plano_acao_dado_bancario if numero_conta_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.dv_conta_plano_acao_dado_bancario == dv_conta_plano_acao_dado_bancario if dv_conta_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.situacao_conta_plano_acao_dado_bancario.ilike(f"%{situacao_conta_plano_acao_dado_bancario}%") if situacao_conta_plano_acao_dado_bancario is not None else True,
                cast(models.PlanoAcaoDadoBancario.data_abertura_conta_plano_acao_dado_bancario, Date) == date.fromisoformat(data_abertura_conta_plano_acao_dado_bancario) if data_abertura_conta_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.nome_programa_agil_conta_plano_acao_dado_bancario.ilike(f"%{nome_programa_agil_conta_plano_acao_dado_bancario}%") if nome_programa_agil_conta_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.saldo_final_conta_plano_acao_dado_bancario == saldo_final_conta_plano_acao_dado_bancario if saldo_final_conta_plano_acao_dado_bancario is not None else True,
                models.PlanoAcaoDadoBancario.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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