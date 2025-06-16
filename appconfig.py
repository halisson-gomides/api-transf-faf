
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    CACHE_SERVER_URL: str        
    CACHE_TTL: str = "30m"      
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_TAGS: list = [
        {
            "name": "Programa",
            "description": "Dados relativos aos Programas - FaF.",
        },
        {
            "name": "Programa - Beneficiário",
            "description": "Dados relativos aos Beneficiários dos Programas - FaF.",
        },
        {
            "name": "Programa - Gestão Ágil",
            "description": "Dados relativos aos Programas cadastrados no Sistema Gestão Ágil - FaF.",
        },
        {
            "name": "Plano de Ação",
            "description": "Dados relativos a Planos de Ação - FaF.",
        },
        {
            "name": "Plano de Ação - Dado Bancário",
            "description": "Dados relativos a Dado Bancário - FaF.",
        },
        {
            "name": "Plano de Ação - Meta",
            "description": "Dados relativos às Metas dos Planos de Ação - FaF.",
        },
        {
            "name": "Plano de Ação - Ações da Meta",
            "description": "Dados relativos às Ações das Metas dos Planos de Ação - FaF.",
        },
        {
            "name": "Plano de Ação - Destinação de Recursos",
            "description": "Dados relativos aos Itens de Despesa dos Planos de Ação - FaF",
        },
        {
            "name": "Plano de Ação - Análise",
            "description": "Dados relativos às Análises dos Planos de Ação - FaF",
        },
        {
            "name": "Plano de Ação - Responsável pela Análise",
            "description": "Dados relativos aos Responsáveis pela Análise dos Planos de Ação - FaF.",
        },
        {
            "name": "Plano de Ação - Histórico",
            "description": "Dados relativos ao Histórico do Plano de Ação - FaF",
        },
        {
            "name": "Termo de Adesão",
            "description": "Dados relativos aos Termos de Adesão - FaF",
        },
        {
            "name": "Termo de Adesão - Histórico",
            "description": "Dados relativos ao Histórico dos Termos de Adesão - FaF",
        },
        {
            "name": "Gestão Financeira - Lançamentos",
            "description": "Dados relativos a Lançamentos - FaF",
        },
        {
            "name": "Gestão Financeira - Subtransações",
            "description": "Dados relativos a Subtransações - FaF",
        },
        {
            "name": "Gestão Financeira - Categorias de Despesa",
            "description": "Dados relativos a Categorias de Despesa - FaF",
        },
        {
            "name": "Empenho",
            "description": "Dados relativos a Empenhos de Despesa - FaF",
        },
        {
            "name": "Relatório de Gestão",
            "description": "Dados relativos a Relatórios de Gestão - FaF",
        },
        {
            "name": "Relatório de Gestão - Ações",
            "description": "Dados relativos às Ações associadas ao Relatório de Gestão - FaF",
        },
        {
            "name": "Relatório de Gestão - Análise",
            "description": "Dados relativos às Análises associadas ao Relatório de Gestão - FaF",
        },
        {
            "name": "Relatório de Gestão - Responsável pela Análise",
            "description": "Dados relativos aos Responsáveis pela Análise do Relatório de Gestão - FaF",
        },
    ]
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    ERROR_MESSAGE_NO_PARAMS: str = "Nenhum parâmetro de consulta foi informado."
    ERROR_MESSAGE_INTERNAL: str = "Erro Interno Inesperado."
    STATS_USER: str 
    STATS_PASSWORD: str 