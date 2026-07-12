from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Ateliê Digital - Log Service'
    ENVIRONMENT: str = 'development'
    DESCRIPTION: str = 'Serviço de registro de logs'
    VERSION: str = '0.1.0'

    DATABASE_URL: str
    DATABASE_SCHEMA: str

    MESSAGING_URL: str

    MIDDLEWARE_STARTLETTE: str
    NAME_ADMIN: str
    PASSWORD_ADMIN: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )


settings = Settings()
