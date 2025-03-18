from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedEmpenhoResponse
from datetime import date
from typing import Optional, Literal
from src.cache import cache


em_router = APIRouter(tags=["Empenho"])


@em_router.get("/empenho",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Empenhos de Despesa - FaF.",
                response_description="Lista Paginada de Empenhos de Despesa - FaF",
                response_model=PaginatedEmpenhoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_empenho_faf(
    id_empenho: Optional[int] = Query(None, description="Identificador Único da Nota de Empenho"),
    numero_empenho: Optional[str] = Query(None, description="Número da Nota de Empenho gerada e enviada pelo SIAFI (Sistema Integrado de Administração Financeira)"),
    ano_empenho: Optional[str] = Query(None, description="Ano do Empenho", pattern="^\d{4}"),
    gestao_emitente_empenho: Optional[str] = Query(None, description="Gestão Emitente no SIAFI"),
    ug_emitente_empenho: Optional[str] = Query(None, description="Unidade Gestora Emitente no SIAFI"),
    data_emissao_empenho: Optional[date] = Query(None, description="Data da Emissão da Nota de Empenho", pattern="^\d{4}-\d{2}-\d{2}$"),
    fonte_recurso_empenho: Optional[str] = Query(None, description="Fonte de Recurso da Nota de Empenho no SIAFI"),
    esfera_orcamentaria_empenho: Literal['0', '1', '2', '3', '4', '5'] = Query(None, description="Indicador da Esfera Orçamentária podendo assumir os seguintes valores: (0, 1, 2, 3, 4, 5)"),
    descricao_esfera_orcamentaria_empenho: Literal['Federal', 'Estadual', 'Municipal', 'Estatal', 'Privada', 'Organismos Internacionais'] = Query(None, description="Descrição do Indicador da Esfera Orçamentária podendo assumir os seguintes valores: (0 - 'Federal', 1 - 'Estadual'; 2 - 'Municipal'; 3 - 'Estatal'; 4 - 'Privada'; 5 - 'Organismos Internacionais')"),
    plano_interno_empenho: Optional[str] = Query(None, description="Instrumento de planejamento e de acompanhamento da ação planejada, usado como forma de detalhamento desta, de uso exclusivo de cada Ministério/órgão, com as seguintes características: - Há um atributo na tabela de órgão para indicar se o órgão utiliza ou não o Plano Interno (PI). Este atributo é mantido pela STN decorrente da solicitação do órgão. - A unidade setorial de orçamento do órgão é responsável por registrar na tabela os códigos de PI. - O SIAFI (Sistema Integrado de Administração Financeira), de acordo com o cadastramento previsto acima, só aceitará a emissão de nota de empenho com o código de PI existente. - Os códigos de PI poderão ter até 11 (onze) posições alfa-numéricas"),
    unidade_gestora_responsavel_empenho: Optional[str] = Query(None, description="Unidade Gestora do Favorecido"),
    observacao_empenho: Optional[str] = Query(None, description="Observação referente a Nota de Empenho informada pelo usuário"),
    cnpj_favorecido_empenho: Optional[str] = Query(None, description="CNPJ do Favorecido"),
    numero_lista_empenho: Optional[str] = Query(None, description="Número da Lista gerado e enviado pelo SIAFI"),
    unidade_gestora_referencia_empenho: Optional[str] = Query(None, description="Unidade Gestora de referência no SIAFI"),
    gestao_referencia_empenho: Optional[str] = Query(None, description="Gestão de referência no SIAFI"),
    numero_interno_empenho: Optional[int] = Query(None, description="Número Interno Sequencial"),
    objeto_empenho: Optional[str] = Query(None, description="Objeto da Nota de Empenho informado pelo usuário"),
    numero_sistema_empenho: Optional[str] = Query(None, description="Campo preenchido com Nota de Sistema “NS” ou Nota de Lançamento “NL”, pelo usuário, sobre Nota de Empenho registrada diretamente no SIAFI (Sistema Integrado de Administração Financeira), situação: 6 - “Registrado no Siafi”"),
    natureza_despesa_empenho: Optional[str] = Query(None, description="Identificador da tabela de Natureza Despesa, recuperado do SICONV"),
    natureza_despesa_sub_item_empenho: Optional[int] = Query(None, description="Identificador da tabela de Natureza Despesa Subitem, recuperado do SICONV"),
    tipo_empenho: Literal['1','3','5'] = Query(None, description="Tipo de Empenho podendo assumir os valores: (1, 3, 5)"),
    descricao_tipo_empenho: Literal['Empenho Ordinário','Estimado','Global'] = Query(None, description="Descrição do Tipo de Empenho podendo assumir os valores: (1 - 'Empenho Ordinário'; 3 - 'Estimado'; 5 - 'Global')"),
    codigo_tipo_nota_empenho: Optional[str] = Query(None, description="Código do Tipo da Nota de Empenho"),
    descricao_tipo_nota_empenho: Optional[str] = Query(None, description="Descrição do Tipo da Nota de Empenho"),
    situacao_empenho: Literal['1', '4', '5', '6'] = Query(None, description="Situação da Nota de Empenho, podendo assumir os valores: (1, 4, 5, 6)"),
    descricao_situacao_empenho: Literal['Minuta de Empenho','Enviado','Pendente','Registrado no SIAFI'] = Query(None, description="Descrição da Situação da Nota de Empenho, podendo assumir os valores: (1 - 'Minuta de Empenho'; 4 - 'Enviado'; 5 - 'Pendente'; 6 - 'Registrado no SIAFI')"),
    valor_empenho: Optional[float] = Query(None, description="Valor Total da Nota de Empenho", ge=0),
    versao_empenho: Optional[int] = Query(None, description="Versão da Nota de Empenho"),
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
        query = select(models.Empenho).where(
            and_(
                models.Empenho.id_empenho == id_empenho if id_empenho is not None else True,
                models.Empenho.numero_empenho == numero_empenho if numero_empenho is not None else True,
                models.Empenho.ano_empenho == ano_empenho if ano_empenho is not None else True,
                models.Empenho.gestao_emitente_empenho == gestao_emitente_empenho if gestao_emitente_empenho is not None else True,
                models.Empenho.ug_emitente_empenho == ug_emitente_empenho if ug_emitente_empenho is not None else True,
                cast(models.Empenho.data_emissao_empenho, Date) == date.fromisoformat(data_emissao_empenho) if data_emissao_empenho is not None else True,
                models.Empenho.fonte_recurso_empenho == fonte_recurso_empenho if fonte_recurso_empenho is not None else True,
                models.Empenho.esfera_orcamentaria_empenho == int(esfera_orcamentaria_empenho) if esfera_orcamentaria_empenho is not None else True,
                models.Empenho.descricao_esfera_orcamentaria_empenho.ilike(f"%{descricao_esfera_orcamentaria_empenho}%") if descricao_esfera_orcamentaria_empenho is not None else True,
                models.Empenho.plano_interno_empenho == plano_interno_empenho if plano_interno_empenho is not None else True,
                models.Empenho.unidade_gestora_responsavel_empenho == unidade_gestora_responsavel_empenho if unidade_gestora_responsavel_empenho is not None else True,
                models.Empenho.observacao_empenho.ilike(f"%{observacao_empenho}%") if observacao_empenho is not None else True,
                models.Empenho.cnpj_favorecido_empenho == cnpj_favorecido_empenho if cnpj_favorecido_empenho is not None else True,
                models.Empenho.numero_lista_empenho == numero_lista_empenho if numero_lista_empenho is not None else True,
                models.Empenho.unidade_gestora_referencia_empenho == unidade_gestora_referencia_empenho if unidade_gestora_referencia_empenho is not None else True,
                models.Empenho.gestao_referencia_empenho == gestao_referencia_empenho if gestao_referencia_empenho is not None else True,
                models.Empenho.numero_interno_empenho == numero_interno_empenho if numero_interno_empenho is not None else True,
                models.Empenho.objeto_empenho.ilike(f"%{objeto_empenho}%") if objeto_empenho is not None else True,
                models.Empenho.numero_sistema_empenho == numero_sistema_empenho if numero_sistema_empenho is not None else True,
                models.Empenho.natureza_despesa_empenho == natureza_despesa_empenho if natureza_despesa_empenho is not None else True,
                models.Empenho.natureza_despesa_sub_item_empenho == natureza_despesa_sub_item_empenho if natureza_despesa_sub_item_empenho is not None else True,
                models.Empenho.tipo_empenho == int(tipo_empenho) if tipo_empenho is not None else True,
                models.Empenho.descricao_tipo_empenho == descricao_tipo_empenho if descricao_tipo_empenho is not None else True,
                models.Empenho.codigo_tipo_nota_empenho == codigo_tipo_nota_empenho if codigo_tipo_nota_empenho is not None else True,
                models.Empenho.descricao_tipo_nota_empenho.ilike(f"%{descricao_tipo_nota_empenho}%") if descricao_tipo_nota_empenho is not None else True,
                models.Empenho.situacao_empenho == int(situacao_empenho) if situacao_empenho is not None else True,
                models.Empenho.descricao_situacao_empenho.ilike(f"%{descricao_situacao_empenho}%") if descricao_situacao_empenho is not None else True,
                models.Empenho.valor_empenho == valor_empenho if valor_empenho is not None else True,
                models.Empenho.versao_empenho == versao_empenho if versao_empenho is not None else True,
                models.Empenho.id_plano_acao == id_plano_acao if id_plano_acao is not None else True
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