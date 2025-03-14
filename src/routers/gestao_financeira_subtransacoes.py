from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedGestaoFinanceiraSubtransacoesResponse
from datetime import date
from typing import Optional, Literal
from src.cache import cache


gfs_router = APIRouter(tags=["Gestão Financeira - Subtransações"])


@gfs_router.get("/gestao_financeira_subtransacoes",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Subtransações - FaF.",
                response_description="Lista Paginada de Subtransações - FaF",
                response_model=PaginatedGestaoFinanceiraSubtransacoesResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_gestao_financeira_subtransacoes_faf(
    id_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Identificador Único da Subtransação"),
    estado_subtransacao_gestao_financeira: Optional[int] = Query(None, description="Estado da Subtransação"),
    situacao_pagamento_subtransacao_gestao_financeira: Literal['3','6'] = Query(None, description="Situação do Pagamento (3, 6)"),
    descricao_situacao_pagamento_subtransacao_gestao_financeira: Literal['Pago', 'Cancelado'] = Query(None, description="Descrição da Situação do Pagamento (3 - 'Pago', 6 - 'Cancelado')"),
    data_pagamento_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Data do Pagamento da Subtransação", pattern="^\d{4}-\d{2}-\d{2}$"),
    tipo_pessoa_beneficiario_subtransacao_gestao_financeira: Literal['1','2','0'] = Query(None, description="Tipo do Favorecido (1, 2 ou 0) da Subtransação"),
    descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei: Literal['CPF', 'CNPJ', 'Não Identificado'] = Query(None, description="Descrição do Tipo do Favorecido (1 - 'CPF', 2 - 'CNP'J ou 0 - 'Não Identificado') da Subtransação"),
    numero_documento_beneficiario_subtransacao_gestao_financeira_ma: Optional[str] = Query(None, description="Identificação do Favorecido da Subtransação"),
    nome_beneficiario_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Nome do Favorecido da Subtransação"),
    codigo_banco_beneficiario_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Código do Banco do Favorecido da Subtransação"),
    codigo_agencia_beneficiario_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Número da Agência do Favorecido da Subtransação"),
    codigo_conta_beneficiario_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Número da Conta do Favorecido da Subtransação"),
    descricao_subtransacao_gestao_financeira: Optional[str] = Query(None, description="Descrição da Subtransação"),
    valor_subtransacao_gestao_financeira: Optional[float] = Query(None, description="Valor do Pagamento", ge=0),
    id_categoria_despesa_gestao_financeira: Optional[int] = Query(None, description="Identificador da Categoria de Despesa do Banco do Brasil"),
    id_lancamento_gestao_financeira: Optional[int] = Query(None, description="Identificador Único do Lançamento"),
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
        query = select(models.GestaoFinanceiraSubtransacoes).where(
            and_(
                models.GestaoFinanceiraSubtransacoes.id_subtransacao_gestao_financeira == id_subtransacao_gestao_financeira if id_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.estado_subtransacao_gestao_financeira == estado_subtransacao_gestao_financeira if estado_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.situacao_pagamento_subtransacao_gestao_financeira == int(situacao_pagamento_subtransacao_gestao_financeira) if situacao_pagamento_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.descricao_situacao_pagamento_subtransacao_gestao_financeira == descricao_situacao_pagamento_subtransacao_gestao_financeira if descricao_situacao_pagamento_subtransacao_gestao_financeira is not None else True,
                cast(models.GestaoFinanceiraSubtransacoes.data_pagamento_subtransacao_gestao_financeira, Date) == date.fromisoformat(data_pagamento_subtransacao_gestao_financeira) if data_pagamento_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.tipo_pessoa_beneficiario_subtransacao_gestao_financeira == int(tipo_pessoa_beneficiario_subtransacao_gestao_financeira) if tipo_pessoa_beneficiario_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei == descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei if descricao_tipo_pessoa_beneficiario_subtransacao_gestao_financei is not None else True,
                models.GestaoFinanceiraSubtransacoes.numero_documento_beneficiario_subtransacao_gestao_financeira_ma == numero_documento_beneficiario_subtransacao_gestao_financeira_ma if numero_documento_beneficiario_subtransacao_gestao_financeira_ma is not None else True,
                models.GestaoFinanceiraSubtransacoes.nome_beneficiario_subtransacao_gestao_financeira.ilike(f"%{nome_beneficiario_subtransacao_gestao_financeira}%") if nome_beneficiario_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.codigo_banco_beneficiario_subtransacao_gestao_financeira == codigo_banco_beneficiario_subtransacao_gestao_financeira if codigo_banco_beneficiario_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.codigo_agencia_beneficiario_subtransacao_gestao_financeira == codigo_agencia_beneficiario_subtransacao_gestao_financeira if codigo_agencia_beneficiario_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.codigo_conta_beneficiario_subtransacao_gestao_financeira == codigo_conta_beneficiario_subtransacao_gestao_financeira if codigo_conta_beneficiario_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.descricao_subtransacao_gestao_financeira.ilike(f"%{descricao_subtransacao_gestao_financeira}%") if descricao_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.valor_subtransacao_gestao_financeira == valor_subtransacao_gestao_financeira if valor_subtransacao_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.id_categoria_despesa_gestao_financeira == id_categoria_despesa_gestao_financeira if id_categoria_despesa_gestao_financeira is not None else True,
                models.GestaoFinanceiraSubtransacoes.id_lancamento_gestao_financeira == id_lancamento_gestao_financeira if id_lancamento_gestao_financeira is not None else True
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