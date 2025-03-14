from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedGestaoFinanceiraLancamentosResponse
from datetime import date
from typing import Optional, Literal
from src.cache import cache


gfl_router = APIRouter(tags=["Gestão Financeira - Lançamentos"])


@gfl_router.get("/gestao_financeira_lancamentos",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Lançamentos - FaF.",
                response_description="Lista Paginada de Lançamentos - FaF",
                response_model=PaginatedGestaoFinanceiraLancamentosResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_gestao_financeira_lancamentos_faf(
    id_lancamento_gestao_financeira: Optional[int] = Query(None, description="Identificador Único do Lançamento"),
    origem_solicitacao_gestao_financeira: Literal['TFF', 'TE'] = Query(None, description="Origem da solicitação de abertura de contas: ('TFF' ou 'TE')"),
    descricao_origem_solicitacao_gestao_financeira: Optional[str] = Query(None, description="Descrição da Origem da solicitação de abertura de contas: ('Transferências Fundo a Fundo' ou 'Transferências Especiais')"),
    cnpj_ente_solicitante_gestao_financeira: Optional[str] = Query(None, description="CNPJ do Ente Solicitante da Conta Bancária"),
    nome_ente_solicitante_gestao_financeira: Optional[str] = Query(None, description="Nome do Ente Solicitante da Conta Bancária"),
    nome_personalizado_ente_solicitante_gestao_financeira: Optional[str] = Query(None, description="Nome Personalizado do Ente Solicitante da Conta Bancária"),
    codigo_programa_agil_ente_solicitante_gestao_financeira: Optional[str] = Query(None, description="Código do Programa Ágil cadastrado no BB"),
    codigo_banco_gestao_financeira: Optional[str] = Query(None, description="Código do Banco do Lançamento"),
    codigo_agencia_gestao_financeira: Optional[str] = Query(None, description="Número da Agência do Lançamento"),
    dv_agencia_gestao_financeira: Optional[str] = Query(None, description="Dígito Verificador (DV) da Agência do Lançamento"),
    codigo_conta_gestao_financeira: Optional[str] = Query(None, description="Número da Conta Corrente do Lançamento"),
    dv_conta_gestao_financeira: Optional[str] = Query(None, description="Dígito Verificador (DV) da Conta Corrente do Lançamento"),
    tipo_operacao_gestao_financeira: Literal['D', 'C'] = Query(None, description="Tipo da Operação ('D' ou 'C')"),
    descricao_tipo_operacao_gestao_financeira: Literal['Débito', 'Crédito'] = Query(None, description="Descrição do Tipo da Operação ('Débito' ou 'Crédito')"),
    descricao_gestao_financeira: Optional[str] = Query(None, description="Descrição do Lançamento"),
    data_lancamento_gestao_financeira: Optional[str] = Query(None, description="Data do Lançamento", pattern="^\d{4}-\d{2}-\d{2}$"),
    data_evento_lancamento_gestao_financeira: Optional[str] = Query(None, description="Data do Evento do Lançamento", pattern="^\d{4}-\d{2}-\d{2}$"),
    numero_ordem_gestao_financeira: Optional[int] = Query(None, description="Número de Ordem do Lançamento"),
    numero_referencia_unica_gestao_financeira: Optional[str] = Query(None, description="Número de Referência do Lançamento"),
    tipo_favorecido_gestao_financeira: Literal['1','2','0'] = Query(None, description="Tipo do Favorecido (1, 2 ou 0)"),
    descricao_tipo_favorecido_gestao_financeira: Literal['CPF', 'CNPJ', 'Não Identificado'] = Query(None, description="Descrição do Tipo do Favorecido (1 - 'CPF', 2 - 'CNPJ' ou 0 - 'Não Identificado')"),
    doc_favorecido_gestao_financeira_mask: Optional[str] = Query(None, description="Identificação do Favorecido do Lançamento"),
    nome_favorecido_gestao_financeira: Optional[str] = Query(None, description="Nome do Favorecido do Lançamento"),
    codigo_banco_favorecido_gestao_financeira: Optional[str] = Query(None, description="Código do Banco do Favorecido do Lançamento"),
    codigo_agencia_favorecido_gestao_financeira: Optional[str] = Query(None, description="Número da Agência do Favorecido do Lançamento"),
    dv_agencia_favorecido_gestao_financeira: Optional[str] = Query(None, description="Dígito Verificador (DV) da Agência do Favorecido do Lançamento"),
    codigo_conta_favorecido_gestao_financeira: Optional[str] = Query(None, description="Código da Conta do Favorecido do Lançamento"),
    dv_conta_favorecido_gestao_financeira: Optional[str] = Query(None, description="Dígito Verificador (DV) da Conta do Favorecido do Lançamento"),
    valor_lancamento_gestao_financeira: Optional[float] = Query(None, description="Valor do Lançamento"),
    id_categoria_despesa_gestao_financeira: Optional[int] = Query(None, description="Identificador da Categoria de Despesa da Plataforma"),
    quantidade_subtransacoes_lancamento_gestao_financeira: Optional[int] = Query(None, description="Quantidade de Subtransações do Lançamento"),
    id_agencia_conta: Optional[str] = Query(None, description="Número da Agência seguido do caracter '-' seguido do Número da Conta"),
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
        query = select(models.GestaoFinanceiraLancamentos).where(
            and_(
                models.GestaoFinanceiraLancamentos.id_lancamento_gestao_financeira == id_lancamento_gestao_financeira if id_lancamento_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.origem_solicitacao_gestao_financeira == origem_solicitacao_gestao_financeira if origem_solicitacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.descricao_origem_solicitacao_gestao_financeira.ilike(f"%{descricao_origem_solicitacao_gestao_financeira}%") if descricao_origem_solicitacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.cnpj_ente_solicitante_gestao_financeira.ilike(f"%{cnpj_ente_solicitante_gestao_financeira}%") if cnpj_ente_solicitante_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.nome_ente_solicitante_gestao_financeira.ilike(f"%{nome_ente_solicitante_gestao_financeira}%") if nome_ente_solicitante_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.nome_personalizado_ente_solicitante_gestao_financeira.ilike(f"%{nome_personalizado_ente_solicitante_gestao_financeira}%") if nome_personalizado_ente_solicitante_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_programa_agil_ente_solicitante_gestao_financeira == codigo_programa_agil_ente_solicitante_gestao_financeira if codigo_programa_agil_ente_solicitante_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_banco_gestao_financeira == codigo_banco_gestao_financeira if codigo_banco_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_agencia_gestao_financeira == codigo_agencia_gestao_financeira if codigo_agencia_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.dv_agencia_gestao_financeira == dv_agencia_gestao_financeira if dv_agencia_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_conta_gestao_financeira == codigo_conta_gestao_financeira if codigo_conta_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.dv_conta_gestao_financeira == dv_conta_gestao_financeira if dv_conta_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.tipo_operacao_gestao_financeira == tipo_operacao_gestao_financeira if tipo_operacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.descricao_tipo_operacao_gestao_financeira == descricao_tipo_operacao_gestao_financeira if descricao_tipo_operacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.descricao_gestao_financeira.ilike(f"%{descricao_gestao_financeira}%") if descricao_gestao_financeira is not None else True,
                cast(models.GestaoFinanceiraLancamentos.data_lancamento_gestao_financeira, Date) == date.fromisoformat(data_lancamento_gestao_financeira) if data_lancamento_gestao_financeira is not None else True,
                cast(models.GestaoFinanceiraLancamentos.data_evento_lancamento_gestao_financeira, Date) == date.fromisoformat(data_evento_lancamento_gestao_financeira) if data_evento_lancamento_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.numero_ordem_gestao_financeira == numero_ordem_gestao_financeira if numero_ordem_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.numero_referencia_unica_gestao_financeira == numero_referencia_unica_gestao_financeira if numero_referencia_unica_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.tipo_favorecido_gestao_financeira == int(tipo_favorecido_gestao_financeira) if tipo_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.descricao_tipo_favorecido_gestao_financeira.ilike(f"%{descricao_tipo_favorecido_gestao_financeira}%") if descricao_tipo_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.doc_favorecido_gestao_financeira_mask == doc_favorecido_gestao_financeira_mask if doc_favorecido_gestao_financeira_mask is not None else True,
                models.GestaoFinanceiraLancamentos.nome_favorecido_gestao_financeira.ilike(f"%{nome_favorecido_gestao_financeira}%") if nome_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_banco_favorecido_gestao_financeira == codigo_banco_favorecido_gestao_financeira if codigo_banco_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_agencia_favorecido_gestao_financeira == codigo_agencia_favorecido_gestao_financeira if codigo_agencia_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.dv_agencia_favorecido_gestao_financeira == dv_agencia_favorecido_gestao_financeira if dv_agencia_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.codigo_conta_favorecido_gestao_financeira == codigo_conta_favorecido_gestao_financeira if codigo_conta_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.dv_conta_favorecido_gestao_financeira == dv_conta_favorecido_gestao_financeira if dv_conta_favorecido_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.valor_lancamento_gestao_financeira == valor_lancamento_gestao_financeira if valor_lancamento_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.id_categoria_despesa_gestao_financeira == id_categoria_despesa_gestao_financeira if id_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.quantidade_subtransacoes_lancamento_gestao_financeira == quantidade_subtransacoes_lancamento_gestao_financeira if quantidade_subtransacoes_lancamento_gestao_financeira is not None else True,
                models.GestaoFinanceiraLancamentos.id_agencia_conta == id_agencia_conta if id_agencia_conta is not None else True
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