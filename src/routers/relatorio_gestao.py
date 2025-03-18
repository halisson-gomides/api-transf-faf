from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date, Time, func
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedRelatorioGestaoResponse
from datetime import date
from typing import Optional, Literal
from src.cache import cache


rg_router = APIRouter(tags=["Relatório de Gestão"])


@rg_router.get("/relatorio_gestao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Relatórios de Gestão - FaF.",
                response_description="Lista Paginada de Relatório de Gestão - FaF",
                response_model=PaginatedRelatorioGestaoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_relatorio_gestao_faf(
    id_relatorio_gestao: Optional[int] = Query(None, description="Identificador Único do Relatório de Gestão"),
    data_relatorio_gestao: Optional[date] = Query(None, description="Data do Envio do Relatório de Gestão", pattern="^\d{4}-\d{2}-\d{2}$"),
    hora_relatorio_gestao: Optional[str] = Query(None, description="Data e Hora do Envio do Relatório de Gestão", pattern="^\d{2}:\d{2}$"),
    tipo_relatorio_gestao: Literal['PARCIAL','FINAL'] = Query(None, description="Tipo do Relatório de Gestão: ('PARCIAL' ou 'FINAL')"),
    situacao_relatorio_gestao: Literal['EM_ELABORACAO', 'ENVIADO_ANALISE_CONSELHO', 'ENVIADO_ANALISE', 'EM_COMPLEMENTACAO', 'ANALISE_CONCLUIDA_CONSELHO', 'ANALISE_CONCLUIDA', 'REJEITADO'] = Query(None, description="Situação do Relatório de Gestão: ('EM_ELABORACAO', 'ENVIADO_ANALISE_CONSELHO', 'ENVIADO_ANALISE', 'EM_COMPLEMENTACAO', 'ANALISE_CONCLUIDA_CONSELHO', 'ANALISE_CONCLUIDA', 'REJEITADO')"),
    valor_executado_relatorio_gestao: Optional[float] = Query(None, description="Valor Repassado do Relatório de Gestão", ge=0),
    valor_pendente_relatorio_gestao: Optional[float] = Query(None, description="Valor Pendente do Relatório de Gestão", ge=0),
    resultados_alcancados_metas_relatorio_gestao: Optional[str] = Query(None, description="Resultados Alcançados do Relatório de Gestão"),
    descritivo_relatorio_gestao: Optional[str] = Query(None, description="Descritivo do Parecer do Relatório de Gestão"),
    contrapartida_relatorio_gestao: Optional[str] = Query(None, description="Contrapartida do Relatório de Gestão"),
    endereco_eletronico_publicidade_acoes_relatorio_gestao: Optional[str] = Query(None, description="URL de Publicidade das Ações Pactuadas no Relatório de Gestão"),
    declaracao_conformidade_relatorio_gestao: Optional[bool] = Query(None, description="Indicador da Declaração de Conformidade do Relatório de Gestão"),
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
        query = select(models.RelatorioGestao).where(
            and_(
                models.RelatorioGestao.id_relatorio_gestao == id_relatorio_gestao if id_relatorio_gestao is not None else True,
                cast(models.RelatorioGestao.data_relatorio_gestao, Date) == date.fromisoformat(data_relatorio_gestao) if data_relatorio_gestao is not None else True,
                func.to_char(cast(models.RelatorioGestao.data_e_hora_relatorio_gestao, Time), 'HH24:MI') == hora_relatorio_gestao if hora_relatorio_gestao is not None else True,
                models.RelatorioGestao.tipo_relatorio_gestao == tipo_relatorio_gestao if tipo_relatorio_gestao is not None else True,
                models.RelatorioGestao.situacao_relatorio_gestao == situacao_relatorio_gestao if situacao_relatorio_gestao is not None else True,
                models.RelatorioGestao.valor_executado_relatorio_gestao == valor_executado_relatorio_gestao if valor_executado_relatorio_gestao is not None else True,
                models.RelatorioGestao.valor_pendente_relatorio_gestao == valor_pendente_relatorio_gestao if valor_pendente_relatorio_gestao is not None else True,
                models.RelatorioGestao.resultados_alcancados_metas_relatorio_gestao.ilike(f"%{resultados_alcancados_metas_relatorio_gestao}%") if resultados_alcancados_metas_relatorio_gestao is not None else True,
                models.RelatorioGestao.descritivo_relatorio_gestao.ilike(f"%{descritivo_relatorio_gestao}%") if descritivo_relatorio_gestao is not None else True,
                models.RelatorioGestao.contrapartida_relatorio_gestao.ilike(f"%{contrapartida_relatorio_gestao}%") if contrapartida_relatorio_gestao is not None else True,
                models.RelatorioGestao.endereco_eletronico_publicidade_acoes_relatorio_gestao.ilike(f"%{endereco_eletronico_publicidade_acoes_relatorio_gestao}%") if endereco_eletronico_publicidade_acoes_relatorio_gestao is not None else True,
                models.RelatorioGestao.declaracao_conformidade_relatorio_gestao == declaracao_conformidade_relatorio_gestao if declaracao_conformidade_relatorio_gestao is not None else True,
                models.RelatorioGestao.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
            )
        )
        # print(str(query))
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.__repr__())